import cv2
import numpy as np
from PIL import Image, ImageFilter
import os

base_dir = r'C:\Users\asus\.gemini\antigravity-ide\brain\c22f3a1f-ea5d-484f-a2ef-c17f6cddb7d1'
out_dir = r'c:\Users\asus\Documents\TOOFIT_TRAILORS\assets'
os.makedirs(out_dir, exist_ok=True)

# ----------------------------------------------------
# 1. SÖKTAŞ (media__1789811096003.png)
# Original: Purple BG + White Monogram/Text
# Goal: White BG + Deep Purple Monogram/Text
# ----------------------------------------------------
soktas_path = os.path.join(base_dir, 'media__1789811096003.png')
img = Image.open(soktas_path).convert('RGB')
w, h = img.size

# Upscale 4x with Lanczos for anti-aliasing
large = img.resize((w * 4, h * 4), Image.Resampling.LANCZOS)
arr = np.array(large, dtype=float)

# Background is purple. Logo/text is white/light pixels.
# Compute brightness of each pixel
brightness = arr.mean(axis=2)

# Background purple brightness ~ 65-75. White text/logo brightness ~ 160-255.
# Mask for white text/logo: 0 for bg, 1 for logo
bg_b = arr[:20, :20, :].mean()
logo_mask = np.clip((brightness - 90.0) / (180.0 - 90.0), 0.0, 1.0)

