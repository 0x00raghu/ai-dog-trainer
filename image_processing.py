import cv2
from PIL import Image
from io import BytesIO
import base64
from io import BytesIO


# Converting an input frame to a PIL image
def convert_frame_to_pil_image(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    return pil_image


def pil_image_to_base64(pil_image):
    img_byte_arr = BytesIO()
    pil_image.save(img_byte_arr, format='JPEG')  # You can change the format if needed
    img_byte_arr = img_byte_arr.getvalue()
    base64_encoded = base64.b64encode(img_byte_arr)
    return base64_encoded.decode('utf-8')  # Convert bytes to string

