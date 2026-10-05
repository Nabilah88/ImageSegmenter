# ImageSegmenter

🧕 Hijab Segmentation & Recoloring (Python + MediaPipe + OpenCV)
This repository contains a simple Python script that performs image segmentation using MediaPipe’s Selfie Multiclass model and applies hijab recoloring using OpenCV.
It is a learning project to understand segmentation masks, color filtering, and natural recoloring techniques.


#What the Script Does?
-Downloads the selfie_multiclass_256x256.tflite segmentation model (if missing)

-Loads an input image (image.jpg)

-Generates a segmentation mask using MediaPipe

-Extracts hijab‑related regions (hair, clothes, others)

-Removes skin regions from the mask

-Cleans the mask using morphological operations

-Filters hijab pixels by hue/saturation similarity

-Recolors the hijab using HSV blending

-Saves the outputs:

->hijab_mask.png

->recolored_peach_v2.png

->recolored_dark_v2.png

#Files

main.py                 # The script (your code)
image.jpg               # Input image (add your own)
selfie_multiclass_256x256.tflite   # Auto-downloaded model
hijab_mask.png          # Generated hijab mask
recolored_peach_v2.png  # Peach recolor output
recolored_dark_v2.png   # Dark recolor output


🛠️ Requirements

- Install dependencies

  pip install mediapipe opencv-python numpy

🚀 How to Run

-Place your input image as:
image.jpg

-Then run:
python main.py

-The script will:

->download the segmentation model (first run only)

->generate a hijab mask

->produce recolored hijab images

-All outputs will appear in the same folder.

🎨 Example Output

-Add your images here once uploaded:
| Mask           | Peach                  | Dark                  |
| --- -----------| --- -------------------| --------------------- |
| hijab_mask.png | recolored_peach_v2.png | recolored_dark_v2.png |


🌙 Hijab Segmentation & Recoloring with MediaPipe + OpenCV
A Python project exploring image segmentation and hijab recoloring using MediaPipe’s Selfie Multiclass model and OpenCV color transformations.
This project is part of my journey toward building AI‑powered tools for hijab styling and personalization.

✨ Features
Downloads and loads the MediaPipe Selfie Multiclass 256×256 segmentation model

Segments hijab‑related regions (hair, clothes, head covering)

Removes skin regions from the mask

Cleans the mask using morphological operations

Extracts color samples from the top‑of‑head region

Filters hijab pixels by hue/saturation similarity

Recolors the hijab using HSV blending

Preserves shadows, folds, and natural lighting

Outputs recolored hijab images in multiple color styles

🧠 How It Works
1. Model Download
If the segmentation model is missing, the script automatically downloads:

Code
selfie_multiclass_256x256.tflite
from the official MediaPipe model repository.

2. Image Segmentation
The MediaPipe Image Segmenter produces a category mask with labels:

0 — Background

1 — Hair

2 — Body Skin

3 — Face Skin

4 — Clothes

5 — Others

The hijab mask is created by combining:

🛠️ Requirements
Python 3.8+

OpenCV

NumPy

MediaPipe

urllib (standard library)

Install dependencies:

bash
pip install opencv-python mediapipe numpy
🚀 Running the Script
Place your input image as:

Code
image.jpg
Then run:

bash
python main.py
Outputs will appear in the same folder.

🎨 Example Results
Original	Mask	Recolored
image.jpg	hijab_mask.png	recolored_peach_v2.png


(Add your images here once uploaded)

🌸 Future Improvements
More accurate hijab-only segmentation

Support for patterned hijabs

Real-time recoloring (WebRTC + ONNX)

Integration into HijabMatch web app

Automatic color recommendations based on skin tone

💗 About This Project
This project is part of my learning journey in computer vision and my long-term goal of building HijabMatch, an AI-powered hijab styling assistant that helps women visualize hijab colors that match their skin tone.



🌸 Purpose
-This project was created to help me understand:

-how segmentation models work

-how to isolate specific regions (like hijabs)

-how to recolor fabric naturally while preserving shadows and folds

-It is a foundational step toward future hijab‑styling and AI‑powered personalization tools.
