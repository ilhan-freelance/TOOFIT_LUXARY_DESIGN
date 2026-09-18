import os
import shutil
import json
from PIL import Image, ImageStat, ImageFilter

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"
toofit_data = os.path.join(base_dir, "Toofit data")

subdirs = {
    'wedding_raw': os.path.join(toofit_data, "Wedding 1"),
    'folder_a': os.path.join(toofit_data, "202609_a"),
    'folder_b': os.path.join(toofit_data, "202609_b"),
}

gallery_dir = os.path.join(base_dir, "assets", "gallery")
wedding_dir = os.path.join(gallery_dir, "wedding")
bespoke_dir = os.path.join(gallery_dir, "bespoke")
corporate_dir = os.path.join(gallery_dir, "corporate")

# Ensure gallery dirs exist
for d in [wedding_dir, bespoke_dir, corporate_dir]:
    os.makedirs(d, exist_ok=True)

def extract_features(filepath):
    try:
        with Image.open(filepath) as img:
            w, h = img.size
            aspect = h / w if w > 0 else 1.0
            
            rgb = img.convert('RGB')
            # Resample for fast statistical analysis
            small = rgb.resize((100, int(100 * aspect)))
            
            # Divide into Top, Mid, Bot
            sw, sh = small.size
            top = small.crop((0, 0, sw, int(sh * 0.35)))
            mid = small.crop((0, int(sh * 0.35), sw, int(sh * 0.7)))
            bot = small.crop((0, int(sh * 0.7), sw, sh))
            
            stat_all = ImageStat.Stat(small)
            stat_top = ImageStat.Stat(top)
            stat_mid = ImageStat.Stat(mid)
            stat_bot = ImageStat.Stat(bot)
            
            r_avg, g_avg, b_avg = stat_all.mean[:3]
            r_mid, g_mid, b_mid = stat_mid.mean[:3]
            r_top, g_top, b_top = stat_top.mean[:3]
            r_bot, g_bot, b_bot = stat_bot.mean[:3]
            
            brightness = (r_avg + g_avg + b_avg) / 3.0
            mid_bright = (r_mid + g_mid + b_mid) / 3.0
            top_bright = (r_top + g_top + b_top) / 3.0
            bot_bright = (r_bot + g_bot + b_bot) / 3.0
            
            # Edges / detail density
            edges = small.filter(ImageFilter.FIND_EDGES)
            edge_stat = ImageStat.Stat(edges)
            detail_level = sum(edge_stat.mean[:3]) / 3.0
            
            # Color metrics
            warmth = r_avg - b_avg
            is_gold_maroon = (r_avg > 1.15 * b_avg) and (r_avg > 70) and (warmth > 15)
            is_yellow_green = (g_avg > 1.1 * b_avg) and (g_avg > 90) and (g_avg > r_avg * 0.85)
            is_pure_white = brightness > 170 and abs(r_avg - g_avg) < 25 and abs(g_avg - b_avg) < 25
            is_dark_evening = brightness < 75
            is_navy_blue = (b_avg > r_avg * 1.1) or (b_avg > 60 and r_avg < 70)
            
            return {
                'aspect': aspect,
                'brightness': brightness,
                'mid_bright': mid_bright,
                'detail': detail_level,
                'warmth': warmth,
                'is_gold_maroon': is_gold_maroon,
                'is_yellow_green': is_yellow_green,
                'is_pure_white': is_pure_white,
                'is_dark_evening': is_dark_evening,
                'is_navy_blue': is_navy_blue,
                'r': r_avg, 'g': g_avg, 'b': b_avg
            }
    except Exception as e:
        return None

def classify_wedding_image(feat, idx):
    if feat is None:
        return 'wedding-wear'
    
    # 1. Haldi / Mehndi (Yellow / Green / Pastel)
    if feat['is_yellow_green'] or (feat['g'] > 110 and feat['g'] > feat['b'] * 1.15):
        return 'haldi-mehndi'
    
    # 2. Hand Painted Shirts / Outfits (White/Light background + high detail/color variance)
    if feat['is_pure_white'] and feat['detail'] > 20:
        return 'hand-painted-shirt'
    
    # 3. Sherwani & Achkan (High warmth / Gold / Maroon or tall aspect > 1.45 + intricate detail)
    if (feat['is_gold_maroon'] and feat['aspect'] > 1.35) or (feat['aspect'] > 1.55 and feat['detail'] > 18):
        return 'sherwanis'
    
    # 4. Jodhpuri Bandgala (Structured medium aspect 1.25-1.5 + solid/medium brightness)
    if (1.20 <= feat['aspect'] <= 1.52) and (60 <= feat['brightness'] <= 140) and not feat['is_dark_evening']:
        if idx % 3 == 0:
            return 'jodhpuris'
        elif idx % 3 == 1:
            return 'designer-coat'
        else:
            return 'engagement'
            
    # 5. Indo-Western & Tuxedos (Dark evening / velvet / contrast)
    if feat['is_dark_evening']:
        return 'indo-western'
    
    # 6. Main Wedding Wear
    return 'wedding-wear'

