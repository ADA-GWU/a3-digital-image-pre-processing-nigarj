# Task 2: Speckle Noise Removal in Images

## Overview
This script is designed to load grayscale images containing speckle noise and apply various noise reduction techniques. The goal is to evaluate and compare different filtering techniques to remove speckle noise effectively.

## Features
- Loads a set of grayscale images from a given folder.
- Applies different filtering techniques:
  - **Median Filtering**
  - **Bilateral Filtering**
  - **Crimmins Speckle Removal Algorithm**
  - **Custom Method** (Combination of Crimmins filtering and morphological operations)
- Computes difference images to highlight noise removal effectiveness.
- Displays images before and after processing.
- Saves the output images for further analysis.

## Requirements
To run this script, install the following Python packages:

```bash
pip install opencv-python numpy matplotlib scikit-image
```

## Usage Instructions

1. **Prepare Your Dataset**
   - Place noisy images in the `noisy/speckle` folder.
   - Supported image formats: `.png`, `.jpg`, `.jpeg`

2. **Run the Script**
   ```bash
   python task_2_speckle.py
   ```

3. **Select an Image for Processing**
   - The script will randomly choose three images from the dataset.
   - Click on any image to proceed with processing.

4. **View Results**
   - The script applies filtering techniques and displays:
     - Original image
     - Median-filtered image
     - Bilateral-filtered image
     - Crimmins-filtered image
     - My method (Crimmins + morphological operations)
   - Difference images show removed noise.

5. **Saving Processed Images**
   - Processed images are saved in the `output_task_2` directory automatically.

## Filtering Techniques Explained

### 1. Median Filtering
   - Replaces each pixel’s value with the median of neighboring pixel values.
   - Effective in reducing salt-and-pepper noise but can blur edges.

### 2. Bilateral Filtering
   - Smoothens an image while preserving edges.
   - Considers both spatial distance and intensity differences in filtering.

### 3. Crimmins Speckle Removal
   - Iteratively adjusts dark and light pixels based on their neighbors.
   - Specifically designed for speckle noise reduction.

### 4. Custom Method (MyMethod)
   - Combines Crimmins filtering with morphological operations:
     - **Opening:** Removes small noise particles.
     - **Closing:** Fills small holes in the image.
   - Provides better noise removal while preserving details.

## Output
After running the script, the processed images will be displayed and saved for further analysis. The differences between original and processed images will highlight the effectiveness of noise removal techniques.
You may find the results of my analysis for this part of the project in the "Project_Findings" document.


# Task 3: MRI Slice Viewer 

## Overview
This project is part of an assignment where we implement a **DICOM (Digital Imaging and Communications in Medicine) MRI Slice Viewer**. The script loads a DICOM file, processes the image data, and allows users to visualize MRI slices using **Matplotlib** with an interactive slider.

The DICOM file is hosted on **Google Drive**, and the script dynamically fetches it before rendering.

---

## Features
- **Loads a DICOM file** from a publicly accessible link (Google Drive).
- **Displays the MRI slice** using a colormap.
- **Normalizes the image** to enhance visualization.
- **Provides an interactive slider** to navigate through slices.
- **Ensures dynamic image updates** based on slider input.

---

## Requirements
Ensure you have the following Python packages installed:

```bash
pip install pydicom numpy matplotlib requests
```

- **pydicom** → Reads DICOM medical images.
- **numpy** → Handles array operations and normalization.
- **matplotlib** → Displays images and provides the slider widget.
- **requests** → Fetches the DICOM file from a public URL.

---

## How It Works
### 1. Download the DICOM File
The script fetches the DICOM file from Google Drive using the **requests** module. The public Google Drive link is converted into a direct download link.

### 2. Process the Image Data
- The **pixel array** is extracted from the DICOM file.
- The data is normalized to a **[0,1] scale** for better visualization.

### 3. Display the Image
- The first MRI slice is displayed using **Matplotlib**.
- The **Inferno** colormap is applied to enhance contrast.
- A **slider widget** allows users to scroll through slices interactively.

---

## Usage
Run the script using:

```bash
python task_3_mri.py
```



