import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os

base_dir = r'C:\Users\asus\.gemini\antigravity-ide\brain\c22f3a1f-ea5d-484f-a2ef-c17f6cddb7d1'
out_dir = r'c:\Users\asus\Documents\TOOFIT_TRAILORS\assets'
os.makedirs(out_dir, exist_ok=True)

# ----------------------------------------------------
# 1. LINEN CLUB (media__1789811071753.png)
# ----------------------------------------------------
linen_path = os.path.join(base_dir, 'media__1789811071753.png')
img = Image.open(linen_path).convert('RGB')

# Upscale x4 with BICUBIC for high sharpness
w, h = img.size
img_large = img.resize((w * 4, h * 4), Image.Resampling.BICUBIC)
arr = np.array(img_large, dtype=float)

# Bounding box of non-white pixels
diff = np.max(np.abs(arr - 255.0), axis=2)
coords = np.argwhere(diff > 15)
ymin, xmin = coords.min(axis=0)
ymax, xmax = coords.max(axis=0)

# Add padding
pad = 12
ymin = max(0, ymin - pad)
ymax = min(arr.shape[0], ymax + pad)
xmin = max(0, xmin - pad)
xmax = min(arr.shape[1], xmax + pad)

cropped = arr[ymin:ymax, xmin:xmax]

# Create transparent image where white becomes transparent
# Luminance calculation
lum = (cropped[:, :, 0] * 0.299 + cropped[:, :, 1] * 0.587 + cropped[:, :, 2] * 0.114)
# Alpha is 255 - lum (smooth alpha transition for anti-aliasing)
alpha = np.clip((255.0 - lum) * 1.5, 0, 255)

rgba = np.dstack((cropped[:, :, 0], cropped[:, :, 1], cropped[:, :, 2], alpha)).astype(np.uint8)
linen_out = Image.fromarray(rgba, mode='RGBA')
linen_out_path = os.path.join(out_dir, 'linen_club_official_logo.png')
linen_out.save(linen_out_path)
print('Saved Linen Club logo:', linen_out.size)


# ----------------------------------------------------
# 2. ARVIND (media__1789811085578.png)
# ----------------------------------------------------
arvind_path = os.path.join(base_dir, 'media__1789811085578.png')
img = Image.open(arvind_path).convert('RGB')
w, h = img.size
img_large = img.resize((w * 4, h * 4), Image.Resampling.BICUBIC)
arr = np.array(img_large, dtype=float)

diff = np.max(np.abs(arr - 255.0), axis=2)
coords = np.argwhere(diff > 15)
ymin, xmin = coords.min(axis=0)
ymax, xmax = coords.max(axis=0)

pad = 12
ymin = max(0, ymin - pad)
ymax = min(arr.shape[0], ymax + pad)
xmin = max(0, xmin - pad)
xmax = min(arr.shape[1], xmax + pad)

cropped = arr[ymin:ymax, xmin:xmax]
lum = (cropped[:, :, 0] * 0.299 + cropped[:, :, 1] * 0.587 + cropped[:, :, 2] * 0.114)
alpha = np.clip((255.0 - lum) * 1.6, 0, 255)

rgba = np.dstack((cropped[:, :, 0], cropped[:, :, 1], cropped[:, :, 2], alpha)).astype(np.uint8)
arvind_out = Image.fromarray(rgba, mode='RGBA')
arvind_out_path = os.path.join(out_dir, 'arvind_official_logo.png')
arvind_out.save(arvind_out_path)
print('Saved Arvind logo:', arvind_out.size)


# ----------------------------------------------------
# 3. SÖKTAŞ (media__1789811096003.png)
# Converts dark purple bg with white logo -> white/transparent bg with deep purple logo!
# ----------------------------------------------------
soktas_path = os.path.join(base_dir, 'media__1789811096003.png')
img = Image.open(soktas_path).convert('RGB')
w, h = img.size
img_large = img.resize((w * 4, h * 4), Image.Resampling.BICUBIC)
arr = np.array(img_large, dtype=float)

