import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology  # For morphological operations

def load_images(folder, sample_size=3):
    """Load a specified number of random images from a folder."""
    files = [f for f in os.listdir(folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    selected_files = np.random.choice(files, sample_size, replace=False)
    return [(f, cv2.imread(os.path.join(folder, f), cv2.IMREAD_GRAYSCALE)) for f in selected_files]

def preprocess_image(img):
    """No preprocessing needed for speckle in most cases."""
    return img

def apply_median_filter(img, kernel_size):
    """Applies a median filter to the image."""
    return cv2.medianBlur(img, kernel_size)

def apply_bilateral_filter(img, kernel_size, sigma_color, sigma_space):
    """Applies a bilateral filter to the image."""
    return cv2.bilateralFilter(img, kernel_size, sigma_color, sigma_space)

def apply_crimmins_speckle_removal(img, iterations=3):
    """Applies the Crimmins speckle removal algorithm."""

    def adjust_dark_pixels(img):
        """Adjusts dark pixels based on neighboring pixels."""
        a = img.astype(np.int16)
        b = a.copy()
        height, width = img.shape[:2]  # Handle grayscale images

        # N-S direction
        c = np.roll(a, -1, axis=0)
        c[0, :] = a[0, :]  # Handle top boundary
        d = np.roll(a, 1, axis=0)
        d[height - 1, :] = a[height - 1, :]  # Handle bottom boundary
        mask = (a < np.minimum(c, d)) & (c != d)
        b[mask] += np.sign(c[mask] - d[mask])

        # E-W direction
        c = np.roll(a, -1, axis=1)
        c[:, 0] = a[:, 0]  # Handle left boundary
        d = np.roll(a, 1, axis=1)
        d[:, width - 1] = a[:, width - 1]  # Handle right boundary
        mask = (a < np.minimum(c, d)) & (c != d)
        b[mask] += np.sign(c[mask] - d[mask])

        # NW-SE direction
        c = np.roll(np.roll(a, -1, axis=0), -1, axis=1)
        c[0, :] = a[0, :]
        c[:, 0] = a[:, 0]
        d = np.roll(np.roll(a, 1, axis=0), 1, axis=1)
        d[height - 1, :] = a[height - 1, :]
        d[:, width - 1] = a[:, width - 1]
        mask = (a < np.minimum(c, d)) & (c != d)
        b[mask] += np.sign(c[mask] - d[mask])

        # NE-SW direction
        c = np.roll(np.roll(a, -1, axis=0), 1, axis=1)
        c[0, :] = a[0, :]
        c[:, width - 1] = a[:, width - 1]
        d = np.roll(np.roll(a, 1, axis=0), -1, axis=1)
        d[height - 1, :] = a[height - 1, :]
        d[:, 0] = a[:, 0]
        mask = (a < np.minimum(c, d)) & (c != d)
        b[mask] += np.sign(c[mask] - d[mask])

        return b.astype(np.uint8)

    def adjust_light_pixels(img):
        """Adjusts light pixels based on neighboring pixels."""
        a = img.astype(np.int16)
        b = a.copy()
        height, width = img.shape[:2]

        # N-S direction
        c = np.roll(a, -1, axis=0)
        c[0, :] = a[0, :]
        d = np.roll(a, 1, axis=0)
        d[height - 1, :] = a[height - 1, :]
        mask = (a > np.maximum(c, d)) & (c != d)
        b[mask] -= np.sign(c[mask] - d[mask])

        # E-W direction
        c = np.roll(a, -1, axis=1)
        c[:, 0] = a[:, 0]
        d = np.roll(a, 1, axis=1)
        d[:, width - 1] = a[:, width - 1]
        mask = (a > np.maximum(c, d)) & (c != d)
        b[mask] -= np.sign(c[mask] - d[mask])

        # NW-SE direction
        c = np.roll(np.roll(a, -1, axis=0), -1, axis=1)
        c[0, :] = a[0, :]
        c[:, 0] = a[:, 0]
        d = np.roll(np.roll(a, 1, axis=0), 1, axis=1)
        d[height - 1, :] = a[height - 1, :]
        d[:, width - 1] = a[:, width - 1]
        mask = (a > np.maximum(c, d)) & (c != d)
        b[mask] -= np.sign(c[mask] - d[mask])

        # NE-SW direction
        c = np.roll(np.roll(a, -1, axis=0), 1, axis=1)
        c[0, :] = a[0, :]
        c[:, width - 1] = a[:, width - 1]
        d = np.roll(np.roll(a, 1, axis=0), -1, axis=1)
        d[height - 1, :] = a[height - 1, :]
        d[:, 0] = a[:, 0]
        mask = (a > np.maximum(c, d)) & (c != d)
        b[mask] -= np.sign(c[mask] - d[mask])

        return b.astype(np.uint8)

    img_adjusted = img.copy()
    for _ in range(iterations):  # Iterations - you can adjust this
        img_adjusted = adjust_dark_pixels(img_adjusted)
        img_adjusted = adjust_light_pixels(img_adjusted)
    return img_adjusted

def apply_opening(img, kernel_size):
    """Applies the opening morphological operation."""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def apply_closing(img, kernel_size):
    """Applies the closing morphological operation."""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

def apply_my_method(img, crimmins_iterations=3, opening_kernel_size=3, closing_kernel_size=3):
    """
    Applies Crimmins speckle removal followed by opening and closing.
    This is 'myMethod'.
    """
    img_crimmins = apply_crimmins_speckle_removal(img, iterations=crimmins_iterations)
    img_opening = apply_opening(img_crimmins, kernel_size=opening_kernel_size)
    img_closing = apply_closing(img_opening, kernel_size=closing_kernel_size)
    return img_closing

def calculate_difference_image(original_img, processed_img):
    """Calculates the difference between two images and normalizes the result for display."""
    diff = original_img.astype(np.int16) - processed_img.astype(np.int16)
    diff = np.abs(diff)
    diff_normalized = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return diff_normalized

def display_results(filename, original_img, processed_median, processed_bilateral, processed_crimmins, processed_mymethod,
                    diff_median, diff_bilateral, diff_crimmins, diff_mymethod):
    """Displays the original image, processed images, and difference images."""

    fig, axes = plt.subplots(2, 5, figsize=(20, 8))  # Adjusted for "myMethod"

    axes[0, 0].imshow(original_img, cmap='gray')
    axes[0, 0].set_title("Original", fontsize=10)
    axes[0, 0].axis("off")

    axes[0, 1].imshow(processed_median, cmap='gray')
    axes[0, 1].set_title("Median Filtered", fontsize=10)
    axes[0, 1].axis("off")

    axes[0, 2].imshow(processed_bilateral, cmap='gray')
    axes[0, 2].set_title("Bilateral Filtered", fontsize=10)
    axes[0, 2].axis("off")

    axes[0, 3].imshow(processed_crimmins, cmap='gray')
    axes[0, 3].set_title("Crimmins Filtered", fontsize=10)
    axes[0, 3].axis("off")

    axes[0, 4].imshow(processed_mymethod, cmap='gray')
    axes[0, 4].set_title("My Method", fontsize=10)
    axes[0, 4].axis("off")
    
    axes[1, 0].imshow(original_img, cmap='gray')
    axes[1, 0].set_title("Original", fontsize=10)
    axes[1, 0].axis("off")

    axes[1, 1].imshow(diff_median, cmap='gray')
    axes[1, 1].set_title("Median Removed", fontsize=10)
    axes[1, 1].axis("off")

    axes[1, 2].imshow(diff_bilateral, cmap='gray')
    axes[1, 2].set_title("Bilateral Removed", fontsize=10)

    axes[1, 3].imshow(diff_crimmins, cmap='gray')
    axes[1, 3].set_title("Crimmins Removed", fontsize=10)

    axes[1, 4].imshow(diff_mymethod, cmap='gray')
    axes[1, 4].set_title("My Method Removed", fontsize=10)



    plt.tight_layout()
    plt.show()

def on_image_click(event, images, fig):
    """Identify the clicked image and process it."""
    if event.xdata is not None and event.ydata is not None:
        num_images = len(images)
        fig_width = fig.get_size_inches()[0] * fig.dpi  # Get figure width in pixels
        img_width = fig_width / num_images

        index = int(event.x // img_width)

        if 0 <= index < num_images:
            filename, img = images[index]
            plt.close(fig)
            process_and_show(filename, img)

def show_initial_selection(images):
    """Display initial selection window with 3 random images side by side."""
    fig, axes = plt.subplots(1, len(images), figsize=(7, 3))

    for i, (filename, img) in enumerate(images):
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(f"Image {i+1}", fontsize=8)
        axes[i].axis("off")

    plt.figtext(0.5, 0.01, "Click on an image to proceed", ha="center", fontsize=10)
    fig.canvas.mpl_connect('button_press_event', lambda event: on_image_click(event, images, fig))
    plt.show()

def process_and_show(filename, img):
    """Applies filters and displays the results."""
    img = preprocess_image(img)

    # Filter parameters - Tuned for speckle removal and detail preservation
    median_kernel_size = 5
    bilateral_kernel_size = 15
    bilateral_sigma_color = 75
    bilateral_sigma_space = 15
    crimmins_iterations = 3
    opening_kernel_size = 3
    closing_kernel_size = 3

    processed_median = apply_median_filter(img, median_kernel_size)
    processed_bilateral = apply_bilateral_filter(img, bilateral_kernel_size, bilateral_sigma_color,
                                                bilateral_sigma_space)
    processed_crimmins = apply_crimmins_speckle_removal(img, iterations=crimmins_iterations)
    processed_mymethod = apply_my_method(img, crimmins_iterations=crimmins_iterations,
                                          opening_kernel_size=opening_kernel_size,
                                          closing_kernel_size=closing_kernel_size)

    diff_median = calculate_difference_image(img, processed_median)
    diff_bilateral = calculate_difference_image(img, processed_bilateral)
    diff_crimmins = calculate_difference_image(img, processed_crimmins)
    diff_mymethod = calculate_difference_image(img, processed_mymethod)

    display_results(filename, img, processed_median, processed_bilateral, processed_crimmins,
                    processed_mymethod, diff_median, diff_bilateral, diff_crimmins, diff_mymethod)

def main():
    images = load_images("noisy/speckle")  
    show_initial_selection(images)

if __name__ == "__main__":
    main()