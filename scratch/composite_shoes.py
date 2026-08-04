import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw

def perfect_positioning():
    # 1. Load clean mannequin base (or rebuild)
    raw_mannequin = Image.open('assets/mannequin_formal_suit_transparent.png').convert('RGBA')
    mw, mh = raw_mannequin.size
    
    # Reload pure shoe
    pure_shoe = Image.open('scratch/pure_shoe_flawless.png').convert('RGBA')
    
    # Clear out any residual bottom pixels below y=835
    man_arr = np.array(raw_mannequin)
    for y in range(835, mh):
        for x in range(mw):
            man_arr[y, x, 3] = 0

    clean_mannequin = Image.fromarray(man_arr)
    
    # 2. Resize and Position Shoes cleanly under mannequin stand feet
    left_shoe = pure_shoe.resize((124, 62), Image.Resampling.LANCZOS)
    right_shoe = ImageOps.mirror(left_shoe)
    
    final_canvas = Image.new('RGBA', (mw, mh), (0, 0, 0, 0))
    
    # Realistic soft ground shadows under the shoes
    shadow = Image.new('RGBA', (mw, mh), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([210, 850, 335, 878], fill=(0, 0, 0, 150))
    s_draw.ellipse([315, 850, 440, 878], fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(5))
    
    # Layer order:
    # 1. Left Shoe (x=215, y=815)
    # 2. Right Shoe (x=318, y=815)
    # 3. Ground Shadow
    # 4. Clean Mannequin (so wooden tripod stand sits naturally over the heel/shoe base)
    
    # Create shoe layer
    shoe_layer = Image.new('RGBA', (mw, mh), (0, 0, 0, 0))
    shoe_layer.paste(left_shoe, (215, 815), left_shoe)
    shoe_layer.paste(right_shoe, (318, 815), right_shoe)
    
    # Composite: Shadow -> Shoes -> Mannequin
    final_canvas = Image.alpha_composite(final_canvas, shadow)
    final_canvas = Image.alpha_composite(final_canvas, shoe_layer)
    final_canvas = Image.alpha_composite(final_canvas, clean_mannequin)
    
    # Save output to assets and scratch
    final_canvas.save('assets/mannequin_formal_suit_transparent.png')
    final_canvas.save('scratch/perfect_seamless_result.png')
    print("Perfect seamless formal shoes updated!")

if __name__ == '__main__':
    perfect_positioning()
