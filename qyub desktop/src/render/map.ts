import * as L from "leaflet"

export function mapData() {
    return {
        map: null as L.Map | null,
        $el: null as any,

        init() {
            this.map = L.map(this.$el);
            this.map.setView([48.857508, 2.295727], 13);

            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
            }).addTo(this.map);
        }
    };
}
