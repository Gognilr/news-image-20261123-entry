#!/usr/bin/env python3
"""Compose the 23 Nov 2026 world-news front page (1024x1024) for make.fun news-image-20261123.

Newsprint front page: masthead, generated hero photograph of the COP31
plenary hall in Antalya, two-line headline, five tagged stories and a
briefs footer. Every story is an event that happened, or was first
reported, on Monday 23 November 2026.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 44
PAPER = (246, 241, 231)
INK = (18, 18, 20)
NAVY = (16, 34, 64)
RED = (178, 34, 34)
RULE = (120, 110, 95)

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
HERO_PATH = os.path.join(
    RUN_DIR,
    "media-generation-news-hero-20261123-0-7c1b716b-c7b5-40d2-8b8e-15f32fbf23dd.webp",
)


def load_font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/noto/{name}", size)


TITLE_FONT = load_font("NotoSerif-Bold.ttf", 56)
DATE_FONT = load_font("NotoSans-Bold.ttf", 30)
HEADLINE_FONT = load_font("NotoSerif-Bold.ttf", 37)
TAG_FONT = load_font("NotoSans-Bold.ttf", 20)
STORY_FONT = load_font("NotoSerif-Bold.ttf", 26)
DECK_FONT = load_font("NotoSans-Regular.ttf", 20)
FOOT_FONT = load_font("NotoSans-Regular.ttf", 19)


def wrap_text(draw, text, font, max_width):
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_hero(path, width, height):
    photo = Image.open(path).convert("RGB")
    scale = max(width / photo.width, height / photo.height)
    resized = photo.resize(
        (int(photo.width * scale), int(photo.height * scale)), Image.LANCZOS
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def main():
    hero_w, hero_h = 936, 296
    hero = fit_hero(HERO_PATH, hero_w, hero_h)

    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    draw.rectangle([18, 18, W - 19, H - 19], outline=RULE, width=1)

    y = 34
    masthead = "THE WORLD IN ONE DAY"
    draw.text(
        ((W - draw.textlength(masthead, font=TITLE_FONT)) / 2, y),
        masthead,
        font=TITLE_FONT,
        fill=NAVY,
    )
    y += 70
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    y += 10
    dateline = "MONDAY, 23 NOVEMBER 2026"
    draw.text(
        ((W - draw.textlength(dateline, font=DATE_FONT)) / 2, y),
        dateline,
        font=DATE_FONT,
        fill=RED,
    )
    y += 42
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 14

    page.paste(hero, (MARGIN, y))
    draw.rectangle(
        [MARGIN, y, MARGIN + hero_w - 1, y + hero_h - 1], outline=INK, width=2
    )
    y += hero_h + 14

    for line in ["COP31 COLLAPSES WITH NO DEAL", "AS FOSSIL-FUEL ROW KILLS PACT"]:
        draw.text(
            ((W - draw.textlength(line, font=HEADLINE_FONT)) / 2, y),
            line,
            font=HEADLINE_FONT,
            fill=INK,
        )
        y += 44
    y += 4
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 12

    stories = [
        (
            "ANTALYA",
            "COP31 ends in deadlock after 48 hours of overtime",
            "EU and island states reject a draft that drops any fossil-fuel mention.",
        ),
        (
            "WASHINGTON",
            "Democrats clinch 258-seat House majority",
            "Biggest since 1992; Hubbard beats Foxx in North Carolina recount.",
        ),
        (
            "LIBYA",
            "Sea drones hit Russian warship at Benghazi",
            "Corvette Merkury capsizes; 10 hurt. Kyiv and Moscow stay silent.",
        ),
        (
            "INDONESIA",
            "24 body bags pulled from candy factory fire",
            "Blaze in Banten still smoulders; about 30 people unaccounted for.",
        ),
        (
            "YEMEN",
            "Strikes and Houthi drone attack kill 5, injure 18",
            "Coalition airstrikes and a Houthi drone hit across the country.",
        ),
    ]
    for tag, head, deck in stories:
        chip_w = draw.textlength(tag, font=TAG_FONT) + 18
        draw.rectangle([MARGIN, y, MARGIN + chip_w, y + 28], fill=NAVY)
        draw.text((MARGIN + 9, y + 3), tag, font=TAG_FONT, fill=PAPER)
        draw.text((MARGIN + chip_w + 12, y + 1), head, font=STORY_FONT, fill=INK)
        y += 30
        for deck_line in wrap_text(draw, deck, DECK_FONT, W - 2 * MARGIN - 24):
            draw.text((MARGIN + 24, y), deck_line, font=DECK_FONT, fill=INK)
            y += 24
        y += 8

    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 10
    briefs = (
        "Also today: Delta delays 1,000+ flights at Atlanta after a systems fault; "
        "South Korea's education minister quits over the college-exam cheating row; "
        "Russian strikes kill 6 near Kyiv; drones hit a UN building in Khartoum; "
        "North Korea's Kim says his country seeks security, not supremacy; "
        "Paolo Bulgari dies at 89."
    )
    for line in wrap_text(draw, briefs, FOOT_FONT, W - 2 * MARGIN):
        draw.text((MARGIN, y), line, font=FOOT_FONT, fill=INK)
        y += 23

    out_path = os.path.join(RUN_DIR, "entry.png")
    page.save(out_path, "PNG")
    print(f"wrote {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    main()
