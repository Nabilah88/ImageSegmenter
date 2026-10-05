import os
import urllib.request
import cv2
import numpy as np
import mediapipe as mp

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(SCRIPT_DIR, "selfie_multiclass_256x256.tflite")
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite"

if not os.path.exists(MODEL_PATH):
    print("Downloading selfie_multiclass_256x256.tflite model...")
    req = urllib.request.Request(MODEL_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(MODEL_PATH, 'wb') as out_file:
        out_file.write(response.read())
    print("Download complete!")

image_path = os.path.join(SCRIPT_DIR, "image.jpg")
image = cv2.imread(image_path)
if image is None:
    print(f"Image not found at '{image_path}'!")
    exit()


rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

BaseOptions = mp.tasks.BaseOptions
ImageSegmenter = mp.tasks.vision.ImageSegmenter
ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions

options = ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    output_category_mask=True
)

with ImageSegmenter.create_from_options(options) as segmenter:
    segmentation_result = segmenter.segment(mp_image)
    category_mask = segmentation_result.category_mask.numpy_view()

BACKGROUND, HAIR, BODY_SKIN, FACE_SKIN, CLOTHES, OTHERS = 0, 1, 2, 3, 4, 5

hijab_mask = np.isin(category_mask, [HAIR, CLOTHES, OTHERS]).astype(np.uint8) * 255

skin_mask = np.isin(category_mask, [FACE_SKIN, BODY_SKIN]).astype(np.uint8) * 255
hijab_mask = cv2.bitwise_and(hijab_mask, cv2.bitwise_not(skin_mask))

kernel = np.ones((5, 5), np.uint8)
hijab_mask = cv2.morphologyEx(hijab_mask, cv2.MORPH_OPEN, kernel)
hijab_mask = cv2.morphologyEx(hijab_mask, cv2.MORPH_CLOSE, kernel)


hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
h, w = hijab_mask.shape
sample_region_mask = hijab_mask[0:h // 6, w // 3:2 * w // 3]
sample_pixels_hsv = hsv_image[0:h // 6, w // 3:2 * w // 3][sample_region_mask == 255]

if len(sample_pixels_hsv) > 0:
    reference_hue = np.median(sample_pixels_hsv[:, 0])
    reference_sat = np.median(sample_pixels_hsv[:, 1])

    hue_diff = np.abs(hsv_image[:, :, 0].astype(int) - reference_hue)
    hue_diff = np.minimum(hue_diff, 180 - hue_diff)
    sat_diff = np.abs(hsv_image[:, :, 1].astype(int) - reference_sat)

    HUE_TOLERANCE = 20
    SAT_TOLERANCE = 60
    color_match = (hue_diff < HUE_TOLERANCE) & (sat_diff < SAT_TOLERANCE)
    hijab_mask = cv2.bitwise_and(hijab_mask, (color_match.astype(np.uint8) * 255))

cv2.imwrite(os.path.join(SCRIPT_DIR, "hijab_mask.png"), hijab_mask)



def recolor_hijab(
    image_bgr,
    mask,
    target_hex,
    dilate_px=3,
    feather_px=3,
    saturation_boost=1.0,
    value_blend=0.35,
):
    """
  
    """
    target_hex = target_hex.lstrip('#')
    target_rgb = tuple(int(target_hex[i:i + 2], 16) for i in (0, 2, 4))
    target_bgr = np.uint8([[target_rgb[::-1]]])
    target_hsv = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2HSV)[0][0]
    target_hue, target_sat, target_val = int(target_hsv[0]), int(target_hsv[1]), int(target_hsv[2])

    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    recolored_hsv = hsv.copy()
    recolored_hsv[:, :, 0] = target_hue
    recolored_hsv[:, :, 1] = np.clip(target_sat * saturation_boost, 0, 255)

    original_v = hsv[:, :, 2]
    recolored_hsv[:, :, 2] = np.clip(
        original_v * (1 - value_blend) + target_val * value_blend, 0, 255
    )

    recolored_hsv = recolored_hsv.astype(np.uint8)
    recolored_bgr = cv2.cvtColor(recolored_hsv, cv2.COLOR_HSV2BGR)

   
    dilate_kernel = np.ones((dilate_px, dilate_px), np.uint8)
    dilated_mask = cv2.dilate(mask, dilate_kernel)
    feathered_mask = cv2.GaussianBlur(dilated_mask, (0, 0), sigmaX=feather_px)
    alpha = (feathered_mask.astype(np.float32) / 255.0)[:, :, np.newaxis]

    blended = (recolored_bgr.astype(np.float32) * alpha +
               image_bgr.astype(np.float32) * (1 - alpha))
    return blended.astype(np.uint8)

result_peach = recolor_hijab(image, hijab_mask, "#F2A97E")
cv2.imwrite(os.path.join(SCRIPT_DIR, "recolored_peach_v2.png"), result_peach)

result_dark = recolor_hijab(image, hijab_mask, "#3A2E2C", saturation_boost=1.3, value_blend=0.5)
cv2.imwrite(os.path.join(SCRIPT_DIR, "recolored_dark_v2.png"), result_dark)

print("Done — check recolored_peach.png and recolored_dark.png")