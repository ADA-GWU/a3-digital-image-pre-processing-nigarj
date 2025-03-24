import pydicom
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import requests
import io

# Google Drive direct download link
dicom_url = "https://drive.google.com/uc?id=1eY2JnfI9RnYeT6ItZ_Fn_Yh3JXpAD-jC"

# Download the DICOM file
response = requests.get(dicom_url)
response.raise_for_status()  # Ensure request was successful
dicom_data = pydicom.dcmread(io.BytesIO(response.content))

# Extract and normalize pixel data
image_data = dicom_data.pixel_array.astype(np.float32)
image_data = (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data))  # Normalize to [0,1]

# Extract metadata dynamically (excluding pixel data)
metadata = {elem.keyword: getattr(dicom_data, elem.keyword, "Not Available")
            for elem in dicom_data if elem.keyword and elem.keyword != "PixelData"}

# Print metadata to console
print("\n=== DICOM Metadata ===")
for key, value in metadata.items():
    print(f"{key}: {value}")

# Set up figure
fig, ax = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(left=0.1, bottom=0.25)

# Display first slice
colormap = 'inferno'
im = ax.imshow(image_data[0], cmap=colormap)
ax.set_title("MRI Slice Viewer")
ax.axis('off')

# Create slider for navigating slices
ax_slider = plt.axes([0.1, 0.1, 0.8, 0.05], facecolor='lightgray')
slider = Slider(ax_slider, "Slice", 0, image_data.shape[0] - 1, valinit=0, valstep=1)

# Function to update displayed slice
def update(val):
    slice_index = int(slider.val)
    im.set_array(image_data[slice_index])
    ax.set_title(f"Slice {slice_index + 1} / {image_data.shape[0]}")
    fig.canvas.draw_idle()

# Connect slider to update function
slider.on_changed(update)

plt.show()
