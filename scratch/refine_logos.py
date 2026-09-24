from PIL import Image, ImageFilter, ImageOps
import numpy as np
import os

base_dir = r'C:\Users\asus\.gemini\antigravity-ide\brain\c22f3a1f-ea5d-484f-a2ef-c17f6cddb7d1'
out_dir = r'c:\Users\asus\Documents\TOOFIT_TRAILORS\assets'

# Helper to remove background cleanly from light background images (Linen Club & Arvind)
def process_white_bg_logo(img_path, out_path, tint_rgb=None):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    # Upscale 4x with lanczos for ultra smooth curves
    large = img.resize((w * 4, h * 4), Image.Resampling.LANCZOS)
    arr = np.array(large, dtype=float)
    
    # Calculate background brightness (mean of top-left and top-right pixels)
    bg_color = (arr[:20, :20, :].mean(axis=(0,1)) + arr[:20, -20:, :].mean(axis=(0,1))) / 2.0
    
    # Distance from background color
    dist = np.linalg.norm(arr - bg_color, axis=2)
    
    # Alpha mask: dist < 10 -> 0, dist > 40 -> 255
    alpha = np.clip((dist - 8.0) / 32.0 * 255.0, 0, 255)
    
    # Soften alpha slightly
    alpha_img = Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    alpha_arr = np.array(alpha_img, dtype=float)
    
    if tint_rgb:
        r, g, b = tint_rgb
        out_r = np.full_like(alpha_arr, r)
        out_g = np.full_like(alpha_arr, g)
        out_b = np.full_like(alpha_arr, b)
    else:
        out_r = arr[:, :, 0]
        out_g = arr[:, :, 1]
        out_b = arr[:, :, 2]
        
    rgba = np.dstack((out_r, out_g, out_b, alpha_arr)).astype(np.uint8)
    
    # Bounding box crop
    nonzero = np.argwhere(alpha_arr > 10)
    ymin, xmin = nonzero.min(axis=0)
    ymax, xmax = nonzero.max(axis=0)
    
    pad = 16
    ymin = max(0, ymin - pad)
    ymax = min(rgba.shape[0], ymax + pad)
    xmin = max(0, xmin - pad)
    xmax = min(rgba.shape[1], xmax + pad)
    
    cropped_rgba = rgba[ymin:ymax, xmin:xmax]
    res = Image.fromarray(cropped_rgba, mode='RGBA')
    res.save(out_path)
    print(f"Saved {os.path.basename(out_path)}: {res.size}")

# 1. LINEN CLUB
process_white_bg_logo(
    os.path.join(base_dir, 'media__1789811071753.png'),
    os.path.join(out_dir, 'linen_club_official_logo.png')
)

# 2. ARVIND
process_white_bg_logo(
    os.path.join(base_dir, 'media__1789811085578.png'),
    os.path.join(out_dir, 'arvind_official_logo.png')
)

# 3. SÖKTAŞ - Dark purple background with white logo & text -> White card with Deep Purple logo
def process_soktas(img_path, out_path):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    large = img.resize((w * 4, h * 4), Image.Resampling.LANCZOS)
    arr = np.array(large, dtype=float)
    
    # Dark purple background average around corner
    bg_color = arr[:15, :15, :].mean(axis=(0,1))
    
    # Distance from purple background
    dist = np.linalg.norm(arr - bg_color, axis=2)
    
    # Alpha mask
    alpha = np.clip((dist - 15.0) / 45.0 * 255.0, 0, 255)
    alpha_img = Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    alpha_arr = np.array(alpha_img, dtype=float)
    
    # Target color: Deep Luxury Purple (#4A1E5C => 74, 30, 92)
    pr, pg, pb = 74, 30, 92
    r_chan = np.full_like(alpha_arr, pr)
    g_chan = np.full_like(alpha_arr, pg)
    b_chan = np.full_like(alpha_arr, pb)
    
    rgba = np.dstack((r_chan, g_chan, b_chan, alpha_arr)).astype(np.uint8)
    
    nonzero = np.argwhere(alpha_arr > 10)
    ymin, xmin = nonzero.min(axis=0)
    ymax, xmax = nonzero.max(axis=0)
    
    pad = 16
    ymin = max(0, ymin - pad)
    ymax = min(rgba.shape[0], ymax + pad)
    xmin = max(0, xmin - pad)
    xmax = min(rgba.shape[1], xmax + pad)
    
    res = Image.fromarray(rgba[ymin:ymax, xmin:xmax], mode='RGBA')
    res.save(out_path)
    print(f"Saved {os.path.basename(out_path)}: {res.size}")

process_soktas(
    os.path.join(base_dir, 'media__1789811096003.png'),
    os.path.join(out_dir, 'soktas_official_logo.png')
)

# 4. SCABAL - Dark navy background with Gold lion crest & White text -> Gold lion + Dark Navy text
def process_scabal(img_path, out_path):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    large = img.resize((w * 4, h * 4), Image.Resampling.LANCZOS)
    arr = np.array(large, dtype=float)
    
    bg_color = arr[:15, :15, :].mean(axis=(0,1))
    dist = np.linalg.norm(arr - bg_color, axis=2)
    
    alpha = np.clip((dist - 15.0) / 40.0 * 255.0, 0, 255)
    alpha_img = Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    alpha_arr = np.array(alpha_img, dtype=float)
    
    # Split into top lion crest (gold) and bottom text (navy)
    crop_h = arr.shape[0]
    crest_split = int(crop_h * 0.44)
    
    r_chan = np.zeros_like(alpha_arr)
    g_chan = np.zeros_like(alpha_arr)
    b_chan = np.zeros_like(alpha_arr)
    
    # Top lion crest: Enhance gold color (boost saturation/contrast)
    gold_r = np.clip(arr[:crest_split, :, 0] * 1.3, 0, 255)
    gold_g = np.clip(arr[:crest_split, :, 1] * 1.3, 0, 255)
    gold_b = np.clip(arr[:crest_split, :, 2] * 1.3, 0, 255)
    
    r_chan[:crest_split, :] = gold_r
    g_chan[:crest_split, :] = gold_g
    b_chan[:crest_split, :] = gold_b
    
    # Bottom text: Dark Navy #0A192F (R:10, G:25, B:47)
    r_chan[crest_split:, :] = 10
    g_chan[crest_split:, :] = 25
    b_chan[crest_split:, :] = 47
    
    rgba = np.dstack((r_chan, g_chan, b_chan, alpha_arr)).astype(np.uint8)
    
    nonzero = np.argwhere(alpha_arr > 10)
    ymin, xmin = nonzero.min(axis=0)
    ymax, xmax = nonzero.max(axis=0)
    
    pad = 16
    ymin = max(0, ymin - pad)
    ymax = min(rgba.shape[0], ymax + pad)
    xmin = max(0, xmin - pad)
    xmax = min(rgba.shape[1], xmax + pad)
    
    res = Image.fromarray(rgba[ymin:ymax, xmin:xmax], mode='RGBA')
    res.save(out_path)
    print(f"Saved {os.path.basename(out_path)}: {res.size}")

process_scabal(
    os.path.join(base_dir, 'media__1789811054910.png'),
    os.path.join(out_dir, 'scabal_official_logo.png')
)
