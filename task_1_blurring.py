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

def apply_blur(img):
    """Apply Gaussian blur to reduce noise before closing."""
    return cv2.GaussianBlur(img, (3, 3), 0)

def apply_closing(img, kernel_size):
    return morphology.closing(img, morphology.square(kernel_size))

def save_processed_images(filename, img, output_folder):
    """Save the processed images after closing."""
    img = preprocess_image(img)  # Ensure correct foreground/background
    blurred = apply_blur(img)  # Apply blurring before closing
    closing_k2 = apply_closing(blurred, 2)
    closing_k3 = apply_closing(blurred, 3)
    
    # Prepare the figure
    fig, axes = plt.subplots(1, 3, figsize=(12, 5))
    images = [("Original", img), ("Closing K=2", closing_k2), ("Closing K=3", closing_k3)]
    
    for ax, (title, image) in zip(axes, images):
        ax.imshow(image, cmap='gray')
        ax.set_title(title)
        ax.axis("off")
    
    plt.suptitle(f"Image: {filename}", fontsize=12)
    
    # Save the figure to the specified folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, f"{filename}_processed.png")
    plt.savefig(output_path)
    plt.close(fig)

def on_image_click(event, images, fig, output_folder):
    """Identify the clicked image and process it."""
    if event.xdata is not None and event.ydata is not None:
        num_images = len(images)
        fig_width = fig.get_size_inches()[0] * fig.dpi  
        img_width = fig_width / num_images 

        index = int(event.x // img_width)  

        if 0 <= index < num_images:
            filename, img = images[index]
            plt.close(fig)
            show_processed_images(filename, img, output_folder)

def show_processed_images(filename, img, output_folder):
    """Show processed images and save after closing."""
    img = preprocess_image(img)  # Ensure correct foreground/background
    blurred = apply_blur(img)  # Apply blurring before closing
    closing_k2 = apply_closing(blurred, 2)
    closing_k3 = apply_closing(blurred, 3)
    
    # Prepare the figure
    fig, axes = plt.subplots(1, 3, figsize=(12, 5))
    images = [("Original", img), ("Closing K=2", closing_k2), ("Closing K=3", closing_k3)]
    
    for ax, (title, image) in zip(axes, images):
        ax.imshow(image, cmap='gray')
        ax.set_title(title)
        ax.axis("off")
    
    plt.suptitle(f"Image: {filename}", fontsize=12)
    
    # Connect the close event to save the image once the window is closed
    def on_close(event):
        save_processed_images(filename, img, output_folder)
    
    fig.canvas.mpl_connect('close_event', on_close)
    
    plt.show()

def show_initial_selection(images, output_folder):
    """Display initial selection window with 3 random images side by side."""
    fig, axes = plt.subplots(1, len(images), figsize=(9, 4))  

    for i, (filename, img) in enumerate(images):
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(f"Image {i+1}", fontsize=10)
        axes[i].axis("off")

    plt.figtext(0.5, 0.01, "Click on an image to proceed", ha="center", fontsize=10)
    fig.canvas.mpl_connect('button_press_event', lambda event: on_image_click(event, images, fig, output_folder))
    plt.show()

def main():
    images = load_images("noisy/chemical")
    output_folder = "output_task_1"
    show_initial_selection(images, output_folder)

if __name__ == "__main__":
    main()