import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point for the news-image-20261118 entry: copy the composed
// front-page image (entry.png, in this repository) to the output dir.
const root = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(root, "entry.png"), join(outDir, "entry.png"));
