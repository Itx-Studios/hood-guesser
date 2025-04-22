import { exec } from "node:child_process";
import fs from "node:fs";
import * as esbuild from "esbuild";
import path from "node:path";

const srcPath = "./src";

const distPath = "./dist";
fs.rmSync(distPath, {recursive: true, force: true});
fs.mkdirSync(distPath);

fs.cpSync(srcPath, distPath, {recursive: true});

exec("tsc", (err) => {
    err && console.error(err);
});

esbuild.buildSync({
    bundle: true,
    minify: true,
    entryPoints: ["./" + path.join(distPath, "render", "render.js")],
    outfile: "./" + path.join(distPath, "render", "bundle.min.js"),
});
