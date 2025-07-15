#!/usr/bin/env python3
"""
Image Compression Script for Document Viewer
Compresses all PNG images to reduce file size for GitHub hosting
"""

import os
import sys
from PIL import Image
import glob

def compress_image(input_path, output_path, quality=85, max_width=1200):
    """
    Compress a single image while maintaining good quality
    
    Args:
        input_path (str): Path to input image
        output_path (str): Path to save compressed image
        quality (int): JPEG quality (1-100), higher is better quality
        max_width (int): Maximum width to resize to
    """
    try:
        with Image.open(input_path) as img:
            # Get original size
            original_size = os.path.getsize(input_path)
            original_width, original_height = img.size
            
            # Calculate new dimensions while maintaining aspect ratio
            if original_width > max_width:
                ratio = max_width / original_width
                new_width = max_width
                new_height = int(original_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"  Resized: {original_width}x{original_height} -> {new_width}x{new_height}")
            
            # Convert to RGB if necessary (for JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Save as optimized JPEG
            img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            
            # Get compressed size
            compressed_size = os.path.getsize(output_path)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            print(f"  Original: {original_size / 1024:.1f} KB")
            print(f"  Compressed: {compressed_size / 1024:.1f} KB")
            print(f"  Saved: {compression_ratio:.1f}%")
            
            return True
            
    except Exception as e:
        print(f"  Error: {e}")
        return False

def compress_all_images():
    """Compress all PNG images in the current directory"""
    
    # Find all PNG files matching the pattern
    png_files = glob.glob("2_CamScanner*.png")
    
    if not png_files:
        print("No PNG files found matching the pattern '2_CamScanner*.png'")
        return
    
    print(f"Found {len(png_files)} images to compress")
    print("=" * 50)
    
    # Create compressed directory
    compressed_dir = "compressed_images"
    if not os.path.exists(compressed_dir):
        os.makedirs(compressed_dir)
        print(f"Created directory: {compressed_dir}")
    
    total_original = 0
    total_compressed = 0
    successful = 0
    
    for i, png_file in enumerate(sorted(png_files), 1):
        print(f"\n[{i}/{len(png_files)}] Processing: {png_file}")
        
        # Generate output filename (change extension to .jpg)
        base_name = os.path.splitext(png_file)[0]
        output_file = os.path.join(compressed_dir, f"{base_name}.jpg")
        
        # Get original size
        original_size = os.path.getsize(png_file)
        total_original += original_size
        
        # Compress image
        if compress_image(png_file, output_file):
            compressed_size = os.path.getsize(output_file)
            total_compressed += compressed_size
            successful += 1
        else:
            print(f"  Failed to compress {png_file}")
    
    print("\n" + "=" * 50)
    print("COMPRESSION SUMMARY")
    print("=" * 50)
    print(f"Successfully compressed: {successful}/{len(png_files)} images")
    print(f"Total original size: {total_original / (1024*1024):.1f} MB")
    print(f"Total compressed size: {total_compressed / (1024*1024):.1f} MB")
    
    if total_original > 0:
        total_savings = (1 - total_compressed / total_original) * 100
        print(f"Total space saved: {total_savings:.1f}%")
        print(f"Space saved: {(total_original - total_compressed) / (1024*1024):.1f} MB")

def update_html_for_compressed_images():
    """Update the HTML and JS files to use compressed JPG images"""
    
    print("\n" + "=" * 50)
    print("UPDATING FILES FOR COMPRESSED IMAGES")
    print("=" * 50)
    
    # Update script.js
    try:
        with open('script.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the file extension and path
        updated_content = content.replace(
            '`2_CamScanner 06-10-2025 08.32_页面_${paddedNumber}.png`',
            '`compressed_images/2_CamScanner 06-10-2025 08.32_页面_${paddedNumber}.jpg`'
        )
        
        with open('script.js', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("Updated script.js to use compressed images")
        
    except Exception as e:
        print(f"Error updating script.js: {e}")

if __name__ == "__main__":
    print("Document Viewer - Image Compression Tool")
    print("=" * 50)
    
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow library not found!")
        print("Please install it using: pip install Pillow")
        sys.exit(1)
    
    # Compress images
    compress_all_images()
    
    # Update files to use compressed images
    update_html_for_compressed_images()
    
    print("\nCompression complete!")
    print("\nNext steps:")
    print("1. Delete original PNG files if satisfied with compression")
    print("2. Test the website with compressed images")
    print("3. Upload to GitHub") 