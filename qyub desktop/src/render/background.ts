export function backgroundData() {
    return {
        mouseX: 0,
        mouseY: 0,
        showBulb: false,
        $el: null as any,

        updateMouse(e: MouseEvent) {
            const rect = this.$el.getBoundingClientRect();
            this.mouseX = e.clientX - rect.left;
            this.mouseY = e.clientY - rect.top;
        }
    };
}
