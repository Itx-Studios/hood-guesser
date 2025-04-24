import * as L from "leaflet";

export function gameData() {
    return {
        phase: null as "guess" | "reveal" | null,
        timer: null as NodeJS.Timeout | null,
        goal: [0, 0] as [number, number],

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
                    this.marker.remove();
                }

                this.marker = L.marker(e.latlng).addTo(this.map);
            });

            this.map.on("resize", () => {
                this.map?.invalidateSize();
            });

            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
            }).addTo(this.map);
        },

        handleNewGame() {
            const inData = {lat: 48.857508, lon: 2.295727, timer: 10000};

            window.api.send("requestOpenStreetView", inData.lat, inData.lon, inData.timer);

            this.map?.setView([inData.lat, inData.lon], 13);
            setTimeout(() => this.map?.invalidateSize(), 200);

            this.phase = "guess";
            this.goal = [inData.lat, inData.lon];

            this.timer = setTimeout(() => {
                alert("Time up!");
                this.handleGameResult();
            }, inData.timer);
        },

        handleSubmitGuess() {
            if (this.phase === "guess") {
                if (!this.timer) return;

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

            if (!this.marker) {
                //alert("No p l i");
            }

            if (this.timer) {
                clearTimeout(this.timer);
                this.timer = null;
            }

            this.phase = "reveal";

            const goal = new L.LatLng(this.goal[0], this.goal[1])
            this.goalMarker = L.marker(goal).addTo(this.map);

            if (this.marker) {
                const lineVector = [this.marker.getLatLng(), goal];

                this.distLine = L.polyline(lineVector, {
                    color: 'red',
                    weight: 3,
                    opacity: 0.5,
                    stroke: true,
                    dashOffset: ""
                }).addTo(this.map);
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
        }
    };
}
