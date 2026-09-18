import os
import numpy as np
from PIL import Image

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"
toofit_data = os.path.join(base_dir, "Toofit data")

# We want to find the light blue suit (cyan/light blue RGB peak in top half, dark RGB peak in bottom half)
matches = []

for root, dirs, files in os.walk(toofit_data):
    for f in files:
        if not f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp')):
            continue
        path = os.path.join(root, f)
        try:
            img = Image.open(path).convert('RGB')
            w, h = img.size
            # Get average color of top half (jacket region)
            top_half = img.crop((0, 0, w, int(h * 0.5)))
            arr = np.array(top_half)
            r_avg = np.mean(arr[:, :, 0])
            g_avg = np.mean(arr[:, :, 1])
            b_avg = np.mean(arr[:, :, 2])
            
            # Light blue: High B & G, lower/moderate R, B > R + 20
            if b_avg > r_avg + 15 and b_avg > 100:
                print(f"Candidate match: {path} | R:{r_avg:.1f} G:{g_avg:.1f} B:{b_avg:.1f}")
                matches.append(path)
        except Exception as e:
            pass

print(f"\nTotal candidate light blue suit images found: {len(matches)}")