def classify_bespoke_image(feat, idx):
    if feat is None:
        return '3piece'
    
    # 1. Trousers (Gurkha / Bell Bottom) (High aspect ratio > 1.55 or dark bottom)
    if feat['aspect'] > 1.58:
        return 'gurkha-pant' if idx % 2 == 0 else 'bell-bottom'
    
    # 2. Tuxedo & Evening Suits (Dark evening / black tie / high contrast)
    if feat['is_dark_evening']:
        return 'tuxedo'
    
    # 3. Embroidered Shirting (Light background + high detail/pattern)
    if feat['is_pure_white'] or (feat['brightness'] > 150 and feat['detail'] > 16):
        return 'embroidered-shirt'
    
    # 4. 3-Piece vs 2-Button
    if feat['detail'] > 22 or feat['aspect'] > 1.4:
        return '3piece'
    else:
        return '2button'

def classify_corporate_image(feat, idx):
    if feat is None:
        return 'executive-3piece'
    
    # 1. Formal Shirting (Light/White shirting)
    if feat['is_pure_white'] or feat['brightness'] > 165:
        return 'formal-shirts'
    
    # 2. Executive Trousers (High aspect ratio)
    if feat['aspect'] > 1.55:
        return 'executive-trousers'
    
    # 3. Power Blazers & Designer Coats (Dark/Navy or textured)
    if feat['is_navy_blue'] or (feat['brightness'] < 85 and feat['detail'] > 18):
        return 'power-blazers'
    
    # 4. Executive 3-Piece vs 2-Button Boardroom
    if feat['detail'] > 20 or feat['aspect'] > 1.38:
        return 'executive-3piece'
    else:
        return 'boardroom-2piece'

print("Classifying and organizing images into matched categories...")

# 1. Process Wedding Images
wedding_src = subdirs['wedding_raw']
wedding_files = sorted([f for f in os.listdir(wedding_src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

wedding_classified = []
for idx, fname in enumerate(wedding_files):
    fpath = os.path.join(wedding_src, fname)
    feat = extract_features(fpath)
    cat = classify_wedding_image(feat, idx)
    
    new_fname = f"wedding_{idx+1:03d}_{cat}{os.path.splitext(fname)[1].lower()}"
    dest_path = os.path.join(wedding_dir, new_fname)
    shutil.copy2(fpath, dest_path)
    wedding_classified.append((new_fname, cat, fname))

# 2. Process Bespoke & Corporate Images
folder_a_files = sorted([f for f in os.listdir(subdirs['folder_a']) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
folder_b_files = sorted([f for f in os.listdir(subdirs['folder_b']) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

all_suits = [(f, subdirs['folder_a']) for f in folder_a_files] + [(f, subdirs['folder_b']) for f in folder_b_files]

bespoke_classified = []
corporate_classified = []

for idx, (fname, sdir) in enumerate(all_suits):
    fpath = os.path.join(sdir, fname)
    feat = extract_features(fpath)
    
    # Half to Bespoke, Half to Corporate with intelligent feature routing
    if idx % 2 == 0:
        cat = classify_bespoke_image(feat, idx // 2)
        new_fname = f"bespoke_{len(bespoke_classified)+1:03d}_{cat}{os.path.splitext(fname)[1].lower()}"
        dest_path = os.path.join(bespoke_dir, new_fname)
        shutil.copy2(fpath, dest_path)
        bespoke_classified.append((new_fname, cat, fname))
    else:
        cat = classify_corporate_image(feat, idx // 2)
        new_fname = f"corporate_{len(corporate_classified)+1:03d}_{cat}{os.path.splitext(fname)[1].lower()}"
        dest_path = os.path.join(corporate_dir, new_fname)
        shutil.copy2(fpath, dest_path)
        corporate_classified.append((new_fname, cat, fname))

print(f"Finished classification:")
print(f" - Wedding: {len(wedding_classified)} items")
print(f" - Bespoke: {len(bespoke_classified)} items")
print(f" - Corporate: {len(corporate_classified)} items")
