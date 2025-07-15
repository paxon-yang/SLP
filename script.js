// Document viewer application
class DocumentViewer {
    constructor() {
        this.images = [];
        this.currentImageIndex = 0;
        this.viewMode = 'grid'; // 'grid' or 'single'
        this.init();
    }

    // Initialize the application
    init() {
        this.generateImageList();
        this.bindEvents();
        this.loadImages();
    }

    // Generate list of image filenames
    generateImageList() {
        // Generate array of image filenames based on the pattern
        for (let i = 1; i <= 78; i++) {
            const paddedNumber = i.toString().padStart(2, '0');
            this.images.push({
                filename: `compressed_images/2_CamScanner 06-10-2025 08.32_页面_${paddedNumber}.jpg`,
                title: `Page ${i}`,
                pageNumber: i
            });
        }
    }

    // Bind event listeners
    bindEvents() {
        // Download PDF button
        document.getElementById('downloadPdf').addEventListener('click', () => {
            this.downloadAsPDF();
        });

        // View mode toggle
        document.getElementById('viewMode').addEventListener('click', () => {
            this.toggleViewMode();
        });

        // Image viewer controls
        document.getElementById('closeViewer').addEventListener('click', () => {
            this.closeImageViewer();
        });

        document.getElementById('prevPage').addEventListener('click', () => {
            this.navigateImage(-1);
        });

        document.getElementById('nextPage').addEventListener('click', () => {
            this.navigateImage(1);
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (document.getElementById('imageViewer').style.display !== 'none') {
                switch(e.key) {
                    case 'Escape':
                        this.closeImageViewer();
                        break;
                    case 'ArrowLeft':
                        this.navigateImage(-1);
                        break;
                    case 'ArrowRight':
                        this.navigateImage(1);
                        break;
                }
            }
        });
    }

    // Load and display images
    async loadImages() {
        const imageGrid = document.getElementById('imageGrid');
        const loading = document.getElementById('loading');
        
        try {
            // Create image cards
            this.images.forEach((image, index) => {
                const card = this.createImageCard(image, index);
                imageGrid.appendChild(card);
            });

            // Hide loading spinner
            loading.style.display = 'none';
            imageGrid.style.display = 'grid';

        } catch (error) {
            console.error('Error loading images:', error);
            loading.innerHTML = `
                <div class="error">
                    <h3>⚠️ Error Loading Images</h3>
                    <p>Please make sure all image files are in the same directory as this HTML file.</p>
                </div>
            `;
        }
    }

    // Create image card element
    createImageCard(image, index) {
        const card = document.createElement('div');
        card.className = 'image-card';
        card.addEventListener('click', () => this.openImageViewer(index));

        card.innerHTML = `
            <img src="${image.filename}" alt="${image.title}" loading="lazy" 
                 onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjhmOWZhIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzZjNzU3ZCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIE5vdCBGb3VuZDwvdGV4dD48L3N2Zz4='">
            <div class="image-info">
                <div class="image-title">${image.title}</div>
                <div class="image-meta">Document Page ${image.pageNumber}</div>
            </div>
        `;

        return card;
    }

    // Open image viewer modal
    openImageViewer(index) {
        this.currentImageIndex = index;
        const viewer = document.getElementById('imageViewer');
        const viewerImage = document.getElementById('viewerImage');
        const currentPage = document.getElementById('currentPage');
        
        viewerImage.src = this.images[index].filename;
        viewerImage.alt = this.images[index].title;
        currentPage.textContent = index + 1;
        
        viewer.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        this.updateNavigationButtons();
    }