# Background color is dark purple (around R:67, G:44, B:95)
# White text/logo has high brightness (R,G,B > 180)
brightness = arr.mean(axis=2)
# Crop around logo area
coords = np.argwhere(brightness > 110)
ymin, xmin = coords.min(axis=0)
ymax, xmax = coords.max(axis=0)

pad = 16
ymin = max(0, ymin - pad)
ymax = min(arr.shape[0], ymax + pad)
xmin = max(0, xmin - pad)
xmax = min(arr.shape[1], xmax + pad)

cropped = arr[ymin:ymax, xmin:xmax]
b_crop = brightness[ymin:ymax, xmin:xmax]

# Map brightness to alpha: dark background -> alpha 0, white logo -> alpha 255
# Target color for SÖKTAŞ logo on white card: Deep Royal Purple (#4A1E5C => R:74, G:30, B:92)
purple_r, purple_g, purple_b = 74, 30, 92

min_b = 80.0
max_b = 200.0
alpha = np.clip((b_crop - min_b) / (max_b - min_b) * 255.0, 0, 255)

r_chan = np.full_like(alpha, purple_r)
g_chan = np.full_like(alpha, purple_g)
b_chan = np.full_like(alpha, purple_b)

rgba_soktas = np.dstack((r_chan, g_chan, b_chan, alpha)).astype(np.uint8)
soktas_out = Image.fromarray(rgba_soktas, mode='RGBA')
soktas_out_path = os.path.join(out_dir, 'soktas_official_logo.png')
soktas_out.save(soktas_out_path)
print('Saved Soktas logo:', soktas_out.size)


# ----------------------------------------------------
# 4. SCABAL (media__1789811054910.png)
# Dark navy bg with Gold crest & White text
# On white bg: Gold crest + Dark Navy text & tagline (#0B2545 => R:11, G:37, B:69)
# ----------------------------------------------------
scabal_path = os.path.join(base_dir, 'media__1789811054910.png')
img = Image.open(scabal_path).convert('RGB')
w, h = img.size
img_large = img.resize((w * 4, h * 4), Image.Resampling.BICUBIC)
arr = np.array(img_large, dtype=float)

# Background is dark navy (approx R:23, G:50, B:74)
b_crop = arr.mean(axis=2)
coords = np.argwhere(b_crop > 90)
ymin, xmin = coords.min(axis=0)
ymax, xmax = coords.max(axis=0)

pad = 16
ymin = max(0, ymin - pad)
ymax = min(arr.shape[0], ymax + pad)
xmin = max(0, xmin - pad)
xmax = min(arr.shape[1], xmax + pad)

cropped = arr[ymin:ymax, xmin:xmax]
b_crop = b_crop[ymin:ymax, xmin:xmax]

# Let's separate gold lion crest (upper ~40% of height) from white text (lower ~60%)
crop_h = ymax - ymin
crest_h = int(crop_h * 0.42)

# For crest (gold): keep original gold RGB, calculate alpha from brightness
alpha_crest = np.clip((b_crop[:crest_h, :] - 70.0) / 100.0 * 255.0, 0, 255)
# Boost gold color brightness slightly
gold_r = np.clip(cropped[:crest_h, :, 0] * 1.25, 0, 255)
gold_g = np.clip(cropped[:crest_h, :, 1] * 1.25, 0, 255)
gold_b = np.clip(cropped[:crest_h, :, 2] * 1.25, 0, 255)

rgba_top = np.dstack((gold_r, gold_g, gold_b, alpha_crest))

# For text (bottom): change white text to dark navy #0A192F (R:10, G:25, B:47)
alpha_text = np.clip((b_crop[crest_h:, :] - 70.0) / 100.0 * 255.0, 0, 255)
navy_r = np.full_like(alpha_text, 10)
navy_g = np.full_like(alpha_text, 25)
navy_b = np.full_like(alpha_text, 47)

rgba_bot = np.dstack((navy_r, navy_g, navy_b, alpha_text))

rgba_scabal = np.vstack((rgba_top, rgba_bot)).astype(np.uint8)
scabal_out = Image.fromarray(rgba_scabal, mode='RGBA')
scabal_out_path = os.path.join(out_dir, 'scabal_official_logo.png')
scabal_out.save(scabal_out_path)
print('Saved Scabal logo:', scabal_out.size)
