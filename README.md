# Document Viewer

A modern web application for viewing scanned document pages and downloading them as PDF.

## Features

- **📄 View All Pages**: Display all 78 scanned document pages in a responsive grid layout
- **🔍 Full Screen Viewer**: Click any page to view it in full screen with navigation controls
- **📥 PDF Download**: Download all pages as a single PDF file with one click
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **⌨️ Keyboard Navigation**: Use arrow keys and Escape key for easy navigation
- **🎨 Modern UI**: Beautiful, clean interface with smooth animations

## How to Use

### Option 1: Local Usage
1. **Open the Website**: Open `index.html` in any modern web browser
2. **View Pages**: 
   - Browse all document pages in the grid view
   - Click any page thumbnail to open full-screen viewer
   - Use arrow keys or navigation buttons to browse pages
   - Press Escape to close the full-screen viewer
3. **Download PDF**: Click the "📥 Download as PDF" button to generate and download a PDF containing all pages

### Option 2: GitHub Pages (Recommended)
1. Fork or clone this repository
2. Enable GitHub Pages in repository settings
3. Access your site at `https://yourusername.github.io/repository-name`

## Image Compression (For GitHub Upload)

Before uploading to GitHub, compress the images to reduce repository size:

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the compression script**:
   ```bash
   python compress_images.py
   ```

3. **What the script does**:
   - Compresses all PNG images to optimized JPEG format
   - Reduces file size by 60-80% while maintaining quality
   - Updates the website code to use compressed images
   - Creates a `compressed_images/` folder

## File Structure

```
wangye2/
├── index.html              # Main HTML file
├── style.css              # CSS styles
├── script.js              # JavaScript functionality
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── compress_images.py     # Image compression script
├── deploy_to_github.py    # One-click deployment script
├── .gitignore            # Git ignore file
├── .github/workflows/    # GitHub Actions
│   └── deploy.yml        # Auto-deployment config
├── compressed_images/    # Compressed images (created after running script)
│   └── 2_CamScanner...  # Compressed image files (78 pages)
└── 2_CamScanner...      # Original images (ignored by git)
```

## Browser Requirements

- Modern web browser with JavaScript enabled
- Support for ES6+ features
- Canvas API support for PDF generation

## Technical Features

- **Lazy Loading**: Images load as needed for better performance
- **Error Handling**: Graceful fallback when images fail to load
- **Progress Tracking**: Real-time progress during PDF generation
- **Memory Efficient**: Optimized image processing to prevent browser crashes
- **Cross-Origin Safe**: Handles image loading without CORS issues

## Keyboard Shortcuts

- `←` / `→` Arrow Keys: Navigate between pages in full-screen mode
- `Escape`: Close full-screen viewer

## Mobile Support

The website is fully responsive and includes:
- Touch-friendly buttons and controls
- Optimized layouts for small screens
- Swipe gestures for navigation (via touch-friendly buttons)

## PDF Generation

The PDF download feature:
- Maintains original image quality
- Automatically fits pages to PDF format
- Includes all 78 pages in correct order
- Downloads with timestamp in filename
- Shows progress during generation

## Troubleshooting

If images don't load:
1. Ensure all image files are in the same directory as `index.html`
2. Check that image filenames match exactly (case-sensitive)
3. Make sure your browser allows local file access

If PDF download fails:
1. Try with fewer pages first to test
2. Ensure sufficient browser memory
3. Check browser console for error messages

## Deployment to GitHub

### 🚀 Quick Deploy (Recommended)
For one-click deployment with automatic image compression:

```bash
python deploy_to_github.py
```

This script will:
- ✅ Check all requirements (Git, Python, Pillow)
- 📷 Compress all images automatically
- 🔧 Set up Git repository
- 🚀 Push to GitHub with your credentials
- 📋 Show final setup instructions

### 📋 Manual Deploy (Alternative)

#### Step 1: Prepare Images
```bash
# Install Python dependencies
pip install -r requirements.txt

# Compress images
python compress_images.py
```

#### Step 2: Create GitHub Repository
1. Create a new repository on GitHub
2. Initialize git in your project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Document viewer with compressed images"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

#### Step 3: Enable GitHub Pages
1. Go to your repository settings on GitHub
2. Scroll down to "Pages" section
3. Under "Source", select "GitHub Actions"
4. The site will automatically deploy when you push changes

#### Step 4: Access Your Site
Your website will be available at: `https://yourusername.github.io/your-repo-name`

## Performance Optimization

- **Image Compression**: JPEG format with 85% quality reduces file size significantly
- **Lazy Loading**: Images load only when needed
- **Progressive Enhancement**: Works even with slow connections
- **CDN Delivery**: GitHub Pages provides global CDN for fast loading

---

**Note**: This is a client-side application that runs entirely in your browser. No data is sent to any server. 