    // Close image viewer modal
    closeImageViewer() {
        const viewer = document.getElementById('imageViewer');
        viewer.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Navigate between images
    navigateImage(direction) {
        this.currentImageIndex += direction;
        
        if (this.currentImageIndex < 0) {
            this.currentImageIndex = this.images.length - 1;
        } else if (this.currentImageIndex >= this.images.length) {
            this.currentImageIndex = 0;
        }
        
        this.openImageViewer(this.currentImageIndex);
    }

    // Update navigation button states
    updateNavigationButtons() {
        const prevBtn = document.getElementById('prevPage');
        const nextBtn = document.getElementById('nextPage');
        
        prevBtn.disabled = this.currentImageIndex === 0;
        nextBtn.disabled = this.currentImageIndex === this.images.length - 1;
    }

    // Toggle view mode (future feature)
    toggleViewMode() {
        if (this.viewMode === 'grid') {
            this.viewMode = 'list';
            document.getElementById('viewMode').innerHTML = '🔄 Grid View';
            // Could implement list view here
        } else {
            this.viewMode = 'grid';
            document.getElementById('viewMode').innerHTML = '🔄 List View';
        }
    }

    // Download all images as PDF
    async downloadAsPDF() {
        const downloadBtn = document.getElementById('downloadPdf');
        const originalText = downloadBtn.innerHTML;
        
        try {
            // Show loading state
            downloadBtn.innerHTML = '⏳ Generating PDF...';
            downloadBtn.disabled = true;

            // Create new jsPDF instance
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF();
            
            // Process each image
            for (let i = 0; i < this.images.length; i++) {
                const image = this.images[i];
                
                try {
                    // Update progress
                    downloadBtn.innerHTML = `⏳ Processing page ${i + 1}/${this.images.length}...`;
                    
                    // Load image
                    const imgData = await this.loadImageAsDataURL(image.filename);
                    
                    // Add new page (except for first image)
                    if (i > 0) {
                        pdf.addPage();
                    }
                    
                    // Calculate image dimensions to fit page
                    const pageWidth = pdf.internal.pageSize.getWidth();
                    const pageHeight = pdf.internal.pageSize.getHeight();
                    const margin = 10;
                    
                    // Create temporary image to get dimensions
                    const tempImg = new Image();
                    await new Promise((resolve) => {
                        tempImg.onload = resolve;
                        tempImg.src = imgData;
                    });
                    
                    const imgWidth = tempImg.width;
                    const imgHeight = tempImg.height;
                    const ratio = Math.min(
                        (pageWidth - 2 * margin) / imgWidth,
                        (pageHeight - 2 * margin) / imgHeight
                    );
                    
                    const finalWidth = imgWidth * ratio;
                    const finalHeight = imgHeight * ratio;
                    const x = (pageWidth - finalWidth) / 2;
                    const y = (pageHeight - finalHeight) / 2;
                    
                    // Add image to PDF
                    pdf.addImage(imgData, 'PNG', x, y, finalWidth, finalHeight);
                    
                } catch (error) {
                    console.warn(`Failed to process image ${i + 1}:`, error);
                    // Add placeholder page
                    if (i > 0) pdf.addPage();
                    pdf.text(`Page ${i + 1} - Image not available`, 20, 20);
                }
                
                // Small delay to prevent browser freezing
                await new Promise(resolve => setTimeout(resolve, 10));
            }
            
            // Generate filename with current date
            const date = new Date().toISOString().split('T')[0];
            const filename = `document-pages-${date}.pdf`;
            
            // Save PDF
            pdf.save(filename);
            
            // Show success message
            downloadBtn.innerHTML = '✅ Download Complete!';
            setTimeout(() => {
                downloadBtn.innerHTML = originalText;
                downloadBtn.disabled = false;
            }, 2000);
            
        } catch (error) {
            console.error('Error generating PDF:', error);
            downloadBtn.innerHTML = '❌ Download Failed';
            setTimeout(() => {
                downloadBtn.innerHTML = originalText;
                downloadBtn.disabled = false;
            }, 2000);
        }
    }

    // Load image as data URL
    loadImageAsDataURL(filename) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.crossOrigin = 'anonymous';
            
            img.onload = function() {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                
                canvas.width = img.width;
                canvas.height = img.height;
                
                ctx.drawImage(img, 0, 0);
                
                try {
                    const dataURL = canvas.toDataURL('image/png');
                    resolve(dataURL);
                } catch (error) {
                    reject(error);
                }
            };
            
            img.onerror = () => {
                reject(new Error(`Failed to load image: ${filename}`));
            };
            
            img.src = filename;
        });
    }
}

// Initialize the document viewer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DocumentViewer();
});

// Service Worker registration for offline capability (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
} 