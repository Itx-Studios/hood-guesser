export function randomPointInCircle(centerX: number, centerY: number, radius: number): [number, number] {
    const theta = Math.random() * 2 * Math.PI;
    const r = radius * Math.sqrt(Math.random());

    const x = centerX + r * Math.cos(theta);
    const y = centerY + r * Math.sin(theta);

    return [x, y]
}
