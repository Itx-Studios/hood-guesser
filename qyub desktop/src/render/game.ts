export function gameData() {
    return {
        isActive: false,

        handleNewGame() {
            this.isActive = true;
            window.api.send('requestOpenStreetView', 48.857508, 2.295727, 30000);

            setTimeout(() => {
                this.isActive = false;
            }, 30000);
        }
    };
}
