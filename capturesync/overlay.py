import os
from PIL import Image, ImageOps

def process_image(image_path, landscape_overlay_path, portrait_overlay_path, output_folder):
    """
    Reads image, detects orientation, applies appropriate overlay, and saves to output_folder.
    Returns the path to the saved file if successful, None otherwise.
    """
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Fix EXIF orientation (crucial for looking right)
            img = ImageOps.exif_transpose(img)
            
            # Determine orientation
            width, height = img.size
            if width > height:
                orientation = 'landscape'
                overlay_path = landscape_overlay_path
            else:
                orientation = 'portrait'
                overlay_path = portrait_overlay_path
            
            # Open the selected overlay
            if not os.path.exists(overlay_path):
                print(f"Error: Overlay not found at {overlay_path}")
                return None
                
            with Image.open(overlay_path) as overlay:
                # Resize overlay to match image dimensions exactly
                # Using LANCZOS for high quality downscaling/upscaling
                overlay_resized = overlay.resize((width, height), Image.Resampling.LANCZOS)
                
                # Ensure we are working in RGBA to handle transparency correctly
                img = img.convert("RGBA")
                overlay_resized = overlay_resized.convert("RGBA")
                
                # Apply overlay
                img.alpha_composite(overlay_resized)
                
                # Prepare output path
                filename = os.path.basename(image_path)
                name, ext = os.path.splitext(filename)
                # Force output to jpg as requested ("Export optimized JPEG")
                output_filename = f"{name}_processed.jpg"
                output_path = os.path.join(output_folder, output_filename)
                
                # Convert back to RGB for JPEG saving
                final_img = img.convert("RGB")
                
                # Save
                final_img.save(output_path, quality=90, optimize=True)
                
                return output_path

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None
