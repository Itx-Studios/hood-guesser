import Alpine from 'alpinejs'
import { gameData } from './game';
import { backgroundData } from './background';

declare global {
    interface Window {
        api: any;
        Alpine: typeof Alpine;
        gameData: () => any;
        backgroundData: () => any;
    }
}

document.addEventListener('alpine:init', () => {
    Alpine.data("game", gameData);
});

window.gameData = gameData;
window.backgroundData = backgroundData;

window.Alpine = Alpine;
Alpine.start();
