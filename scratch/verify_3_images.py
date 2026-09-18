import os
from PIL import Image

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

test_files = [
    # Image 1 (Navy suit + grey pants)
    os.path.join(base_dir, "Toofit data", "2 piece suit", "download.png"),
    os.path.join(base_dir, "assets", "gallery", "bespoke", "bespoke_20_2button.jpg"),
    
    # Image 2 (Pink striped shirt + tan pants)
    os.path.join(base_dir, "Toofit data", "Formal shirts", "197737c5e4deb135aa160780559ee904.jpg"),
    
    # Image 3 (White Jodhpuri VR background)
    os.path.join(base_dir, "Toofit data", "Jodhpuri", "90d83ff7b46c102f24df1b6c7b84a689.jpg"),
    os.path.join(base_dir, "Toofit data", "Jodhpuri", "6dce5fb7acb985d9e31f99e0d9730ac1.jpg"),
]

for tf in test_files:
    if os.path.exists(tf):
        with Image.open(tf) as img:
            print(f"EXIST: {tf} -> Size: {img.size}, Mode: {img.mode}")
    else:
        print(f"NOT FOUND: {tf}")
