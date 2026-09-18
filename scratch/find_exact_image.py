import os
import numpy as np
from PIL import Image

f1 = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\Toofit data\2 piece suit\1c9e6fbd6958a0c672a4f69216ce1d59.jpg"
f2 = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\Toofit data\2 piece suit\1cfdac64a0ed03c074ac03413d856e9d.jpg"

for path in [f1, f2]:
    img = Image.open(path).convert('RGB')
    w, h = img.size
    # Check middle section (chest/buttons area)
    chest = img.crop((int(w*0.3), int(h*0.2), int(w*0.7), int(h*0.5)))
    arr = np.array(chest)
    # Light blue jacket color: R~150-180, G~190-220, B~220-255
    r_med = np.median(arr[:, :, 0])
    g_med = np.median(arr[:, :, 1])
    b_med = np.median(arr[:, :, 2])
    print(f"{os.path.basename(path)} -> Chest color median: R={r_med}, G={g_med}, B={b_med}")

