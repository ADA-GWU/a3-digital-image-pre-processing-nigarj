import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import white_tophat, disk, closing, square

def load_images(folder, sample_size=3):
    files = [f for f in os.listdir(folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    selected_files = np.random.choice(files, sample_size, replace=False)
    return [(f, cv2.imread(os.path.join(folder, f), cv2.IMREAD_GRAYSCALE)) for f in selected_files]

def denoise_image(img):
    return cv2.fastNlMeansDenoising(img, None, 30, 7, 21)

def enhance_lines(img):
    """Enhance lines using the best chosen method."""
    inverted = cv2.bitwise_not(img)  # Invert for better edge detection
    
    # Top-Hat transformation
    tophat = white_tophat(inverted, disk(3))
    
    # Canny edge detection
    canny = cv2.Canny(inverted, 50, 150)
    
    # Sobel operator
    sobelx = cv2.Sobel(inverted, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(inverted, cv2.CV_64F, 0, 1, ksize=3)
    sobel_edges = cv2.magnitude(sobelx, sobely)
    sobel_edges = np.uint8(255 * (sobel_edges / np.max(sobel_edges)))
    
    return sobel_edges

def enhance_lines_closing(img):
    """Enhance lines using morphological closing."""
    inverted = cv2.bitwise_not(img)
    closed = closing(inverted, square(3))
    return cv2.bitwise_not(closed)

def process_image(img):
    denoised = denoise_image(img)
    enhanced_edge = enhance_lines(denoised)
    enhanced_closing = enhance_lines_closing(denoised)
    return [
        ("Original", img),
        ("Denoised", denoised),
        ("Enhanced (Closing)", enhanced_closing),
        ("Enhanced (Edge detection)", enhanced_edge)
        
    ]

def show_processed_images(filename, img):
    steps = process_image(img)
    
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    
    for i, (title, image) in enumerate(steps):
        axes[i].imshow(image, cmap='gray')
        axes[i].set_title(title)
        axes[i].axis("off")
    
    plt.suptitle(f"Processing Steps: {filename}")
    plt.show()

def on_image_click(event, images, fig):
    if event.xdata is not None and event.ydata is not None:
        num_images = len(images)
        fig_width = fig.get_size_inches()[0] * fig.dpi
        img_width = fig_width / num_images
        index = int(event.x // img_width)
        
        if 0 <= index < num_images:
            filename, img = images[index]
            plt.close(fig)
            show_processed_images(filename, img)

def show_initial_selection(images):
    fig, axes = plt.subplots(1, len(images), figsize=(9, 4))
    
    for i, (filename, img) in enumerate(images):
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(f"Image {i+1}", fontsize=10)
        axes[i].axis("off")
    
    plt.figtext(0.5, 0.01, "Click on an image to proceed", ha="center", fontsize=10)
    fig.canvas.mpl_connect('button_press_event', lambda event: on_image_click(event, images, fig))
    plt.show()

def main():
    images = load_images("noisy/chemical")
    show_initial_selection(images)

if __name__ == "__main__":
    main()
