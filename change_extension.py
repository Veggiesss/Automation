#Made to change one extension of all files in one folder to another, the process is to take one file with extension a, create a copy, change the copy's extension to b, then remove the original
#Made for organization, although it is quite slow (~ 5seconds per file)
#Made on June 14, 2025

import os
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image

load_dotenv()

# 🔧 Configuration
folder = Path(os.getenv("RENAME_PATH"))  # Set your target folder here

def convert_images():
    from_ext = input("🔍 Enter the extension you want to convert from (e.g., png): ").strip().lower().lstrip('.')
    to_ext = input("🎯 Enter the extension you want to convert to (e.g., webp): ").strip().lower().lstrip('.')

    if from_ext == to_ext:
        print("⚠️ Source and target extensions are the same. Nothing to do.")
        return

    files = list(folder.glob(f"*.{from_ext}"))
    if not files:
        print(f"❌ No .{from_ext} files found.")
        return

    for f in files:
        target_file = f.with_suffix(f".{to_ext}")
        try:
            img = Image.open(f).convert("RGBA")  # Ensures transparency is preserved
            img.save(target_file, to_ext, quality=90)
            print(f"✅ Converted: {f.name} → {target_file.name}")

            # Delete original file
            f.unlink()
            print(f"🗑️ Deleted original: {f.name}")

        except Exception as e:
            print(f"⚠️ Failed to convert {f.name}: {e}")

    print("🏁 Conversion complete.")

if __name__ == "__main__":
    convert_images()
