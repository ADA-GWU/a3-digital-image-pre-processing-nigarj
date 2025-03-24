# Assignment 3: Image Processing and Analysis

## Overview
This assignment consists of three tasks focused on image preprocessing, noise removal, and medical image visualization. Each task applies different image-processing techniques to enhance and analyze images for better quality and interpretation.

### **Task 1: Image Preprocessing and Enhancement**
Task 1 focuses on grayscale image preprocessing by applying blurring, morphological operations, denoising, and edge enhancement techniques. It consists of two Python scripts:

#### **Script 1: `task_1_blurring.py`**
- Loads grayscale images from a directory.
- Applies **Gaussian blurring** to reduce noise.
- Uses **morphological closing** with different kernel sizes.
- Displays and saves processed images.

#### **Script 2: `task_1_denoise.py`**
- Loads grayscale images from a directory.
- **Denoises** images using non-local means denoising.
- Enhances edges using:
  - **Top-hat transformation**
  - **Canny edge detection**
  - **Sobel operator**
  - **Morphological closing**
- Displays and saves processed images.

#### **Dependencies**
Both scripts require the following Python libraries:
```sh
pip install numpy opencv-python matplotlib scikit-image
```

#### **Folder Structure**
```
project_root/
│-- noisy/chemical/  # Folder containing noisy grayscale images
│-- output_task_1/   # Folder where processed images will be saved
│-- task_1_blurring.py
│-- task_1_denoise.py
```

#### **Running Task 1 Scripts**
```sh
python task_1_blurring.py
python task_1_denoise.py
```
A selection window will display 3 random images. Click on one to process and view the results.

---
### **Task 2: Speckle Noise Removal in Images**
This script is designed to load grayscale images containing **speckle noise** and apply various noise reduction techniques, comparing their effectiveness.

#### **Features**
- Loads grayscale images from a given folder.
- Applies different filtering techniques:
  - **Median Filtering**
  - **Bilateral Filtering**
  - **Crimmins Speckle Removal Algorithm**
  - **Custom Method** (Combination of Crimmins filtering and morphological operations)
- Computes difference images to highlight noise removal effectiveness.
- Displays images before and after processing.
- Saves output images for further analysis.

#### **Dependencies**
```sh
pip install opencv-python numpy matplotlib scikit-image
```

#### **Running Task 2 Script**
```sh
python task_2_speckle.py
```

#### **Filtering Techniques Explained**
- **Median Filtering** → Reduces salt-and-pepper noise but can blur edges.
- **Bilateral Filtering** → Smoothens images while preserving edges.
- **Crimmins Speckle Removal** → Iteratively adjusts dark and light pixels to reduce speckle noise.
- **Custom Method (Crimmins + Morphology)** → Uses opening and closing morphological operations for better noise removal.

#### **Output**
Processed images are saved in the `output_task_2/` directory, highlighting noise reduction effectiveness.

---
### **Task 3: MRI Slice Viewer**
This task implements a **DICOM (Digital Imaging and Communications in Medicine) MRI Slice Viewer**. The script loads a **DICOM file**, processes the image data, and allows users to visualize MRI slices using an interactive slider.

#### **Features**
- **Loads a DICOM file** from a publicly accessible Google Drive link.
- **Displays MRI slices** using a colormap.
- **Normalizes image data** for better visualization.
- **Provides an interactive slider** to navigate through slices.

#### **Dependencies**
```sh
pip install pydicom numpy matplotlib requests
```
- **pydicom** → Reads DICOM medical images.
- **numpy** → Handles array operations and normalization.
- **matplotlib** → Displays images and provides slider widget.
- **requests** → Fetches the DICOM file from Google Drive.

#### **Running Task 3 Script**
```sh
python task_3_mri.py
```

#### **How It Works**
1. **Download the DICOM File**
   - The script fetches the DICOM file from Google Drive using `requests`.
2. **Process the Image Data**
   - Extracts **pixel array** from the DICOM file.
   - Normalizes data to a **[0,1] scale** for better contrast.
3. **Display the Image**
   - Displays the first MRI slice with **Inferno colormap**.
   - A **slider widget** allows users to scroll through slices interactively.

---


