import boto3
from io import BytesIO
from botocore.exceptions import NoCredentialsError
from openai import OpenAI
import os

client = OpenAI()
client.api_key = "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"

def generate_caption(pil_image):
    global previous_caption
    try:
        image_url = upload_image_and_get_url(pil_image, "dogtoyimages", "testfolder/image.jpeg")  
        prompt = "is the person in the image siiting or standing. keep it brief. guess even if you're not sure"
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url,"detail":"low"}},
                    ],
                },
            ],
            max_tokens=300,
        )
        caption = response.choices[0].message.content
        previous_caption = caption
        return caption
    except Exception as e:
        print(e) 
        return "Unable to process image."

def upload_image_and_get_url(pil_image, bucket_name, object_name):
    """
    Uploads an image to AWS S3 and returns the URL of the uploaded image.

    :param pil_image: PIL Image object to upload.
    :param bucket_name: Name of the S3 bucket.
    :param object_name: S3 object name. If not specified, filename is used.
    :return: URL of the uploaded image.
    """
    img_byte_arr = BytesIO()
    pil_image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=img_byte_arr)
        location = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        if location:
            url = f"https://{bucket_name}.s3.{location}.amazonaws.com/{object_name}"
        else:
            url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        return url
    except NoCredentialsError:
        return "Error: AWS credentials not found."
