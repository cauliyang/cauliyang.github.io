"""Procedural 'Bytes of Life' backdrop: teal/charcoal gradient, glowing 3D-ish double helix, dot grid, bokeh."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

TEAL = (45, 212, 191); PINK = (232, 121, 249); PALE = (204, 251, 241); MINT = (94, 234, 212)

def helix(draw_lines, draw_glow, W, H, S, cy, amp, wavelen, tilt, phase0, width, alpha, rung_every, bases=True):
    """Two sinusoidal strands; depth = cos(phase) modulates width/alpha so it reads as a helix."""
    def strand(phase):
        pts, depth = [], []
        for x in range(-W // 4, W + W // 4, 4 * S):
            th = 2 * math.pi * x / wavelen + phase
            y = cy + amp * math.sin(th)
            dx, dy = x - W / 2, y - cy
            rx = W / 2 + dx * math.cos(tilt) - dy * math.sin(tilt)
            ry = cy + dx * math.sin(tilt) + dy * math.cos(tilt)
            pts.append((rx, ry)); depth.append(0.5 + 0.5 * math.cos(th))  # 1 = front, 0 = back
        return pts, depth
    a, da = strand(phase0); b, db = strand(phase0 + math.pi)
    # rungs first (behind)
    for i in range(0, len(a), rung_every):
        draw_lines.line([a[i], b[i]], fill=PALE + (int(alpha * 0.45),), width=max(1, int(1.5 * S)))
    # strands as depth-modulated segments
    for pts, dep, col in ((a, da, TEAL), (b, db, PINK)):
        for i in range(len(pts) - 1):
            d = dep[i]
            w = max(1, int(width * (0.45 + 0.75 * d)))
            draw_lines.line([pts[i], pts[i + 1]], fill=col + (int(alpha * (0.35 + 0.65 * d)),), width=w)
            draw_glow.line([pts[i], pts[i + 1]], fill=col + (int(alpha * 0.55 * d),), width=w * 5)
        if bases:
            for i in range(0, len(pts), rung_every):
                d = dep[i]; x, y = pts[i]
                r = width * (0.9 + 1.1 * d)
                draw_lines.ellipse([x - r, y - r, x + r, y + r], fill=col + (int(alpha * (0.5 + 0.5 * d)),))
                draw_glow.ellipse([x - 3 * r, y - 3 * r, x + 3 * r, y + 3 * r], fill=col + (int(alpha * 0.6 * d),))

def gen(w, h, seed, out, scale=1.0):
    rnd = random.Random(seed)
    S = 2
    W, H = w * S, h * S
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = xx / W; v = yy / H

    # base: teal glow top-left -> stone-900 -> fuchsia dusk bottom-right
    c_teal = np.array([14, 52, 54], np.float32)
    c_mid = np.array([22, 24, 26], np.float32)
    c_pink = np.array([48, 18, 52], np.float32)
    t = np.clip(0.6 * u + 0.4 * v, 0, 1)[..., None]
    base = c_teal * (1 - t) + c_mid * t
    f = (np.clip((u - 0.5) * 1.8, 0, 1) * np.clip((v - 0.35) * 1.5, 0, 1))[..., None]
    base = base * (1 - 0.7 * f) + c_pink * 0.7 * f
    # soft light source top-left
    light = np.exp(-(((u - 0.12) ** 2) * 2.2 + ((v - 0.1) ** 2) * 3.0))[..., None]
    base = base + np.array([20, 90, 80], np.float32) * light * 0.55
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

    # dot grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    step = 40 * S
    for gy in range(step // 2, H, step):
        for gx in range(step // 2, W, step):
            fade = 0.35 + 0.65 * (1 - gx / W) * (1 - gy / H)
            gd.ellipse([gx - S, gy - S, gx + S, gy + S], fill=MINT + (int(70 * fade),))
    img = Image.alpha_composite(img, grid)

    lines = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lines); gdw = ImageDraw.Draw(glow)

    # background helix: small, faint, upper-right, different tilt
    helix(ld, gdw, W, H, S, cy=H * 0.22, amp=60 * S * scale, wavelen=520 * S * scale, tilt=0.12,
          phase0=1.1, width=2 * S, alpha=70, rung_every=14, bases=False)
    # main helix
    helix(ld, gdw, W, H, S, cy=H * 0.6, amp=170 * S * scale, wavelen=980 * S * scale, tilt=-0.2,
          phase0=0.4, width=4 * S, alpha=235, rung_every=8)

    # bokeh
    for _ in range(90):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.uniform(3, 14) * S
        col = rnd.choice([TEAL, TEAL, MINT, PINK])
        gdw.ellipse([x - r, y - r, x + r, y + r], fill=col + (int(rnd.uniform(60, 170)),))
    for _ in range(40):  # sharp pinpoint sparkles
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.uniform(0.8, 2.2) * S
        ld.ellipse([x - r, y - r, x + r, y + r], fill=PALE + (int(rnd.uniform(90, 200)),))

    glow = glow.filter(ImageFilter.GaussianBlur(26 * S))
    img = Image.alpha_composite(img, glow)
    img = Image.alpha_composite(img, lines.filter(ImageFilter.GaussianBlur(0.7 * S)))

    vig = np.sqrt((u - 0.5) ** 2 * 1.2 + (v - 0.5) ** 2)
    vig = np.clip(1 - 0.5 * vig ** 1.7, 0, 1)
    arr = np.asarray(img.convert("RGB")).astype(np.float32) * vig[..., None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").resize((w, h), Image.LANCZOS)
    img.save(out, quality=86, optimize=True, progressive=True)
    print(out, img.size)




def og_card(out):
    from PIL import ImageFont
    tmp = out + ".base.jpg"
    gen(1200, 630, 23, tmp, scale=0.7)
    im = Image.open(tmp).convert("RGBA")
    band = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(band).rectangle([0, 140, 1200, 470], fill=(10, 18, 20, 175))
    im = Image.alpha_composite(im, band.filter(ImageFilter.GaussianBlur(45)))
    d = ImageDraw.Draw(im)
    font = lambda size, index: ImageFont.truetype("/usr/share/fonts/inter/Inter.ttc", size, index=index)
    title, sub, small = font(118, 34), font(38, 10), font(26, 0)  # Inter Display ExtraBold, Inter Medium, Inter Regular
    def center(text, y, f, fill):
        w = d.textlength(text, font=f); d.text(((1200 - w) / 2, y), text, font=f, fill=fill)
    tw = d.textlength("Bytes of Life", font=title); x0 = (1200 - tw) / 2 - 16; y0 = 185
    d.text((x0, y0), "Bytes of Life", font=title, fill=(245, 245, 244))
    d.rectangle([x0 + tw + 14, y0 + 30, x0 + tw + 38, y0 + 122], fill=(20, 184, 166))
    center("Where algorithms meet biology", 350, sub, (153, 246, 228))
    center("yangyangli.top", 560, small, (168, 162, 158))
    im.convert("RGB").save(out, optimize=True)
    import os; os.remove(tmp)
    print(out, im.size)

if __name__ == "__main__":
    gen(1920, 1080, 7, "assets/img/hero-bytesoflife.jpg")
    gen(1600, 900, 11, "assets/img/featured-default.jpg", scale=0.85)
    og_card("assets/img/og-default.png")
