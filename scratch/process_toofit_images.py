import os
import shutil
import glob

# Paths
base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"
toofit_data_dir = os.path.join(base_dir, "Toofit data")

wedding_src = os.path.join(toofit_data_dir, "Wedding 1")
folder_a_src = os.path.join(toofit_data_dir, "202609_a")
folder_b_src = os.path.join(toofit_data_dir, "202609_b")

assets_gallery_dir = os.path.join(base_dir, "assets", "gallery")
wedding_dest = os.path.join(assets_gallery_dir, "wedding")
bespoke_dest = os.path.join(assets_gallery_dir, "bespoke")
corporate_dest = os.path.join(assets_gallery_dir, "corporate")

for d in [wedding_dest, bespoke_dest, corporate_dest]:
    os.makedirs(d, exist_ok=True)

print("Organizing images from Toofit data...")

# 1. Process Wedding 1 images (103 images)
wedding_files = sorted([f for f in os.listdir(wedding_src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
wedding_cats = [
    'sherwanis', 'jodhpuris', 'designer-coat', 'wedding-wear', 
    'engagement', 'haldi-mehndi', 'indo-western', 'hand-painted-shirt'
]

wedding_items = []
for idx, fname in enumerate(wedding_files):
    cat = wedding_cats[idx % len(wedding_cats)]
    src_path = os.path.join(wedding_src, fname)
    new_fname = f"wedding_{idx+1:03d}_{cat}{os.path.splitext(fname)[1].lower()}"
    dest_path = os.path.join(wedding_dest, new_fname)
    shutil.copy2(src_path, dest_path)
    rel_path = f"assets/gallery/wedding/{new_fname}"
    wedding_items.append({
        'src': rel_path,
        'category': cat,
        'filename': fname,
        'index': idx + 1
    })

print(f"Copied {len(wedding_items)} wedding images.")

# 2. Process 202609_a & 202609_b images for Bespoke and Corporate
suit_files = sorted([f for f in os.listdir(folder_a_src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
b_files = sorted([f for f in os.listdir(folder_b_src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
all_suit_files = suit_files + b_files

bespoke_cats = ['3piece', '2button', 'tuxedo', 'gurkha-pant', 'bell-bottom', 'embroidered-shirt']
corporate_cats = ['executive-3piece', 'boardroom-2piece', 'power-blazers', 'formal-shirts', 'executive-trousers']

bespoke_items = []
corporate_items = []

# Distribute images: first 200 to Bespoke, rest to Corporate
for idx, fname in enumerate(all_suit_files):
    src_dir = folder_a_src if idx < len(suit_files) else folder_b_src
    src_path = os.path.join(src_dir, fname)
    
    if idx % 2 == 0:
        cat = bespoke_cats[(idx // 2) % len(bespoke_cats)]
        new_fname = f"bespoke_{len(bespoke_items)+1:03d}_{cat}{os.path.splitext(fname)[1].lower()}"
        dest_path = os.path.join(bespoke_dest, new_fname)
        shutil.copy2(src_path, dest_path)
        rel_path = f"assets/gallery/bespoke/{new_fname}"
        bespoke_items.append({
            'src': rel_path,
            'category': cat,
            'filename': fname
        })
    else:
        cat = corporate_cats[(idx // 2) % len(corporate_cats)]
        new_fname = f"corporate_{len(corporate_items)+1:03d}_{cat}{os.path.splitext(fname)[1].lower()}"
        dest_path = os.path.join(corporate_dest, new_fname)
        shutil.copy2(src_path, dest_path)
        rel_path = f"assets/gallery/corporate/{new_fname}"
        corporate_items.append({
            'src': rel_path,
            'category': cat,
            'filename': fname
        })

print(f"Copied {len(bespoke_items)} bespoke images and {len(corporate_items)} corporate images.")
