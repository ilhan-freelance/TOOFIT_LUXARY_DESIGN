import os
from update_html_galleries import update_file

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

files_to_delete = [
    # 1. Navy double-breasted suit (AMANIQUEATTIRE)
    os.path.join(base_dir, "Toofit data", "2 piece suit", "download.png"),
    os.path.join(base_dir, "assets", "gallery", "bespoke", "bespoke_20_2button.jpg"),
    
    # 2. Pink striped formal shirt (ITALIAN VEGA)
    os.path.join(base_dir, "Toofit data", "Formal shirts", "197737c5e4deb135aa160780559ee904.jpg"),
    
    # 3. White Jodhpuri suit (VR DESIGNER)
    os.path.join(base_dir, "Toofit data", "Jodhpuri", "90d83ff7b46c102f24df1b6c7b84a689.jpg")
]

print("Deleting target images...")
for fpath in files_to_delete:
    if os.path.exists(fpath):
        try:
            os.remove(fpath)
            print(f"DELETED: {fpath}")
        except Exception as e:
            print(f"Error deleting {fpath}: {e}")
    else:
        print(f"File not found or already deleted: {fpath}")

# Rebuild all 3 page galleries
print("\nRebuilding page HTML galleries...")
update_file('wedding.html', 'wedding', 'wedding', 'wedding')
update_file('bespoke.html', 'bespoke', 'bespoke', 'bespoke')
update_file('corporate.html', 'corporate', 'corporate', 'corporate')
print("All galleries updated successfully!")
