import { app, BrowserWindow } from "electron";

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        title: "Hood Guesser",
        icon: "assets/icon.png",
        autoHideMenuBar: true,
        darkTheme: true,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            // preload: path.join(__dirname, "preload.js")
        }
    });

    win.loadFile(`dist/render/index.html`);
};

app.on("ready", () => {createWindow()});

app.on("window-all-closed", () => {
    process.platform !== "darwin" && app.quit();
});

app.on("activate", () => {
    BrowserWindow.getAllWindows().length === 0 && createWindow();
});
