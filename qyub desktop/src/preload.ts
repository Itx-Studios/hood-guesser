const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {
    send: (channel: string, ...args: any[]) => {
        console.log(`ipc send on channel "${channel}"\n\tdata: ${args.join(', ')}`);

        const validChannels = ["requestOpenStreetView", "requestCloseStreetView"];
        if (validChannels.includes(channel)) {
            ipcRenderer.send(channel, args);
        }
    },
    receive: (channel: string, func: (...args: any[]) => void) => {
        const validChannels = [""];
        if (validChannels.includes(channel)) {
            // Strip event as it includes `sender`
            ipcRenderer.on(channel, (_: any, ...args: any[]) => func(...args));
        }
    }
});