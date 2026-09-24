from PIL import Image, ImageFilter
import numpy as np
import os

base_dir = r'C:\Users\asus\.gemini\antigravity-ide\brain\c22f3a1f-ea5d-484f-a2ef-c17f6cddb7d1'
out_dir = r'c:\Users\asus\Documents\TOOFIT_TRAILORS\assets'

# 1. SÖKTAŞ:
# Original media__1789811096003.png is a purple rectangle with white text & logo inside.
# We want to extract ONLY the white pixels (emblem + SÖKTAŞ text), color them purple (#4A1E5C), and make everything else 100% transparent.
soktas_path = os.path.join(base_dir, 'media__1789811096003.png')
img = Image.open(soktas_path).convert('RGB')
w, h = img.size
large = img.resize((w * 4, h * 4), Image.Resampling.LANCZOS)
arr = np.array(large, dtype=float)

# Background color is purple (~ R:67, G:44, B:95). White text/logo pixels have high RGB (>160).
# Let's compute pixel distance from pure white (255, 255, 255) vs background.
dist_from_bg = np.linalg.norm(arr - arr[:10, :10, :].mean(axis=(0,1)), axis=2)

# Any pixel with dist_from_bg > 35 is part of logo/text
alpha = np.clip((dist_from_bg - 30.0) / 30.0 * 255.0, 0, 255)
alpha_img = Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
alpha_arr = np.array(alpha_img, dtype=float)

# Set RGB color to Deep Purple #4A1E5C (74, 30, 92) for the logo content
r_chan = np.full_like(alpha_arr, 74)
g_chan = np.full_like(alpha_arr, 30)
b_chan = np.full_like(alpha_arr, 92)

rgba_soktas = np.dstack((r_chan, g_chan, b_chan, alpha_arr)).astype(np.uint8)

nonzero = np.argwhere(alpha_arr > 15)
ymin, xmin = nonzero.min(axis=0)
ymax, xmax = nonzero.max(axis=0)
pad = 12
res_soktas = Image.fromarray(rgba_soktas[max(0, ymin-pad):min(rgba_soktas.shape[0], ymax+pad), max(0, xmin-pad):min(rgba_soktas.shape[1], xmax+pad)], mode='RGBA')
res_soktas.save(os.path.join(out_dir, 'soktas_official_logo.png'))
print('Soktas perfectly transparent saved:', res_soktas.size)

# 2. SCABAL:
# Original media__1789811054910.png is a dark navy rectangle with Gold crest & White text.
scabal_path = os.path.join(base_dir, 'media__1789811054910.png')
img = Image.open(scabal_path).convert('RGB')
w, h = img.size
large = img.resize((w * 4, h * 4), Image.Resampling.LANCZOS)
arr = np.array(large, dtype=float)

bg_col = arr[:10, :10, :].mean(axis=(0,1))
dist_from_bg = np.linalg.norm(arr - bg_col, axis=2)

alpha = np.clip((dist_from_bg - 30.0) / 30.0 * 255.0, 0, 255)
alpha_img = Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
alpha_arr = np.array(alpha_img, dtype=float)

crop_h = arr.shape[0]
crest_split = int(crop_h * 0.44)

r_chan = np.zeros_like(alpha_arr)
g_chan = np.zeros_like(alpha_arr)
b_chan = np.zeros_like(alpha_arr)

# Top lion crest: keep original gold color enhanced
r_chan[:crest_split, :] = np.clip(arr[:crest_split, :, 0] * 1.4, 0, 255)
g_chan[:crest_split, :] = np.clip(arr[:crest_split, :, 1] * 1.4, 0, 255)
b_chan[:crest_split, :] = np.clip(arr[:crest_split, :, 2] * 1.4, 0, 255)

# Bottom text: Dark Navy #0B2545 (11, 37, 69)
r_chan[crest_split:, :] = 11
g_chan[crest_split:, :] = 37
b_chan[crest_split:, :] = 69

rgba_scabal = np.dstack((r_chan, g_chan, b_chan, alpha_arr)).astype(np.uint8)

nonzero = np.argwhere(alpha_arr > 15)
ymin, xmin = nonzero.min(axis=0)
ymax, xmax = nonzero.max(axis=0)
pad = 12
res_scabal = Image.fromarray(rgba_scabal[max(0, ymin-pad):min(rgba_scabal.shape[0], ymax+pad), max(0, xmin-pad):min(rgba_scabal.shape[1], xmax+pad)], mode='RGBA')
res_scabal.save(os.path.join(out_dir, 'scabal_official_logo.png'))
print('Scabal perfectly transparent saved:', res_scabal.size)
