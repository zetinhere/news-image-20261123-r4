# THE WORLD — Monday 23 November 2026

A newspaper front page that sums up 23 November 2026 in one image:
masthead and dateline, lead story on the COP31 climate talks collapsing
in Turkey, six more stories in two rows of three columns (Iran strikes
warning, Russian warship sunk off Libya, Kyiv strikes, Indonesia factory
fire, BepiColombo reaching Mercury, Nvidia soaring as Huang returns),
and an "Also today" footer ticker (Manchester concert evacuation, AI
Riemann-hypothesis claim, Seoul education minister resigning).

This is the third-round entry for `news-image-20261123` — a different
visual concept from the earlier collage grid (round 1) and 24-hour dial
(round 2).

## Build

```sh
python3 draw.py   # writes entry.png (1024x1024, deterministic)
```

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the committed `entry.png` into the output directory
and makes it world-readable (0644). No network is used at build or run
time; the image is drawn from scratch with PIL.
