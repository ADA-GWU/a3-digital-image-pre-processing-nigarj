import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology

def load_images(folder, sample_size=3):
    """Load 3 random images from a folder."""
    files = [f for f in os.listdir(folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    selected_files = np.random.choice(files, sample_size, replace=False)
    return [(f, cv2.imread(os.path.join(folder, f), cv2.IMREAD_GRAYSCALE)) for f in selected_files]

def preprocess_image(img):
    """Ensure foreground is white and background is black."""
    if np.mean(img) > 127:  # If background is white, invert it
        img = cv2.bitwise_not(img)
    return img

def apply_erosion(img, kernel_size):
    return morphology.erosion(img, morphology.square(kernel_size))

def apply_dilation(img, kernel_size):
    return morphology.dilation(img, morphology.square(kernel_size))

def apply_opening(img, kernel_size):
    return morphology.opening(img, morphology.square(kernel_size))

def apply_closing(img, kernel_size):
    return morphology.closing(img, morphology.square(kernel_size))

def show_processed_images(filename, img):
    """Display all transformations with kernel sizes from 1 to 5 in a compact grid."""
    
    img = preprocess_image(img)  # Ensure correct foreground/background

    fig, axes = plt.subplots(4, 5, figsize=(10, 8))  # Compact figure

    transformations = [
        ('Erosion', apply_erosion),
        ('Dilation', apply_dilation),
        ('Opening', apply_opening),
        ('Closing', apply_closing)
    ]
    
    for row, (title, transform) in enumerate(transformations):
        for col, kernel_size in enumerate(range(1, 6)):  # Kernel sizes from 1 to 5
            result = transform(img, kernel_size)
            axes[row, col].imshow(result, cmap='gray')
            axes[row, col].set_title(f"{title}\nK={kernel_size}", fontsize=9)
            axes[row, col].axis("off")
    
    plt.subplots_adjust(hspace=0.3, wspace=0.2)  # Reduce spacing
    plt.suptitle(f"Image: {filename}", fontsize=12, y=0.98)
    plt.show()

def on_image_click(event, images, fig):
    """Identify the clicked image and process it."""
    if event.xdata is not None and event.ydata is not None:
        num_images = len(images)
        fig_width = fig.get_size_inches()[0] * fig.dpi  # Get figure width in pixels
        img_width = fig_width / num_images  # Approximate width of each image

        index = int(event.x // img_width)  

        if 0 <= index < num_images:
            filename, img = images[index]
            plt.close(fig)
            show_processed_images(filename, img)

def show_initial_selection(images):
    """Display initial selection window with 3 random images side by side."""
    fig, axes = plt.subplots(1, len(images), figsize=(9, 4))  # Smaller selection window

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
