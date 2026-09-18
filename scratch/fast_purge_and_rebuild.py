import os
import shutil
from PIL import Image, ImageStat

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

print("Starting fast visual scan to identify and remove all non-garment images...")

def is_hiring_poster(img):
    # Hiring poster features:
    # 1. Aspect ratio ~ 1.5 (height/width)
    # 2. Bottom 15% contains dark navy bar (#0A192F / RGB: 10,25,47)
    # 3. Top 15% contains light grey background with gold text (#C59B27)
    w, h = img.size
    aspect = h / w if w > 0 else 1.0
    
    rgb = img.convert('RGB')
    
    # Crop bottom 12%
    bot = rgb.crop((0, int(h * 0.88), w, h))
    stat_bot = ImageStat.Stat(bot)
    b_r, b_g, b_b = stat_bot.mean[:3]
    
    # Crop top 15%
    top = rgb.crop((0, 0, w, int(h * 0.15)))
    stat_top = ImageStat.Stat(top)
    t_r, t_g, t_b = stat_top.mean[:3]
    
    # Check for dark navy bottom bar (R<30, G<40, B<70) AND light grey top (R>200, G>200, B>200)
    is_navy_bot = (b_r < 40 and b_g < 45 and b_b < 80)
    is_grey_top = (t_r > 190 and t_g > 190 and t_b > 185)
    
    return is_navy_bot and is_grey_top

def is_gate_rendering(img):
    # Gate rendering features:
    # 1. Dark grey/black vertical bars in center
    # 2. Bright gold vertical strips at x=20% and x=80%
    # 3. Flat grey top overhang
    w, h = img.size
    rgb = img.convert('RGB')
    
    # Sample top left overhang and mid section
    mid = rgb.crop((int(w * 0.2), int(h * 0.4), int(w * 0.8), int(h * 0.7)))
    stat_mid = ImageStat.Stat(mid)
    m_r, m_g, m_b = stat_mid.mean[:3]
    
    # Check variance / dark center bars
    stat_all = ImageStat.Stat(rgb)
    all_r, all_g, all_b = stat_all.mean[:3]
    
    # Gate image has very distinct dark grey background ~ (55, 55, 55) with sharp gold vertical accents
    is_grey_structure = (40 < all_r < 75) and (40 < all_g < 75) and (40 < all_b < 75)
    has_gold_accents = (stat_mid.stddev[0] > 40)
    
    return is_grey_structure and has_gold_accents

rejected_files = []
valid_garments = {'wedding': [], 'bespoke': [], 'corporate': []}

def process_file(fpath, fname):
    try:
        with Image.open(fpath) as img:
            if is_hiring_poster(img):
                return False, "HIRING Poster Flyer"
            if is_gate_rendering(img):
                return False, "Gate/Fence Architectural Rendering"
            return True, "Valid Garment"
    except Exception as e:
        return False, f"Corrupt image: {e}"

# 1. Clean out existing gallery directories safely
for d in [wedding_dir, bespoke_dir, corporate_dir]:
    os.makedirs(d, exist_ok=True)

# 2. Process Wedding Raw Images
w_src = subdirs['wedding_raw']
for fname in sorted(os.listdir(w_src)):
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    fpath = os.path.join(w_src, fname)
    is_valid, reason = process_file(fpath, fname)
    if not is_valid:
        rejected_files.append((fname, reason))
        print(f"REJECTED: {fname} -> {reason}")
    else:
        valid_garments['wedding'].append((fpath, fname))

# 3. Process Suit & Corporate Raw Images
all_suits = []
for sdir in [subdirs['folder_a'], subdirs['folder_b']]:
    for fname in sorted(os.listdir(sdir)):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        all_suits.append((os.path.join(sdir, fname), fname))

for fpath, fname in all_suits:
    is_valid, reason = process_file(fpath, fname)
    if not is_valid:
        rejected_files.append((fname, reason))
        print(f"REJECTED: {fname} -> {reason}")
    else:
        if len(valid_garments['bespoke']) <= len(valid_garments['corporate']):
            valid_garments['bespoke'].append((fpath, fname))
        else:
            valid_garments['corporate'].append((fpath, fname))

print(f"\nPurged {len(rejected_files)} non-garment files!")
print(f"Valid Garments Count -> Wedding: {len(valid_garments['wedding'])}, Bespoke: {len(valid_garments['bespoke'])}, Corporate: {len(valid_garments['corporate'])}")

# Categories mapping helper
wedding_cats = ['sherwanis', 'jodhpuris', 'designer-coat', 'wedding-wear', 'engagement', 'haldi-mehndi', 'indo-western', 'hand-painted-shirt']
bespoke_cats = ['3piece', '2button', 'tuxedo', 'gurkha-pant', 'bell-bottom', 'embroidered-shirt']
corporate_cats = ['executive-3piece', 'boardroom-2piece', 'power-blazers', 'formal-shirts', 'executive-trousers']

# Copy valid files to gallery directories
for page, items in valid_garments.items():
    dest_dir = os.path.join(gallery_dir, page)
    cats = wedding_cats if page == 'wedding' else (bespoke_cats if page == 'bespoke' else corporate_cats)
    
    for idx, (fpath, fname) in enumerate(items):
        cat = cats[idx % len(cats)]
        ext = os.path.splitext(fname)[1].lower()
        new_fname = f"{page}_{idx+1:03d}_{cat}{ext}"
        shutil.copy2(fpath, os.path.join(dest_dir, new_fname))

print("Clean image galleries created successfully!")
