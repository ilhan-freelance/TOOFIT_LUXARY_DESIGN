import os
import re

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

files = ['index.html', 'bespoke.html', 'wedding.html', 'corporate.html']

missing_images = []

for fname in files:
    fpath = os.path.join(base_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
        # Find src=" assets/... " and url('assets/...')
        img_srcs = re.findall(r'src=["\']([^"\']+)["\']', content)
        bg_urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', content)
        
        all_paths = img_srcs + bg_urls
        
        for path in set(all_paths):
            if path.startswith('http') or path.startswith('data:'):
                continue
            
            # Local file path check
            full_path = os.path.join(base_dir, path.replace('/', os.sep))
            if not os.path.exists(full_path):
                print(f"MISSING IMAGE in {fname}: '{path}'")
                missing_images.append((fname, path))

print(f"\nFound {len(missing_images)} missing image references.")
