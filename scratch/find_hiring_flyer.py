import os
import pytesseract
from PIL import Image

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

found_files = []

for root, dirs, files in os.walk(base_dir):
    # Skip .git directory
    if '.git' in root:
        continue
    for fname in files:
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            fpath = os.path.join(root, fname)
            try:
                with Image.open(fpath) as img:
                    # OCR check for HIRING or 8619297045
                    text = pytesseract.image_to_string(img.convert('RGB')).upper()
                    if 'HIRING' in text or '8619297045' in text or 'BUSINESS DEVELOPMENT' in text:
                        print(f"FOUND HIRING FLYER: {fpath}")
                        found_files.append(fpath)
            except Exception as e:
                pass

print(f"Total hiring flyers found: {len(found_files)}")
