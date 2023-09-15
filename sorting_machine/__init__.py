# Import Pymata4 library for serial communication 
from pymata4 import pymata4
from .sm_objects import SortingMachine, Cassette, Gate
from picamera2 import Picamera2



def init_board():
    """Pymata4() board initialization for Serial Communicateion

    Returns:
        Pymata4(): Arduino board instance as Pymata4() object
    """
    board = pymata4.Pymata4()
    print(f"{board.get_firmware_version()}")
    print(f"{board.get_protocol_version()}")
    print(f"{board.get_pymata_version()}")
    print("Arduino board as Pymata4() instance initialized")
    return board

def init_machine(board, ir_pin, step_pin, dir_pin, servo_configs):
    # Initialize the machine object and set pins to use.

    cassette = Cassette(board, step_pin, dir_pin)
    print(f"Casseette instance initialized with parameters: "\
          f"Step pin of driver = {step_pin}"\
          f"Direction pin of driver = {dir_pin}")
    gates_list = []
    for key, value in servo_configs.items():
        pin = int(key)
        close_pos = value[0]
        open_pos = value[1]
        pos = value[2]
        gate = Gate(board, pin, close_pos, open_pos, pos)
        print(f"Servo connected to pin: {key} initialized successfully with parameters: "\
              f"Close position: {close_pos}"\
              f"Open position: {open_pos}"\
              f"Position depending on cassette origin: {pos}")
        gate.close()
        gates_list.append(gate)
    
    sm = SortingMachine(board, cassette, gates_list, ir_pin)
    print("Sorting machine initialized successfully !!!")
    return sm
           
