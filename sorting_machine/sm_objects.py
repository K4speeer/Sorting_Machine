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
        self.feed_step = 36
        self.drop_step = 60
        self.max_items = 10
        self.items = []
        self.pulse_delay = 0.05
        self.steps_per_revolution = 200 # 1 motor step = 1.8 degree (NEMA-17 stepper motor)
        
        
    def rotate(self, angle):
        self.board.digital_write(self.dir_pin, 1)
        steps_to_rotate = int(self.steps_per_revolution * angle / 360)
        
        for _ in range(steps_to_rotate):
            self.board.digital_write(self.step_pin, 1)
            sleep(self.pulse_delay)
            self.board.digital_write(self.step_pin, 0)
            sleep(self.pulse_delay)
            
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
        
