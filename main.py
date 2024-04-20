import cv2
import time
import threading
from image_processing import convert_frame_to_pil_image
from caption_generation_gpt4 import generate_caption
from openai_response_generation import generate_response
from text_to_voice import text_to_speech

# create VideoCapture object for camera feed
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)  # set resolution to 640x280
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)

# initialize variable for tracking processing times
last_process_time = time.time()
last_generation_time = time.time()
previous_caption = ""  # initialize variables for tracking previous captions and responses
previous_response = ""
previous_captions = []
previous_responses = []
lock = threading.Lock()  # initialize lock for threading synchronization


# convert frame to PIL image format and generate caption for a frame
def process_frame(frame):
    global last_generation_time, previous_captions, previous_response 
    pil_image = convert_frame_to_pil_image(frame)
    current_time = time.time() # track current time for processing time comparison
    caption = generate_caption(pil_image)  
    print(time.time()-current_time)
    print(caption)
    response = generate_response(caption, previous_response)  # generate response for caption and previous response
    print(time.time()-current_time)    
    print(response)
    text_to_speech(response)
    if caption:
        #previous_captions.append(caption) # add caption to previous captions list
        #if len(previous_captions) > 3: # limit previous captions list to 10 items
        #    previous_captions.pop(0)
        previous_response = response
    last_generation_time = current_time # update last generation time


def display_frame(frame):
    """
    Function to display a frame on the screen and overlay the previous captions on top of it.
    """
    global previous_captions
    with lock: # synchronize with lock
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.0
        thickness = 1
        color = (0, 0, 0)
        org = (10, 20)
        previous_captions_str = '\n'.join(previous_captions)
        cv2.putText(frame, previous_captions_str, org, font, font_scale, color, thickness, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        flipped_frame = cv2.flip(frame, 1) # Flip the frame horizontally
        cv2.imshow('frame', flipped_frame)

#The LOOOOOOP
def main_loop():
    global last_process_time
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error capturing frame, exiting.")
            break

        current_time = time.time()
        if current_time - last_process_time >= 20:
            t = threading.Thread(target=process_frame, args=(frame,))
            t.start()
            last_process_time = current_time

        display_frame(frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main_loop()
