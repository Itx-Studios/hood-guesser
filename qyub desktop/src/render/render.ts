import Alpine from 'alpinejs'
import { particleData } from './particle';
import { mapData } from './map';
import { gameData } from './game';
import { backgroundData } from './background';

declare global {
    interface Window {
        api: any;
        Alpine: typeof Alpine;
        particleData: () => any;
        mapData: (...args: any[]) => any;
        gameData: () => any;
        backgroundData: () => any;
    }
}

document.addEventListener('alpine:init', () => {
    Alpine.data("particleEffect", particleData);
    Alpine.data("map", mapData);
});

window.particleData = particleData;
window.mapData = mapData;
window.gameData = gameData;
window.backgroundData = backgroundData;

window.Alpine = Alpine;
Alpine.start();
