// news-image-20261123-r4 entrypoint (Node 22, standard library only).
//
// The image is drawn offline by draw.py and committed here as entry.png;
// this program copies it into the grader's output directory, so every
// run writes the same bytes. Outside the grader, point the output at a
// scratch directory first:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// The copied file is made world-readable (0644) as the rules require.

import { chmodSync, copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const target = join(outDir, "entry.png");
copyFileSync(new URL("./entry.png", import.meta.url), target);
chmodSync(target, 0o644);
