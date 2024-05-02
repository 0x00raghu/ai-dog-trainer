import fireworks.client
from image_processing import pil_image_to_base64
import json

fireworks.client.api_key = "tVYMmEP9Ina5PnHMrGnyhlHiwx7XSaXtMTjFnWQQ46YnLSlU"

def detect_frame(pil_image, previous_instruction):
    try:
        base64_image = pil_image_to_base64(pil_image)
        prompt = f"The image shows a person either in the sitting or standing state. This was their instruction to follow: '{previous_instruction}'. Can you generate a json response with the field 'followed' that takes the value 1 if the person followed the instruction and 0 if they did not. Don't return '1' for follolwed unless absolutely sure. "
        completion = fireworks.client.ChatCompletion.create(
            model="accounts/fireworks/models/firellava-13b",
            response_format={ "type": "json_object" },    
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}","detail":"low"}},
                    ],
                },
            ],
            max_tokens=50,
            temperature=0,
        )
        response = completion.choices[0].message.content
        print(response)
        return json.loads(response)
    except Exception as e:
        print(e) 
        return "Unable to process image."    

