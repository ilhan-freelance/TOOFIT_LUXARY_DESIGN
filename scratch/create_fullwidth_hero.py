import os
from PIL import Image, ImageFilter, ImageDraw

input_path = r'c:\Users\asus\Documents\TOOFIT_TRAILORS\assets\hero_royal_wedding_user.jpg'
output_path = r'c:\Users\asus\Documents\TOOFIT_TRAILORS\assets\hero_royal_wedding_fullwidth.jpg'

img = Image.open(input_path).convert('RGB')
w, h = img.size

# Target widescreen 2.5:1 ratio for full-bleed hero coverage
target_w = int(h * 2.5)
target_h = h

# Background wallpaper
bg = img.resize((target_w, target_h)).filter(ImageFilter.GaussianBlur(30))

# Create canvas
canvas = Image.new('RGB', (target_w, target_h))
canvas.paste(bg, (0, 0))

# Create gradient mask for smooth side blending
offset_x = (target_w - w) // 2
mask = Image.new('L', (w, h), 255)
draw = ImageDraw.Draw(mask)
feather = int(w * 0.12)

for i in range(feather):
    alpha = int(255 * (i / feather))
    draw.line([(i, 0), (i, h)], fill=alpha)
    draw.line([(w - 1 - i, 0), (w - 1 - i, h)], fill=alpha)

canvas.paste(img, (offset_x, 0), mask)
canvas.save(output_path, quality=98)
print(f"Successfully generated ultra-wide fullwidth image at {output_path} ({target_w}x{target_h})")
