import * as L from "leaflet";
import { earthDistance, formatDistance, formatTime } from "./utils";

export function gameData() {
    return {
        phase: null as "guess" | "reveal" | null,
        goal: [0, 0] as [number, number],
        timerTimeout: null as NodeJS.Timeout | null,
        timerInterval: null as NodeJS.Timeout | null,
        timeLeft: 0,

        map: null as L.Map | null,
        marker: null as L.Marker | null,
        goalMarker: null as L.Marker | null,
        distLine: null as L.Polyline | null,

        $refs: null as any,

        init() {
            this.map = L.map(this.$refs.mapDiv as HTMLDivElement);

            this.map.on("click", (e) => {
                if (!this.map || this.phase !== "guess") return;

                if (this.marker) {
                    this.marker.setLatLng(e.latlng);
                    return;
                }

                const pinIcon =  L.icon({iconUrl: "../../assets/pin.svg", iconSize: [42, 42], iconAnchor: [22, 37]});
                this.marker = L.marker(e.latlng, {title: "Your guess", icon: pinIcon}).addTo(this.map);
            });

            this.map.on("keydown", (e) => {
                if (e.originalEvent.key === "Enter") {
                    this.handleSubmitGuess();
                }
            });

            this.map.on("resize", () => {
                this.map?.invalidateSize();
            });

            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
            }).addTo(this.map);
        },

        handleNewGame() {
            const inData = {lat: 48.857508, lon: 2.295727, timer: 20000};

            this.phase = "guess";
            this.goal = [inData.lat, inData.lon];

            window.api.send("requestOpenStreetView", inData.lat, inData.lon, inData.timer);

            this.map?.setView([inData.lat, inData.lon], 13);
            setTimeout(() => this.map?.invalidateSize(), 200);

            this.timeLeft = Math.round(inData.timer / 1000);

            this.timerTimeout = setTimeout(() => {
                alert("Time up!");
                this.handleGameResult();
            }, inData.timer);

            this.timerInterval = setInterval(() => {
                this.timeLeft--;
            }, 1000);
        },

        handleSubmitGuess() {
            if (this.phase === "guess") {
                if (!this.timerTimeout) return;

                if (!this.marker) {
                    alert("No point selected");
                    return;
                } 
    
                this.handleGameResult();
            } else if (this.phase === "reveal") {
                this.handleHideResult();
            }
        },

        handleGameResult() {
            if (!this.map) return;

            if (this.timerTimeout) {
                clearTimeout(this.timerTimeout);
                this.timerTimeout = null;
            }

            if (this.timerInterval) {
                clearInterval(this.timerInterval);
                this.timerInterval = null;
            }

            this.phase = "reveal";

            const goal = new L.LatLng(this.goal[0], this.goal[1])
            const goalIcon =  L.icon({iconUrl: "../../assets/score_flag.svg", iconSize: [42, 42], iconAnchor: [10, 36.5]});
            this.goalMarker = L.marker(goal, {icon: goalIcon, title: "The goal"}).addTo(this.map);

            if (this.marker) {
                const markerLatLng = this.marker.getLatLng();

                const line = [markerLatLng, goal];

                this.distLine = L.polyline(line, {
                    color: "red",
                    weight: 3,
                    opacity: 0.8,
                    stroke: true,
                }).addTo(this.map);

                const distance = earthDistance(this.goal[0], this.goal[1], markerLatLng.lat, markerLatLng.lng);
                const fDistance = formatDistance(distance);
                
                const popup = L.popup({autoClose: false, closeOnClick: false})
                .setContent(`<h3>Distance: ${fDistance}</h3>`)
                .setLatLng(this.distLine.getCenter());

                this.distLine.bindPopup(popup).openPopup(this.distLine.getCenter());

                this.map.fitBounds(this.distLine.getBounds());
            } else {
                this.map.fitBounds(this.goalMarker.getLatLng().toBounds(0), {maxZoom: 15});
            }
        },

        handleHideResult() {
            this.marker?.remove();
            this.goalMarker?.remove();
            this.distLine?.remove();

            this.marker = null;
            this.goalMarker = null;
            this.distLine = null;

            this.phase = null;
            this.goal = [0, 0];
        },

        formatTime: formatTime,
    };
}
