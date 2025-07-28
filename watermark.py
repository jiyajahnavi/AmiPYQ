import os
import fitz  # PyMuPDF
from PIL import Image

# === CONFIGURATION ===
logo_path = "amipyq_logo.png"
input_folder = "pdfs"
output_folder = "watermarked_pdfs"

# === PREPARE FOLDERS ===
os.makedirs(output_folder, exist_ok=True)

# === RESIZE & ADD TRANSPARENCY TO LOGO ===
logo = Image.open(logo_path).convert("RGBA")  # ensure alpha channel
logo = logo.resize((150, 150))  # Resize to 150x150 px

# Apply 50% transparency
alpha = logo.split()[3]
alpha = alpha.point(lambda p: int(p * 0.5))  # 50% opacity
logo.putalpha(alpha)

# Save transparent logo temporarily
temp_logo_path = "temp_logo.png"
logo.save(temp_logo_path)

# === PROCESS PDFs ===
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_folder, filename)
        doc = fitz.open(pdf_path)

        for page in doc:
            # Get page dimensions
            page_width = page.rect.width
            page_height = page.rect.height

            # Center logo on page
            logo_width = 150
            logo_height = 150
            x = (page_width - logo_width) / 2
            y = (page_height - logo_height) / 2
            rect = fitz.Rect(x, y, x + logo_width, y + logo_height)

            # Add image
            page.insert_image(rect, filename=temp_logo_path, overlay=True)

        # Save output
        output_path = os.path.join(output_folder, filename)
        doc.save(output_path)
        doc.close()
        print(f"✅ Watermarked: {filename}")

# Clean up
os.remove(temp_logo_path)
print("🎉 All PDFs processed and saved in 'watermarked_pdfs'")
