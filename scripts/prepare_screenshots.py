from PIL import Image, ImageDraw, ImageFont
import os

# Files to process (from workspace static/)
INPUTS = [
    ("static/Immagine 2025-11-16 151332.png",
     "exports/screenshot_home_1200x675.png"),
    ("static/Immagine 2025-11-16 151246.png",
     "exports/screenshot_transactions_1200x675.png"),
]

OUT_W = 1200
OUT_H = 675
OVERLAY_TEXT = "EE • bitcoin-expense-tracker"


def center_crop_to_aspect(img, target_w, target_h):
    w, h = img.size
    target_aspect = target_w / target_h
    current_aspect = w / h
    if current_aspect > target_aspect:
        # image is too wide -> crop sides
        new_w = int(h * target_aspect)
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)
    else:
        # image is too tall -> crop top/bottom
        new_h = int(w / target_aspect)
        top = (h - new_h) // 2
        box = (0, top, w, top + new_h)
    return img.crop(box)


def add_overlay_text(img, text):
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
    padding = 12
    # use textbbox for reliable text measurement
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    rect_w = text_w + padding * 2
    rect_h = text_h + padding * 2
    # draw semi-transparent rectangle
    overlay_color = (0, 0, 0, 170)
    overlay = Image.new("RGBA", (rect_w, rect_h), overlay_color)
    img.paste(overlay, (20, 20), overlay)
    # draw text in bright color
    draw = ImageDraw.Draw(img)
    text_color = (200, 255, 200)
    draw.text((20 + padding, 20 + padding // 2),
              text, font=font, fill=text_color)
    return img


def process_image(in_path, out_path):
    if not os.path.exists(in_path):
        print(f"Input not found: {in_path}")
        return
    img = Image.open(in_path).convert("RGB")
    img = center_crop_to_aspect(img, OUT_W, OUT_H)
    img = img.resize((OUT_W, OUT_H), Image.LANCZOS)
    # convert to RGBA for overlay
    img = img.convert("RGBA")
    img = add_overlay_text(img, OVERLAY_TEXT)
    # save
    img.save(out_path, format="PNG")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    for inp, outp in INPUTS:
        os.makedirs(os.path.dirname(outp), exist_ok=True)
        process_image(inp, outp)
