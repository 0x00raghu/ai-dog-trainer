import cv2
import time
import threading
from image_processing import convert_frame_to_pil_image
# from caption_generation_firellava_13B import generate_caption
# from response_generation_legacy import generate_response
from response_generation import text_to_speech
from response_generation import next_instruction
from response_generation import appreciate
from image_understanding import detect_frame
from motor import rotate_60_degrees

# create VideoCapture object for camera feed
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)  # set resolution to 640x280
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)

# initialize variable for tracking processing times
last_process_time = time.time()
last_process_time_repeat_instruction = time.time()

# last_generation_time = time.time()
# previous_caption = ""  # initialize variables for tracking previous captions and responses
# previous_response = ""
# previous_captions = []
# previous_responses = []
lock = threading.Lock()  # initialize lock for threading synchronization
is_followed = 0


# convert frame to pil image and check if the person followed the instruction
def process_frame(frame, previous_instruction):
    global is_followed 
    pil_image = convert_frame_to_pil_image(frame)
    current_time = time.time()
    response_data = detect_frame(pil_image, previous_instruction)  # generate response for caption and previous response
    followed = response_data['followed']  # Extract followed status    
    print("detect time",time.time()-current_time)    
    print(followed)
    if followed == 1:
        is_followed = 1


def display_frame(frame):
    """
    Function to display a frame on the screen and overlay the previous captions on top of it.
    """
    with lock: # synchronize with lock
        cv2.imshow('frame', frame)


def introduce():
    intro_text = "Hi Toffee. Here's a Treat. Sit."
    text_to_speech(intro_text)

def detect(previous_instruction):
    global last_process_time, is_followed, last_process_time_repeat_instruction
    while is_followed == 0: # loop until person/dog follows the instruction
        ret, frame = cap.read()
        if not ret:
            print("Error capturing frame, exiting.")
            break


        current_time = time.time()
        if current_time - last_process_time >= 0.4:
            t = threading.Thread(target=process_frame, args=(frame, previous_instruction,))
            t.start()
            last_process_time = current_time

        if current_time - last_process_time_repeat_instruction >= 5:
            t2 = threading.Thread(target=repeat_instruction, args=(previous_instruction,))
            t2.start()
            last_process_time_repeat_instruction = current_time

        display_frame(frame)

        if cv2.waitKey(1) == ord('q'):
            print("ordq error")
            break    

def repeat_instruction(previous_instruction):
    text_to_speech(previous_instruction)

def reward(previous_instruction):
    print("rotating")
    rotate_thread = threading.Thread(target=rotate_60_degrees)
    rotate_thread.start()    
    appreciate_thread = threading.Thread(target=appreciate, args = (previous_instruction,))
    appreciate_thread.start()
    rotate_thread.join()  # Wait for rotation to complete
    appreciate_thread.join()

#The LOOOOOOP
def main():
    global is_followed    
    introduce() # intro and first instruction
    previous_instruction = "Sit."
    while True:
        print("starting detection")
        detect(previous_instruction) # detect if the dog followed the instruction
        print("ended detection")
        print("starting reward")
        reward(previous_instruction) # drop treat + appreciate (implement streaming)
        print("ending reward")
        time.sleep(7) # give time for grabbing the treat and prepare for the next instruction
        is_followed = 0
        # hook() # sound effect to grab attention
        print("starting instruction")
        previous_instruction = next_instruction(previous_instruction) # generate and speak out the instruction (implement streaming)
        print("ending instruction")


if __name__ == '__main__':
    main()
