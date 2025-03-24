import pydicom
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Load the DICOM file
dicom_path = "E1154S7I.dcm"  # Update with your file path
dicom_data = pydicom.dcmread(dicom_path)

# Extract pixel data and normalize
image_data = dicom_data.pixel_array.astype(np.float32)
image_data = (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data))  # Normalize to [0,1]

fig, ax = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(left=0.1, bottom=0.25)  # Space for slider

# Display the first slice
colormap = 'inferno' 
im = ax.imshow(image_data[0], cmap=colormap)
ax.set_title("MRI Slice Viewer")

# Slice index text overlay
slice_text = ax.text(10, 20, f"Slice: 0", color="white", fontsize=12, bbox=dict(facecolor='black', alpha=0.5))

# Create Slider Axis
ax_slider = plt.axes([0.1, 0.1, 0.8, 0.05], facecolor='lightgray')
slider = Slider(ax_slider, "Slice", 0, image_data.shape[0] - 1, valinit=0, valstep=1)

# Update function for slider
def update(val):
    slice_index = int(slider.val)
    im.set_array(image_data[slice_index])
    slice_text.set_text(f"Slice: {slice_index}/{image_data.shape[0] - 1}")
    fig.canvas.draw_idle()

# Connect slider to update function
slider.on_changed(update)

plt.show()
