import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'wedding' in line.lower() and ('<img' in line.lower() or 'id=' in line.lower() or 'section' in line.lower() or 'slide' in line.lower()):
        print(f"Line {i+1}: {line.strip()[:120]}")
