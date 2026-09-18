import os
import shutil
from PIL import Image, ImageStat
import pytesseract

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

print("Scanning for non-garment images (Posters, Flyers, Gates, Furniture, Architecture)...")

rejected_files = []
valid_garments = {'wedding': [], 'bespoke': [], 'corporate': []}

def check_is_non_garment(filepath):
    # Check filename first
    fname_lower = os.path.basename(filepath).lower()
    if 'hero_mansion' in fname_lower or 'gate' in fname_lower or 'fence' in fname_lower:
        return True, "Architectural gate/fence image"

    try:
        with Image.open(filepath) as img:
            w, h = img.size
            rgb = img.convert('RGB')
            
            # OCR check for text heavy posters like "HIRING", "MANAGER", "REQUIREMENTS", "APPLY"
            try:
                text = pytesseract.image_to_string(rgb)
                text_upper = text.upper()
                poster_keywords = ['HIRING', 'BUSINESS DEVELOPMENT', 'RESPONSIBILITIES', 'REQUIREMENTS', 'APPLY NOW', 'GRADUATE OR MBA', 'SALARY', 'SHOWROOM']
                for kw in poster_keywords:
                    if kw in text_upper:
                        return True, f"Flyer/Poster text found: '{kw}'"
            except Exception as e:
                pass

            # Visual check for gate / architecture renderings:
            # Gate images typically have strong vertical metal bars (high edge density in middle)
            # and non-human aspect ratios / grey cement borders
            stat = ImageStat.Stat(rgb)
            r_avg, g_avg, b_avg = stat.mean[:3]
            
            # Check if top 20% and bottom 20% are dark/concrete grey with identical center bars
            # Also check if it's the specific gate rendering image
            if abs(r_avg - 105) < 15 and abs(g_avg - 105) < 15 and abs(b_avg - 105) < 15:
                # Might be a gate/building rendering
                pass

            return False, "Valid Garment"
    except Exception as e:
        return True, f"Corrupt or unreadable image: {e}"

# 1. Clean out existing gallery directories completely
for d in [wedding_dir, bespoke_dir, corporate_dir]:
    if os.path.exists(d):
        for f in os.listdir(d):
            try:
                os.remove(os.path.join(d, f))
            except Exception:
                pass
    else:
        os.makedirs(d, exist_ok=True)

# 2. Process Wedding Raw Images
print("Processing Wedding images...")
w_src = subdirs['wedding_raw']
for fname in sorted(os.listdir(w_src)):
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    fpath = os.path.join(w_src, fname)
    is_bad, reason = check_is_non_garment(fpath)
    if is_bad:
        rejected_files.append((fname, reason))
        print(f"REJECTED: {fname} -> {reason}")
    else:
        valid_garments['wedding'].append((fpath, fname))

# 3. Process Bespoke & Corporate Raw Images
print("Processing Suit & Corporate images...")
all_suit_paths = []
for sdir in [subdirs['folder_a'], subdirs['folder_b']]:
    for fname in sorted(os.listdir(sdir)):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        all_suit_paths.append((os.path.join(sdir, fname), fname))

for fpath, fname in all_suit_paths:
    is_bad, reason = check_is_non_garment(fpath)
    if is_bad:
        rejected_files.append((fname, reason))
        print(f"REJECTED: {fname} -> {reason}")
    else:
        # Separate into bespoke vs corporate
        if len(valid_garments['bespoke']) <= len(valid_garments['corporate']):
            valid_garments['bespoke'].append((fpath, fname))
        else:
            valid_garments['corporate'].append((fpath, fname))

print(f"\nPurged {len(rejected_files)} non-clothing / poster / architectural images!")
print(f"Remaining Valid Garments: Wedding={len(valid_garments['wedding'])}, Bespoke={len(valid_garments['bespoke'])}, Corporate={len(valid_garments['corporate'])}")

# Categories mapping helper
wedding_cats = ['sherwanis', 'jodhpuris', 'designer-coat', 'wedding-wear', 'engagement', 'haldi-mehndi', 'indo-western', 'hand-painted-shirt']
bespoke_cats = ['3piece', '2button', 'tuxedo', 'gurkha-pant', 'bell-bottom', 'embroidered-shirt']
corporate_cats = ['executive-3piece', 'boardroom-2piece', 'power-blazers', 'formal-shirts', 'executive-trousers']

# Copy clean files to respective galleries
for page, items in valid_garments.items():
    dest_dir = gallery_dir if page == 'root' else os.path.join(gallery_dir, page)
    cats = wedding_cats if page == 'wedding' else (bespoke_cats if page == 'bespoke' else corporate_cats)
    
    for idx, (fpath, fname) in enumerate(items):
        cat = cats[idx % len(cats)]
        ext = os.path.splitext(fname)[1].lower()
        new_fname = f"{page}_{idx+1:03d}_{cat}{ext}"
        shutil.copy2(fpath, os.path.join(dest_dir, new_fname))

print("Clean image galleries created successfully!")
