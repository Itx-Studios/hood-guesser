import Alpine from 'alpinejs'

declare global {
    interface Window {
        Alpine: typeof Alpine;
        particles: () => any;
    }
}

type Vector2D = [number, number];

function distanceSmaller(p1: Vector2D, p2: Vector2D, length: number): boolean {
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 < length**2;
}

function particles() {
    return {
        particles: Array.from({ length: 50 }, (_, i) => ({
            id: i,
            layer: Math.floor(Math.random() * 3),
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
        })),
        updateParticles(e: MouseEvent) {
            console.log("up");
            this.particles = this.particles.map(p => ({
                ...p,
                y: distanceSmaller([e.clientX, e.clientY], [p.x, p.y], 67)?  p.y + p.layer * 0.03: p.y,
                x: distanceSmaller([e.clientX, e.clientY], [p.x, p.y], 67)?  p.x + p.layer * 0.03: p.x,
            }));
        },
    };
}

window.particles = particles;
 
window.Alpine = Alpine;
Alpine.start();
