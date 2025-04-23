interface Color {
    r: number;
    g: number;
    b: number;
}

interface Particle {
    x: number;
    y: number;
    size: number;
    speedX: number;
    speedY: number;
    color: Color;
}

export function particleData() {
    return {
        particles: [] as Particle[],
        mouse: { x: 0, y: 0 },
        canvas: null as HTMLCanvasElement | null,
        ctx: null as CanvasRenderingContext2D | null,
        numParticles: 160,
        $refs: null as any,

        init() {
            this.canvas = this.$refs.canvas as HTMLCanvasElement;
            this.ctx = this.canvas.getContext("2d");
            this.resizeCanvas();
            this.createParticles();
            this.animate();
        },

        resizeCanvas() {
            if (this.canvas) {
                this.canvas.width = window.innerWidth;
                this.canvas.height = window.innerHeight;
            }
        },

        createParticles() {
            for (let i = 0; i < this.numParticles; i++) {
                this.particles.push({
                    x: Math.random() * (this.canvas?.width || 0),
                    y: Math.random() * (this.canvas?.height || 0),
                    size: Math.random() * 3 + 1,
                    speedX: Math.random() * 2 - 1,
                    speedY: Math.random() * 2 - 1,
                    color: {
                        r: 0,
                        g: Math.floor(Math.random() * (255 - 200 + 1) + 200),
                        b: Math.floor(Math.random() * (255 - 200 + 1) + 200)
                    }
                });
            }
        },

        updateMouse(event: MouseEvent) {
            if (this.canvas) {
                const rect = this.canvas.getBoundingClientRect();
                this.mouse.x = event.clientX - rect.left;
                this.mouse.y = event.clientY - rect.top;
            }
        },

        animate() {
            if (this.ctx && this.canvas) {
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

                for (let particle of this.particles) {
                    const dx = particle.x - this.mouse.x;
                    const dy = particle.y - this.mouse.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 100) {
                        particle.speedX = dx / dist * 1.2;
                        particle.speedY = dy / dist * 1.2;
                    }

                    particle.x += particle.speedX * 0.5;
                    particle.y += particle.speedY * 0.5;
                    

                    if (particle.x < 0 || particle.x > this.canvas.width) particle.speedX *= -1;
                    if (particle.y < 0 || particle.y > this.canvas.height) particle.speedY *= -1;

                    this.drawParticle(particle);
                }

                requestAnimationFrame(() => this.animate());
            }
        },

        drawParticle(particle: Particle) {
            if (this.ctx) {
                this.ctx.beginPath();
                this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                this.ctx.fillStyle = `rgb(${particle.color.r}, ${particle.color.g}, ${particle.color.b})`;
                this.ctx.fill();
            }
        }
    };
}
