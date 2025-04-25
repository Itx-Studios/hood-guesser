const gameSets = require("../../gameSets.json");

export function randomPointInCircle(centerX: number, centerY: number, radius: number): [number, number] {
    const theta = Math.random() * 2 * Math.PI;
    const r = radius * Math.sqrt(Math.random());

    const x = centerX + r * Math.cos(theta);
    const y = centerY + r * Math.sin(theta);

    return [x, y]
}

function randomFloat(min: number, max: number): number {
    return Math.random() * (max - min) + min;
}

export function getPolygonBounds(polygon: [number, number][]): [number, number, number, number] {
    return [
        Math.min(...polygon.map(([x]) => x)),
        Math.max(...polygon.map(([x]) => x)),
        Math.min(...polygon.map(([_, y]) => y)),
        Math.max(...polygon.map(([_, y]) => y)),  
    ];
}

function round(value: number, precision: number): number {
    return Math.round(value * precision) / precision;
}

export function isPointInPolygon(polygon: [number, number][], point: [number, number], precision: number): boolean {
    const x = round(point[0], precision);
    const y = round(point[1], precision);
    let inside = false;
  
    for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
        const xi = round(polygon[i][0], precision);
        const yi = round(polygon[i][1], precision);
        const xj = round(polygon[j][0], precision);
        const yj = round(polygon[j][1], precision);

        const intersects = (yi > y) !== (yj > y) &&
            x < round(xi + ((y - yi) * (xj - xi)) / (yj - yi), precision);

        if (intersects) {
            inside = !inside;
        }
    }
  
    return inside;
}

export function randomPointInPolygon(polygon: [number, number][]): [number, number] {
    const [minX, maxX, minY, maxY] = getPolygonBounds(polygon);

    let attempts = 0;
    const maxAttempts = 10000;

    while (attempts < maxAttempts) {
        attempts++;
        const rndX = randomFloat(minX, maxX);
        const rndY = randomFloat(minY, maxY);
        const rndPoint: [number, number] = [rndX, rndY];

        if (isPointInPolygon(polygon, rndPoint, 1e6)) {
            return rndPoint;
        }
    }

    throw new Error(`No point found`);
}

function degreesToRadians(degrees: number) {
    return degrees * Math.PI / 180;
}
  
export function earthDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
    const earthRadius = 6371000;
  
    const dLat = degreesToRadians(lat2-lat1);
    const dLon = degreesToRadians(lon2-lon1);
  
    lat1 = degreesToRadians(lat1);
    lat2 = degreesToRadians(lat2);
  
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    return earthRadius * c;
}

export function formatDistance(dist: number): string {
    if (dist >= 1000) {
        return `${Math.round(dist / 1000)}.${Math.round(dist % 1000)}km`;
    } else {
        return Math.round(dist) + "m";
    }
}

export function formatTime(time: number): string {
    if (time >= 60) {
        let minutes: number | string = time % 60;
        let seconds: number | string = Math.floor(time / 60);
        if (minutes < 10) minutes = "0" + minutes;
        if (seconds < 10) seconds = "0" + seconds;
        return `${time % 60}:${Math.floor(time / 60)}`;
    } else {
        let seconds: number | string = time;
        if (seconds < 10) seconds = "0" + seconds;
        return `00:${seconds}`;
    }
}

export function loadGameSet(name: string): Object | null {
    if (!(gameSets instanceof Array)) return null;

    for (const gameSet of gameSets) {
        if (gameSet.name === name) {
            return gameSet;
        }
    }
    return null;
}
