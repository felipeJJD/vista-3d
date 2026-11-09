"""Grava o modo demo do vista-3d quadro a quadro (relógio manual) e monta um MP4 1080x1920.

uso: python capture.py pagina.html saida.mp4 [--secs 16] [--fps 30] [--only 0,60,120]
--only salva só esses quadros como PNG (conferência rápida) ao lado da saída.
"""
import argparse, pathlib, subprocess, tempfile, shutil
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("page"); ap.add_argument("out")
ap.add_argument("--secs", type=float, default=16); ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--only", default="")
a = ap.parse_args()

page_url = pathlib.Path(a.page).resolve().as_uri() + "?capture"
out = pathlib.Path(a.out).resolve()
only = {int(x) for x in a.only.split(",") if x}
tmp = pathlib.Path(tempfile.mkdtemp(prefix="vista3d_"))
total = int(a.secs * a.fps)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader"])
    pg = b.new_page(viewport={"width": 390, "height": 694}, device_scale_factor=1080 / 390)
    pg.goto(page_url, wait_until="networkidle")
    pg.wait_for_function("window.__ready === true", timeout=60000)
    pg.evaluate("document.fonts.ready")
    for i in range(total + 1):
        if not only or i in only:
            dst = (out.parent / f"{out.stem}_{i:04d}.png") if only else (tmp / f"f{i:05d}.png")
            pg.screenshot(path=str(dst))
        if only and i >= max(only):
            break
        pg.evaluate(f"window.__step({1 / a.fps})")
    b.close()

if not only:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(a.fps), "-i", str(tmp / "f%05d.png"),
                    "-vf", "crop=1080:1920:0:0,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "slow", str(out)], check=True)
    print("ok", out)
shutil.rmtree(tmp, ignore_errors=True)
