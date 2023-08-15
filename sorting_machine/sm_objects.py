class Item:
    def __init__(self):
        self.color = None
        self.size = None
        self.image = None
        self.prediction_info = {}
        
    def get_color(self):
        return self.color
    
    def get_size(self):
        return self.size
    
    def get_image(self):
        return self.image
    
    def get_prediction_info(self):
        return self.prediction_info
    
    def set_color(self, color):
        self.color = color
    
    def set_size(self, size):
        self.size = size
        
    def set_image(self, image):
        self.image = image
        
    def set_prediction_info(self, prediction_type, prediction_result):
        self.prediction_info[prediction_type] = prediction_result
        
class Cassette:
    def __init__(self, board, step_pin, dir_pin):
        self.board = board
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.direction_value = 1 # 1 Clockwise , 0 CounterClockwise
        self.feed_step = 36
        self.drop_step = 60
        self.max_items = 10
        self.items = []
        self.pulse_delay = 0.05
        self.steps_per_revolution = 200 # 1 motor step = 1.8 degree (NEMA-17 stepper motor)
        self.initial_pos = 0
        self.current_pos = 0
        
    def rotate(self, angle):
        self.board.digital_write(self.dir_pin, self.direction_value)
        steps_to_rotate = int(self.steps_per_revolution * angle / 360)
        
        for _ in range(steps_to_rotate):
            self.board.digital_write(self.step_pin, 1)
            sleep(self.pulse_delay)
            self.board.digital_write(self.step_pin, 0)
            sleep(self.pulse_delay)
        
        self.current_pos += angle
        
    def origin(self):
        position = self.current_pos % 360
        if position >= 180:
            angle = 360 - position
            self.rotate(angle)
        else:
            self.direction_value = 0
            self.rotate(position)
            sleep(4)
            self.direction_value = 1
            
    def add_item(self, item):
        self.items.append(item)
        
class Gate:
    def __init__(self, board, pin, close_pos, open_pos):
        self.board = board
        self.pin = pin
        self.close_pos = close_pos
        self.open_pos = open_pos
        self.board.set_pin_mode_servo(self.pin)
        
    def open(self):
        self.board.servo_write(self.pin, self.open_pos)
    
    def close(self):
        self.board.servo_write(self.pin, self.close_pos)
    
    def drop_item(self):
        self.open()
        sleep(1.5)
        self.close()
        sleep(1.5)
        
class SortingMachine:
    def __init__(self, cassette, gates_list):
        self.cassette = cassette
        self.gates = gates_list
        # # The code below used to define each gate from the gate_list as g(i)
        # # Its equals to : self.g1 = gates_list[0] and so on
        # # But don't forget to refactor rest of the code that related to the gates
        # self.gates_prefix = "g"
        # for i, gate in enumerate(self.gates):
        #     gate_name = f"{self.gates_prefix}{i+1}"
        #     setattr(self, gate_name, gate)
        #
        # In my case I'll work with 3 gates so i will decalare them individually 
        self.g1 = self.gates[0]
        self.g2 = self.gates[1]
        self.g3 = self.gates[2]
        
            
   
        
            