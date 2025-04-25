export function randomPointInCircle(centerX: number, centerY: number, radius: number): [number, number] {
    const theta = Math.random() * 2 * Math.PI;
    const r = radius * Math.sqrt(Math.random());

    const x = centerX + r * Math.cos(theta);
    const y = centerY + r * Math.sin(theta);

    return [x, y]
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
