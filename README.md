# MRI Slice Viewer (Task 3)

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



