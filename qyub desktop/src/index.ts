import { app, BrowserWindow, ipcMain } from "electron";
import { createMainWindow, createStreetViewWindow, streetViewURL } from "./window.js";

app.on("ready", () => {
    createMainWindow();
});

app.on("window-all-closed", () => {
    process.platform !== "darwin" && app.quit();
});

app.on("activate", () => {
    BrowserWindow.getAllWindows().length === 0 && createMainWindow();
});

let streetViewWin: BrowserWindow | null = null;
let streetViewTimer: NodeJS.Timeout;

function setStreetViewTimer(time: number) {
    streetViewTimer = setTimeout(() => {
        if (streetViewWin && !streetViewWin.isDestroyed()) {
            streetViewWin.close();
        }
    }, time);
}

ipcMain.on("requestOpenStreetView", (_, [latitude, longitude, timer]: [number, number, number]) => {
    if (typeof latitude !== "number" || typeof longitude !== "number") {
        throw new Error("Invalid parameters: latitude and longitude must be numbers");
    }

    if (streetViewWin && !streetViewWin.isDestroyed()) {
        streetViewWin.loadURL(streetViewURL(latitude, longitude));
        clearTimeout(streetViewTimer);
        setStreetViewTimer(timer);
        return;
    }

    streetViewWin = createStreetViewWindow(latitude, longitude);

    streetViewWin.on("closed", () => {
        streetViewWin = null;
    })

    setStreetViewTimer(timer);
});

ipcMain.on("requestCloseStreetView", () => {
    if (streetViewWin && !streetViewWin.isDestroyed()) {
        streetViewWin.close();
        clearTimeout(streetViewTimer);
    }
});
