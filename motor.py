from gpiozero import OutputDevice
import time

# Pin assignments
in1 = OutputDevice(17)
in2 = OutputDevice(18)
in3 = OutputDevice(27)
in4 = OutputDevice(22)

# Sleep time configuration
step_sleep = 0.001

# Step count (number of steps for a 90 degree rotation)
# Assuming 4096 steps for a full 360 degree rotation
steps_per_60_degrees = 4096 // 6

# Direction: True for clockwise, False for counter-clockwise
direction = False

# Stepper motor sequence (8-step sequence)
step_sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

motor_pins = [in1, in2, in3, in4]
motor_step_counter = 0

# Define a function to cleanup GPIO setup
def cleanup():
    in1.off()
    in2.off()
    in3.off()
    in4.off()

def rotate_60_degrees():    
    global motor_step_counter
    try:
        for _ in range(steps_per_60_degrees):
            for pin_index, pin in enumerate(motor_pins):
                if step_sequence[motor_step_counter][pin_index] == 1:
                    pin.on()
                else:
                    pin.off()

            # Update step counter based on direction
            if direction:
                motor_step_counter = (motor_step_counter - 1) % 8
            else:
                motor_step_counter = (motor_step_counter + 1) % 8

            time.sleep(step_sleep)
        # Pause or do something else between 90 degree steps if necessary
        # time.sleep(1)  # Uncomment to add a pause
    finally:
        cleanup()