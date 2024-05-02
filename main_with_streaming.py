import cv2
import time
import threading
from image_processing import convert_frame_to_pil_image
# from caption_generation_firellava_13B import generate_caption
# from response_generation_legacy import generate_response
from response_generation import text_to_speech
from response_generation import next_instruction
from response_generation_with_streaming import appreciate
from image_understanding import detect_frame
import asyncio
from motor import rotate_60_degrees


# create VideoCapture object for camera feed
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)  # set resolution to 640x280
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)

# initialize variable for tracking processing times
last_process_time = time.time()
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
    intro_text = "This is John Wick and I'm here to train you to sit and stand. Find a chair and start by sitting down. Follow my instructions to get skittles."
    text_to_speech(intro_text)

def detect(previous_instruction):
    global last_process_time, is_followed
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

        display_frame(frame)

        if cv2.waitKey(1) == ord('q'):
            print("ordq error")
            break    

async def reward(previous_instruction):
    print("rotating")
    rotate_thread = threading.Thread(target=rotate_60_degrees)
    rotate_thread.start()    
    await appreciate(previous_instruction)  # Await the coroutine directly
    rotate_thread.join()  # Wait for rotation to complete

#The LOOOOOOP
def main():
    global is_followed    
    introduce() # intro and first instruction
    previous_instruction = "Sit down."
    while True:
        print("starting detection")
        detect(previous_instruction) # detect if the dog followed the instruction
        print("ended detection")
        print("starting reward")
        asyncio.run(reward(previous_instruction)) # drop treat + appreciate (implement streaming)
        print("ending reward")
        time.sleep(3) # give time for grabbing the treat and prepare for the next instruction
        is_followed = 0
        # hook() # sound effect to grab attention
        print("starting instruction")
        previous_instruction = next_instruction(previous_instruction) # generate and speak out the instruction (implement streaming)
        print("ending instruction")


if __name__ == '__main__':
    main()
