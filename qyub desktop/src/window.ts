import { BrowserWindow, BrowserWindowConstructorOptions } from "electron";
import path, { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

function createWindow(
    title: string,
    width: number,
    height: number,
    file: boolean,
    entry: string,
    preload?: string,
    more?: BrowserWindowConstructorOptions
): BrowserWindow {
    const win = new BrowserWindow({
        width,
        height,
        title,
        icon: path.normalize(path.join(__dirname, "..", "assets", "icon.png")),
        autoHideMenuBar: true,
        darkTheme: true,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload
        },
        ...more
    });

    if (file) {
        win.loadFile(entry);
    } else {
        win.loadURL(entry);
    }

    win.on("ready-to-show", () => {
        win.show();
        win.focus();
    });

    return win;
};

export function createMainWindow() {
    createWindow(
        "Hood Guesser",
        800,
        600,
        true,
        path.join(__dirname, "render", "index.html"),
        path.join(__dirname, "preload.js")
    );
}

export function streetViewURL(latitude: number, longitude: number): string {
    return `https://maps.google.com/maps?q=&layer=c&cbll=${latitude},${longitude}`;
}

export function createStreetViewWindow(latitude: number, longitude: number): BrowserWindow {
    const win = createWindow(
        "Hood Guesser",
        800,
        600,
        false,
        streetViewURL(latitude, longitude)
    );
    win.maximize();
    return win;
}
