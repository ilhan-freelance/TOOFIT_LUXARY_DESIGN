import os

file_path = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\index.html"
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace hero_mansion_suit_4k.jpg with corporate_tailored_suit.png
updated_content = content.replace('assets/hero_mansion_suit_4k.jpg', 'assets/corporate_tailored_suit.png')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Updated index.html to replace missing hero_mansion_suit_4k.jpg with corporate_tailored_suit.png")
