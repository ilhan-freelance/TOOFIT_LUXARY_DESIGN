import os
from PIL import Image
import pytesseract

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

print("Scanning all image files for matches...")

matches = []

for root, dirs, files in os.walk(base_dir):
    if '.git' in root or 'scratch' in root:
        continue
    for fname in sorted(files):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        fpath = os.path.join(root, fname)
        
        try:
            with Image.open(fpath) as img:
                w, h = img.size
                rgb = img.convert('RGB')
                
                # Run OCR to detect watermarks or text
                text = ""
                try:
                    text = pytesseract.image_to_string(rgb).upper()
                except Exception:
                    pass
                
                # Check keywords
                reasons = []
                if "AMANI" in text or "QUEATTIRE" in text or "AMANIQUE" in text:
                    reasons.append("OCR AMANIQUEATTIRE (Navy double breasted suit)")
                if "ITALIAN" in text or "VEGA" in text or "TALIAN" in text:
                    reasons.append("OCR ITALIAN VEGA (Pink striped shirt)")
                if "VR" in text or "DESIGNER" in text or "DESIG" in text:
                    # Let's verify if white suit with VR background
                    reasons.append("OCR VR DESIGNER (White jodhpuri suit)")
                
                # Also check color distribution / feature check
                # Navy suit + grey pants (Image 1)
                # Pink striped shirt + tan pants (Image 2)
                # All-white suit + brown/gold background (Image 3)
                
                if reasons or ("VR" in fname.upper() or "AMANI" in fname.upper()):
                    matches.append((fpath, text.strip().replace('\n', ' '), reasons))
                else:
                    # Print any text found for inspection if suspicious
                    if any(k in text for k in ["AMANI", "VEGA", "ITALIAN", "VR"]):
                        matches.append((fpath, text.strip().replace('\n', ' '), ["Keyword substring match"]))
                        
        except Exception as e:
            pass

print(f"\nFound {len(matches)} potential OCR matches:")
for m in matches:
    print(f"File: {m[0]}")
    print(f"Reasons: {m[2]}")
    print(f"OCR snippet: {m[1][:100]}")
    print("-" * 50)
