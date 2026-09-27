"""Génère l'icône (toque de l'onglet Recettes) et l'écran de démarrage Android.

Lancé une fois en local ; les PNG produits sont commités dans resources/android/res
et copiés dans le projet Android par le workflow GitHub Actions.
Usage : python3 resources/generate_icons.py
"""
import math
import os
from PIL import Image, ImageDraw

PINK = (243, 211, 211)      # --pink  #F3D3D3 (rose pastel de l'app)
BORDEAUX = (114, 47, 53)    # --bordeaux #722F35
CREAM = (253, 248, 245)     # --cream #FDF8F5

OUT = os.path.join(os.path.dirname(__file__), "android", "res")


def arc(p0, rx, large, sweep, p1, steps=60):
    """Arc SVG (rx=ry, sans rotation) -> liste de points."""
    x1, y1 = p0
    x2, y2 = p1
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    r = rx
    d2 = dx * dx + dy * dy
    if d2 > r * r:
        r = math.sqrt(d2)
    coef = math.sqrt(max(0, (r * r - d2) / d2))
    if large == sweep:
        coef = -coef
    cx = coef * dy + (x1 + x2) / 2
    cy = -coef * dx + (y1 + y2) / 2
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    da = a2 - a1
    if sweep and da < 0:
        da += 2 * math.pi
    if not sweep and da > 0:
        da -= 2 * math.pi
    return [(cx + r * math.cos(a1 + da * i / steps), cy + r * math.sin(a1 + da * i / steps)) for i in range(steps + 1)]


def toque_paths():
    # Même tracé que l'icône « Recettes » de la barre du bas (viewBox 24x24)
    pts = [(6, 13)]
    pts += arc((6, 13), 4, 1, 1, (7.5, 5.3))[1:]
    pts += arc((7.5, 5.3), 5, 0, 1, (16.5, 5.3))[1:]
    pts += arc((16.5, 5.3), 4, 1, 1, (18, 13))[1:]
    pts += [(18, 20), (6, 20), (6, 13)]
    return [pts, [(6, 16), (18, 16)]]


def draw_toque(size, scale, bg, fg, stroke=1.9, offset=(0, 0)):
    """Dessine la toque centrée sur un carré `size`, occupant `scale` de la largeur."""
    ss = 4
    S = size * ss
    img = Image.new("RGBA", (S, S), bg)
    d = ImageDraw.Draw(img)
    # boîte englobante du dessin : x 2..22, y 1.3..20
    k = S * scale / 20.0
    ox = S / 2 - 12 * k + offset[0] * S
    oy = S / 2 - 10.65 * k + offset[1] * S
    w = max(1, int(stroke * k))
    for path in toque_paths():
        P = [(ox + x * k, oy + y * k) for x, y in path]
        # trait « pinceau rond » : disques rapprochés le long du tracé (joints propres)
        rad = w / 2
        for (xa, ya), (xb, yb) in zip(P, P[1:]):
            n = max(1, int(math.hypot(xb - xa, yb - ya) / (rad * 0.25)))
            for i in range(n + 1):
                x, y = xa + (xb - xa) * i / n, ya + (yb - ya) * i / n
                d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=fg)
    return img.resize((size, size), Image.LANCZOS)


def rounded(img, radius_ratio):
    size = img.size[0]
    ss = 4
    m = Image.new("L", (size * ss, size * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size * ss - 1, size * ss - 1], radius=size * ss * radius_ratio, fill=255)
    m = m.resize((size, size), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), m)
    return out


def save(img, *parts):
    path = os.path.join(OUT, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)


DENS = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}

for name, f in DENS.items():
    # icône classique (anciens Android) : carré arrondi rose + toque bordeaux
    s = int(48 * f)
    save(rounded(draw_toque(s, 0.62, PINK, BORDEAUX), 0.22), f"mipmap-{name}", "ic_launcher.png")
    save(rounded(draw_toque(s, 0.58, PINK, BORDEAUX), 0.5), f"mipmap-{name}", "ic_launcher_round.png")
    # icône adaptative : premier plan transparent (zone sûre = 66 % centraux)
    s = int(108 * f)
    save(draw_toque(s, 0.50, (0, 0, 0, 0), BORDEAUX), f"mipmap-{name}", "ic_launcher_foreground.png")

# écran de démarrage (remplace le logo Capacitor)
SPLASH = {"mdpi": (320, 480), "hdpi": (480, 800), "xhdpi": (720, 1280), "xxhdpi": (960, 1600), "xxxhdpi": (1280, 1920)}


def splash(w, h):
    img = Image.new("RGB", (w, h), CREAM)
    s = int(min(w, h) * 0.42)
    logo = rounded(draw_toque(s, 0.6, PINK, BORDEAUX), 0.22)
    img.paste(logo, ((w - s) // 2, (h - s) // 2), logo)
    return img


for name, (w, h) in SPLASH.items():
    save(splash(w, h), f"drawable-port-{name}", "splash.png")
    save(splash(h, w), f"drawable-land-{name}", "splash.png")
save(splash(480, 480), "drawable", "splash.png")

# aperçu pour le README
os.makedirs(os.path.join(os.path.dirname(__file__), "preview"), exist_ok=True)
rounded(draw_toque(512, 0.62, PINK, BORDEAUX), 0.22).save(os.path.join(os.path.dirname(__file__), "preview", "icon-512.png"))
print("OK")
