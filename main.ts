// The World on Monday — entry for make.fun's news-image-20261123 bounty,
// "Sum up 23 November's world news in one image".
//
// The entry itself is the poster in entry.png beside this file: a front-page
// summary of Monday 23 November 2026 — Nvidia reinstating Jensen Huang as
// CEO, the Iran–Hormuz blockade standoff, India's $1.62bn package for
// Nepal, the EU's proposed 22nd sanctions package on Russia, Armenia's
// draft constitution dropping the Karabakh reference, and Bangladesh's
// warning that ex-PM Sheikh Hasina will be arrested if she returns —
// drawn programmatically by draw_image.py (kept in this repository as the
// record of how the image was made). This program's whole job is to place
// that image where the grader looks for it, /output/entry.png; outside
// the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const poster = new URL("entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

if (!existsSync(poster)) {
  throw new Error(`poster not found: ${poster}`);
}

// Validate the poster before copying: it must exist, be a real PNG, and be
// exactly 1024x1024, the size the bounty requires. Fail loudly instead of
// handing the grader a broken or wrong-sized file.
const head = readFileSync(poster).subarray(0, 33);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.subarray(0, 8).equals(PNG_MAGIC) || head.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error("entry.png is not a valid PNG file");
}
const width = head.readUInt32BE(16);
const height = head.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png must be 1024x1024, got ${width}x${height}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(poster, join(outDir, "entry.png"));
const bytes = statSync(poster).size;
console.log(`entry.png: ${bytes} bytes, ${width}x${height}, copied to ${join(outDir, "entry.png")}`);
