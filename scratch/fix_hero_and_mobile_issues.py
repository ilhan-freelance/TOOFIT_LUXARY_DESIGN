import os
import shutil

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"
assets_dir = os.path.join(base_dir, "assets")

# 1. Restore Slide 3 Model Image (Copy hero_corporate_banner.jpg to hero_mansion_suit_4k.jpg)
src_img = os.path.join(assets_dir, "hero_corporate_banner.jpg")
dest_img = os.path.join(assets_dir, "hero_mansion_suit_4k.jpg")

if os.path.exists(src_img):
    shutil.copy2(src_img, dest_img)
    print("Copied hero_corporate_banner.jpg to hero_mansion_suit_4k.jpg successfully!")

# 2. Fix Navbar overflow on mobile across all HTML files
html_files = ['index.html', 'wedding.html', 'bespoke.html', 'corporate.html', 'defined_by_style.html', 'styled_by_toofit.html', 'client_diaries.html']

for fname in html_files:
    fpath = os.path.join(base_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace <div class="tf-nav-row flex... with <div class="tf-nav-row hidden md:flex...
    content = content.replace(
        'class="tf-nav-row flex justify-center items-center w-full text-center"',
        'class="tf-nav-row hidden md:flex justify-center items-center w-full text-center"'
    )
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed mobile navbar for {fname}")

print("Done updating navbar and hero slide image.")
