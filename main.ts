import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point for the news-image-20261118 entry.
// Copies the composed front-page image (entry.png, next to this file)
// into $MAKEFUN_OUTPUT_DIR/entry.png. Standard library only, no network.
const root = dirname(fileURLToPath(import.meta.url));
const src = join(root, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const dest = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error(`entry image not found: ${src}`);
}

const header = readFileSync(src).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!header.equals(pngMagic)) {
  throw new Error(`entry image is not a PNG file: ${src}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);

const size = statSync(dest).size;
if (size !== statSync(src).size) {
  throw new Error(`copied entry image has wrong size: ${dest} (${size} bytes)`);
}

console.log(`Wrote ${dest} (${size} bytes)`);
