import fireworks.client
import boto3
from io import BytesIO
from botocore.exceptions import NoCredentialsError


fireworks.client.api_key = "tVYMmEP9Ina5PnHMrGnyhlHiwx7XSaXtMTjFnWQQ46YnLSlU"
# Assuming the Fireworks client is properly authenticated elsewhere in your code

def generate_caption(pil_image):
    global previous_caption
    try:
        image_url = upload_image_and_get_url(pil_image, "dogtoyimages", "testfolder/image.jpeg")  
        prompt = "is the person in the image siiting or standing. keep it brief. guess even if you're not sure"
        #print('I')
        completion = fireworks.client.ChatCompletion.create(
            model="accounts/fireworks/models/firellava-13b",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                },
            ],
            max_tokens=512,
            temperature=0,
        )
        #print('J')
        caption = completion.choices[0].message.content
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
    # Convert PIL Image to bytes
    # print('A')
    img_byte_arr = BytesIO()
    # print('B')
    pil_image.save(img_byte_arr, format='JPEG')
    # print('C')
    img_byte_arr = img_byte_arr.getvalue()
    #print('D')

    # Upload to S3
    s3_client = boto3.client('s3')
    #print('F')
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=img_byte_arr)
        #print('G')
       # Construct URL
        location = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        #print('H')
        if location:
            url = f"https://{bucket_name}.s3.{location}.amazonaws.com/{object_name}"
        else:
            url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        #print(url)
        return url
    except NoCredentialsError:
        return "Error: AWS credentials not found."    
