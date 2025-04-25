import * as L from "leaflet";
import { earthDistance, formatDistance, formatTime, getPolygonBounds, loadGameSet, randomPointInCircle, randomPointInPolygon } from "./utils";

export function gameData() {
    return {
        phase: null as "guess" | "reveal" | null,

        goal: [0, 0] as [number, number],
        timerInterval: null as NodeJS.Timeout | null,
        timeLeft: 0,

        map: null as L.Map | null,
        marker: null as L.Marker | null,
        goalMarker: null as L.Marker | null,
        distLine: null as L.Polyline | null,

        timeSelect: 30 as number,
        gameSetName: "Munich medium",
        gameSet: null as any,

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

            this.gameSet = loadGameSet(this.gameSetName);
        },

        handleNewGame() {
            if (!this.gameSet) return;

            if (this.gameSet.type === "polygon") {
                if (!this.gameSet.points) return;
                this.goal = randomPointInPolygon(this.gameSet.points);
            } else if (this.gameSet.type === "radius") {
                if (!this.gameSet.radius || !this.gameSet.center) return;
                if (!(this.gameSet.center instanceof Array)) return;
                if (this.gameSet.center.length !== 2 || !this.gameSet.center.every((val: any) => typeof val === "number")) return;
                if (typeof this.gameSet.radius !== "number") return;

                this.goal = randomPointInCircle(this.gameSet.center[0], this.gameSet.center[1], this.gameSet.radius);
            } else {
                return;
            }

            this.phase = "guess";

            window.api.send("requestOpenStreetView", this.goal[0], this.goal[1], this.timeSelect * 1000);

            this.timeLeft = this.timeSelect;

            this.timerInterval = setInterval(() => {
                this.timeLeft--;
                if (this.timeLeft === 0) {
                    alert("Time up");
                    this.handleGameResult();
                }
            }, 1000);

            this.map?.setView([0, 0], 20);

            if (this.gameSet.type === "radius") {
                this.map?.fitBounds(L.circle(this.gameSet.center, {radius: this.gameSet.radius}).getBounds(), {maxZoom: 13});
            } else {
                const [minX, maxX, minY, maxY] = getPolygonBounds(this.gameSet.points);
                this.map?.fitBounds(L.polygon([[minX, minY], [minX, maxY], [maxX, minY], [maxX, maxY]]).getBounds());
            }

            setTimeout(() => this.map?.invalidateSize(), 200);
        },

        handleSubmitGuess() {
            if (this.phase === "guess") {
                if (!this.timerInterval) return;

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