# Soften mask slightly for ultra smooth anti-aliased curves
mask_img = Image.fromarray((logo_mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
smooth_mask = np.array(mask_img, dtype=float) / 255.0

# Target Colors:
# Background: Pure White (255, 255, 255)
# Logo/Text: Deep Royal Purple (#4A1E5C => 74, 30, 92)
purple_r, purple_g, purple_b = 74, 30, 92

out_r = (1.0 - smooth_mask) * 255.0 + smooth_mask * purple_r
out_g = (1.0 - smooth_mask) * 255.0 + smooth_mask * purple_g
out_b = (1.0 - smooth_mask) * 255.0 + smooth_mask * purple_b

soktas_rgb = np.dstack((out_r, out_g, out_b)).astype(np.uint8)

# Crop to content box
nonzero = np.argwhere(smooth_mask > 0.05)
ymin, xmin = nonzero.min(axis=0)
ymax, xmax = nonzero.max(axis=0)

pad = 20
ymin = max(0, ymin - pad)
ymax = min(soktas_rgb.shape[0], ymax + pad)
xmin = max(0, xmin - pad)
xmax = min(soktas_rgb.shape[1], xmax + pad)

res_soktas = Image.fromarray(soktas_rgb[ymin:ymax, xmin:xmax], mode='RGB')
res_soktas.save(os.path.join(out_dir, 'soktas_official_logo.png'))
print('Saved SOKTAS logo (White BG + Purple text):', res_soktas.size)


# ----------------------------------------------------
# 2. SCABAL (media__1789811054910.png)
# Original: Dark Navy BG + Gold Crest (top) + White Text (bottom)
# Goal: White BG + Gold Crest (top) + Dark Navy Text (bottom)
# ----------------------------------------------------
scabal_path = os.path.join(base_dir, 'media__1789811054910.png')
img = Image.open(scabal_path).convert('RGB')
w, h = img.size
large = img.resize((w * 4, h * 4), Image.Resampling.LANCZOS)
arr = np.array(large, dtype=float)

brightness = arr.mean(axis=2)
bg_b = arr[:20, :20, :].mean()

logo_mask = np.clip((brightness - 55.0) / (130.0 - 55.0), 0.0, 1.0)
mask_img = Image.fromarray((logo_mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
smooth_mask = np.array(mask_img, dtype=float) / 255.0

crop_h = arr.shape[0]
crest_split = int(crop_h * 0.44)

# Create output channels initialized to pure white (255)
out_r = np.full_like(smooth_mask, 255.0)
out_g = np.full_like(smooth_mask, 255.0)
out_b = np.full_like(smooth_mask, 255.0)

# Top lion crest (gold): blend white bg with original gold pixels
gold_r = np.clip(arr[:crest_split, :, 0] * 1.35, 0, 255)
gold_g = np.clip(arr[:crest_split, :, 1] * 1.35, 0, 255)
gold_b = np.clip(arr[:crest_split, :, 2] * 1.35, 0, 255)

m_top = smooth_mask[:crest_split, :]
out_r[:crest_split, :] = (1.0 - m_top) * 255.0 + m_top * gold_r
out_g[:crest_split, :] = (1.0 - m_top) * 255.0 + m_top * gold_g
out_b[:crest_split, :] = (1.0 - m_top) * 255.0 + m_top * gold_b

# Bottom text (navy #0B2545 => 11, 37, 69)
navy_r, navy_g, navy_b = 11, 37, 69
m_bot = smooth_mask[crest_split:, :]
out_r[crest_split:, :] = (1.0 - m_bot) * 255.0 + m_bot * navy_r
out_g[crest_split:, :] = (1.0 - m_bot) * 255.0 + m_bot * navy_g
out_b[crest_split:, :] = (1.0 - m_bot) * 255.0 + m_bot * navy_b

scabal_rgb = np.dstack((out_r, out_g, out_b)).astype(np.uint8)

nonzero = np.argwhere(smooth_mask > 0.05)
ymin, xmin = nonzero.min(axis=0)
ymax, xmax = nonzero.max(axis=0)

pad = 20
ymin = max(0, ymin - pad)
ymax = min(scabal_rgb.shape[0], ymax + pad)
xmin = max(0, xmin - pad)
xmax = min(scabal_rgb.shape[1], xmax + pad)

res_scabal = Image.fromarray(scabal_rgb[ymin:ymax, xmin:xmax], mode='RGB')
res_scabal.save(os.path.join(out_dir, 'scabal_official_logo.png'))
print('Saved SCABAL logo (White BG + Gold crest + Navy text):', res_scabal.size)


# ----------------------------------------------------
# 3. LINEN CLUB (media__1789811071753.png)
# Original: White BG with Maroon text + silver flower
# Goal: Crop cleanly on white background
# ----------------------------------------------------
linen_path = os.path.join(base_dir, 'media__1789811071753.png')
img = Image.open(linen_path).convert('RGB')
w, h = img.size
large = img.resize((w * 4, h * 4), Image.Resampling.LANCZOS)
arr = np.array(large, dtype=float)

diff = np.max(np.abs(arr - 255.0), axis=2)
nonzero = np.argwhere(diff > 12)
ymin, xmin = nonzero.min(axis=0)
ymax, xmax = nonzero.max(axis=0)

pad = 16
ymin = max(0, ymin - pad)
ymax = min(arr.shape[0], ymax + pad)
xmin = max(0, xmin - pad)
xmax = min(arr.shape[1], xmax + pad)

res_linen = Image.fromarray(arr[ymin:ymax, xmin:xmax].astype(np.uint8), mode='RGB')
res_linen.save(os.path.join(out_dir, 'linen_club_official_logo.png'))
print('Saved LINEN CLUB logo:', res_linen.size)


# ----------------------------------------------------
# 4. ARVIND (media__1789811085578.png)
# Original: White BG with Red text + tagline
# Goal: Crop cleanly on white background
# ----------------------------------------------------
arvind_path = os.path.join(base_dir, 'media__1789811085578.png')
img = Image.open(arvind_path).convert('RGB')
w, h = img.size
large = img.resize((w * 4, h * 4), Image.Resampling.LANCZOS)
arr = np.array(large, dtype=float)

diff = np.max(np.abs(arr - 255.0), axis=2)
nonzero = np.argwhere(diff > 12)
ymin, xmin = nonzero.min(axis=0)
ymax, xmax = nonzero.max(axis=0)

pad = 16
ymin = max(0, ymin - pad)
ymax = min(arr.shape[0], ymax + pad)
xmin = max(0, xmin - pad)
xmax = min(arr.shape[1], xmax + pad)

res_arvind = Image.fromarray(arr[ymin:ymax, xmin:xmax].astype(np.uint8), mode='RGB')
res_arvind.save(os.path.join(out_dir, 'arvind_official_logo.png'))
print('Saved ARVIND logo:', res_arvind.size)
