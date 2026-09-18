import os

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"
file_to_remove = os.path.join(base_dir, "Toofit data", "2 piece suit", "1c9e6fbd6958a0c672a4f69216ce1d59.jpg")

if os.path.exists(file_to_remove):
    os.remove(file_to_remove)
    print(f"Removed target image from Toofit data: {file_to_remove}")
else:
    print("File not found or already removed.")
