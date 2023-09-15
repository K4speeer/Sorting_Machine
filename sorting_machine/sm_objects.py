import time
import datetime
import os
from picamera2 import Picamera2

class Item:
    '''
    Item object
    - Attributes: color (str) / size (str) / image_path (str) / prediction_info{ "prediction_type" : prediction_result[] } (dict)
    - Methods: get_color(), get_size(), get_image_path(), get_prediction_info()
    set_color(), set_size(), set_image_path(), set_prediction_info()
    '''
    def __init__(self):
        self.color = None # objects color
        self.size = None # objects size ("small", "big")
        self.image_path = None # objects image_path
        self.prediction_info = {} # objects prediction info dict (key: prediction type , value: list of prediction result)
        self.distination = 0
        self.index = 0
        self.gate = None
        print("An item initiated successfully")
        
    def get_color(self):
        '''
        Returns: Objects color in string format 
         example: "red"
        '''
        return self.color
    
    def get_size(self):
        '''
        Returns: Objects size in string format 
         example: "small"
        '''
        return self.size
    
    def get_image_path(self):
        '''
        Returns: Image path
        '''
        return self.image_path
    
    def get_prediction_info(self):
        '''
        Returns: A dictionary where:
            Key: classification Type (color / size)
            Value: A list with prediction result
        '''
        return self.prediction_info
    
    
    def set_color(self, color):
        '''
        - Input: Color class in string format
        - Sets a color attribute to the object 
        '''
        self.color = color
    
    def set_size(self, size):
        '''
        - Input: Size class in string format
        - Sets a size attribute to the object 
        '''
        self.size = size
        
    def set_image_path(self, image_path):
        '''
        - Input: Objects image path as a string
        - Sets an image path of the object 
        '''
        self.image_path = image_path
        
    def set_prediction_info(self, prediction_type, prediction_result):
        '''
        - Input:
            - prediction_type: ("color" / "size")
            - prediction_result: A list of prediction results
        - Sets a key/value data in a prediction_info dict of the object 
        '''
        self.prediction_info[prediction_type] = prediction_result
    
    def set_gate(self, gate):
        self.gate = gate

class Cassette:
    '''
    Cassette object represents the circular plate with sectors that moved and controlled by the stepper motor
    
    Attributes:
        - board: Pymata4() objects that represents Arduino board
        - step_pin: Arduino pin that connected to step_pin of the stepper motor driver(A4988)
        - dir_pin: Arduino pin that connected to direction pin of the stepper motor driver(A4988)
    
    Methods:
        - rotate(angle): takes an angle value as an attribute and rotates the stepper
        - origin(): sets the stepper to the initial position
        - add_item(item): takes Item object as attribute and adds it to current items list of the cassette
        - not_empty(): boolean function to check if the cassette is empty of items or not
        - clear_items(): clears current items[] list (used after distributing) 
    '''
    def __init__(self, board, step_pin, dir_pin):
        self.board = board # Arduino board (Pymata4 object)
        self.step_pin = step_pin # Step pin of the stepper motor driver (A4988) 
        self.dir_pin = dir_pin # Direction pin of the stepper motor
        self.board.set_pin_mode_digital_output(self.step_pin)
        self.board.set_pin_mode_digital_output(self.dir_pin)
        self.direction_value = 1 # Rotation Direction: 1 Clockwise , 0 CounterClockwise
        self.feed_step = 36 # Feeding step 36° (The cassette is circular and containes 10 sectors -> 360/10 = 36°)
        self.max_items = 10 # Number of cassette sectors
        self.items = [] # A list of current items in cassette
        self.pulse_delay = 0.05 # Time delay between step_pin output pulses (changable, affects rotation speed)
        self.steps_per_revolution = 200 # 1 motor step = 1.8° (NEMA-17 stepper motor) (changable, depends on used stepper motor)
        self.initial_pos = 0 # A variable used to calculate the distance to origin position
        self.current_pos = 0 # A variable to track cassette position
        
    def rotate(self, angle):
        '''
        A function to control stepper motor rotation using A4988 driver
        Input: The angle for the stepper motor to rotate
        Action: send pulses from board(arduino) to step_pin(driver) every pulse_delay(sec)
        '''
        # Set rotation direction (1: CW, 0: CCW)
        self.board.digital_write(self.dir_pin, self.direction_value)
        # Calculates steps needed to acheive the desired angle using the formula below:
        # steps per revolution * desired angle / 360°
        steps_to_rotate = round(self.steps_per_revolution * angle / 360)
        # for loop to send pulses from the board to the driver
        for _ in range(steps_to_rotate):
            # Setting step_pin value to: 1 -  Logic HIGH
            self.board.digital_write(self.step_pin, 1)
            # Making a delay for pulse_delay (seconds)
            time.sleep(self.pulse_delay)
            # Setting step_pin value to: 0 -  Logic LOW
            self.board.digital_write(self.step_pin, 0)
            # Making a delay for pulse_delay (seconds)
            time.sleep(self.pulse_delay)
        # Adding the rotated angle to the current position to track the position of the cassette
        if self.direction_value == 1:
            self.current_pos += angle
        else:
            self.current_pos -= angle
        print(f"Cassette at poistion {self.current_pos%360}")
        
    def origin(self):
        '''
        A function to set the cassette to origin position
        '''
        # Calculating current cassette position
        # Getting the angle between the initial_position and current_position
        position = self.current_pos % 360
        # Checking the value of the angle to determine optimal rotation direction
        #  If >= 180 rotate CW, else rotate CCW
        if position >= 180:
            # Calculating the angle
            angle = 360 - position
            # Calling rotate() function with calculated angle as argument
            self.rotate(angle)
            # A time delay
            time.sleep(2)
        else:
            # Setting rotation direction to CCW 0 - Logic LOW 
            self.direction_value = 0
            self.rotate(position)
            time.sleep(2)
            # Setting rotation direction back to CW 1 - Logic HIGH 
            self.direction_value = 1
        print("Cassette at origin position", end="\n")
           
    def add_item(self, item):
        """Function to add Item object to current items[] of the cassette

        Args:
            item (Object): An Item object
        """
        self.items.append(item)
        print("Item added to Cassette's list")
    
    def not_full(self):
        return True if len(self.items) < 10 else False    
    
    def not_empty(self):
        """Boolean function to check wethere the cassette is empty or nut

        Returns:
            Boolean: True if not empty else False
        """
        return True if len(self.items) > 0 else False

    def clear_items(self):
        """Clears the current items[] list of objects
                
                Used after distributing the items
        """ 
        self.items.clear()
        print("Cassette's list cleared")
               
class Gate:
    '''
    Gate object represents the gates in the machine base that controlled with servo-motors (MG-995)
    
    Attributes:
        - board: Pymata4() object represents the Arduino board (object)
        - pin: Arduino pin that the servo-motor connected to (int)
        - close_pos: angle value at which the gate is in close position (int [0:180])
        - open_pos: angle value at which the gate is in open position (int [0:180])
        - parameter: the sorting parameter that the gate should accept (str)
        - position: the angle between the gate and the initial position of the stepper motor cassette (int)
        
    Methods:
        - get_param(): returns the sorting parametter attached to the gate in string format
        - set_param(param): takes a str format paramter that associated with the gate
        - add_item(): adds an item to the list of items to be passed through the gate
        - get_objects_quantaty(): returns total number of objects passed to through the gate
        - open(): opens the gate
        - close(): closes the gate
        - drop_item(): opens the gate and closes it after dropping the Item
    '''
    
    def __init__(self, board, pin, close_pos, open_pos, position):
        self.board = board # Pymata4() objects represents Arduino board
        self.pin = pin # Pin number that attached to the servo-motor
        self.close_pos = close_pos # Angle value that sets the gate to close position
        self.open_pos = open_pos # Angle value that sets the gate to open position
        self.board.set_pin_mode_servo(self.pin) # defining the pin as a servo pin in pymata4.Pymata4() object
        self.parameter =  None # The sorting parameter that the gate responsible of
        self.objects_passed = 0 # Passed objects counter variable
        self.items = [] # List of Item's indexes from the cassette to be passed to the gate 
        self.position = position # The angle between the gate and cassette initial position
    
    def set_param(self, parameter):
        """Attaches a sorting parameter to the gate

        Args:
            parameter (str): A parameter that the gate is responsible for
        """
        self.parameter = parameter
    
    def get_param(self):
        """Get the sorting parameter that attached to the gate

        Returns:
            string: sorting parameter 
        """
        return self.parameter
    
    def add_item(self, item):
        """Adding an index of the item form the cassette list to be passed to the gate

        Args:
            item (int): Item's index from the cassette's current items[] list
        """
        self.items.append(item)
        print("Item added to list")
    
    def get_objects_quantaty(self):
        """Get total number of objects passed through the gate

        Returns:
            int: Total number objects passed
        """
        return self.objects_passed
        
    def open(self):
        """Function to open the gate
        """
        # Using  Pymata4 object to set the servo to the open_pos angle
        self.board.servo_write(self.pin, self.open_pos)
        time.sleep(1)
        print("Servo Openned", end="\n")
    
    def close(self):
        """Function to close the gate
        """
        # Using Pymata4 object to set the servo to the close_pos angle
        self.board.servo_write(self.pin, self.close_pos)
        time.sleep(1)
        print("Servo Closed", end="\n")
    
    def test_servo(self):
        self.open()
        self.close()
    
    def drop_item(self):
        """Function to drop an item in the gate by openning it and closing after delay (1.5 seconds)
        """
        self.open()
        # Increment the number of objects passed by 1
        self.objects_passed += 1
        self.close()
        print("Item collected!", end="\n")
 
        
class SortingMachine:
    """Sorting Machine object, represents the full machine that works with:
            1 Stepper motor controlled by A4988 Driver as Cassette() object
            3 Servo motors (MG-995) as Gate() objects
            IR obstacle sensor 
        Attributes:
            board: Arduino board as Pymata4() object 
            cassette: Stepper motor as Cassette() object 
            gates_list: List of servo motors represented as Gate() objects
            ir_sensor_pin: Arduino pin number that connected to IR obstacle sensor
            sorting_param: General sorting parameter of the machine ("color" / "size" / "colorsize")
            session_id: ID number of the session in the database used to generate a session name
        Methods:
            set_gates_params(gates_params): sets a sorting parameter for each gate
            set_general_sort_parameter(parameter): sets a general sorting parameter
            set_session_id(session_id): sets a session ID for current session
            take_picture(file_name): Initaites Raspberry-Pi camera to capture image and save it with passed file_name argument
            ir_listener(): Returns True if IR detecs an obstacle, else returns False
            timer(duration): Timer function works on countdown mode from the passed duration argument
            feed(): Controls cassette feeding process with objects to be sorted
            classify_color(item, model_function): Runs color classification model with passed function on the item 
            classify_size(item, model_function): Runs size classification model with passed function on the item  
            sort(): processes the data after classification and sorts currently feeded cassette items by gates
            distribute(): Distributes the items in specific gates based on sort() results
            finish_and_report(): Generates a list with operation report data and shuts the machine down
            create_session_folder(): Creates a folder to store item images taken during the sorting process 
            run(): Loop function for running the machine 
    """
    def __init__(self, board, cassette, gates_list, ir_sensor_pin):
        self.cassette = cassette # Cassette() object 
        self.gates = gates_list # List of Gate() objects
        # # The code below used to define each gate from the gate_list as g(i)
        # # Its equals to : self.g1 = gates_list[0] and so on
        # # But don't forget to refactor rest of the code that related to the gates
        # self.gates_prefix = "g"
        # for i, gate in enumerate(self.gates):
        #     gate_name = f"{self.gates_prefix}{i+1}"
        #     setattr(self, gate_name, gate)
        #
        # In my case I'll work with 3 gates so i will decalare them individually 
        # self.g1 = self.gates[0]
        # self.g2 = self.gates[1]
        # self.g3 = self.gates[2]
        self.board = board # Pymata4() object representing Arduino board
        self.ir_sensor_pin = ir_sensor_pin # IR-Sensor pin number
        self.board.set_pin_mode_digital_input_pullup(self.ir_sensor_pin) # Declaring IR sensor pin as digital input with pullup resistor activation
        self.ir_trig_val = 0 # Default IR trigger Value 0 - Logic LOW
        self.sorting_param = 'color' # General sroting parameter, Default: "color" 
        self.total_objects = 0 # Variable to count total objects number
        self.classified_objects = [] # Currently loaded items with classification information
        self.start_time = "" # Session start time
        self.end_time = "" # Session end time
        self.session_id = 0 # Session ID related on database information
        self.date_info = datetime.datetime.now().strftime("%Y-%m-%d - %H:%M") # Getting current date and time information
        self.session_name = "" # Generating a session name using session_id and current date
        self.images_path = "" # Default image path
        self.report = []
        self.timer_interrupted = False
        self.sort_circle = False
        
    def set_gates_params(self, gates_params):
        """Sets a sorting parameter for each gate

        Args:
            gates_params (list): list of strings represents sorting parameter per gate
        """
        print("Setting parameters to gates", end="\n")
        for i, gate in enumerate(self.gates):
            parameter = gates_params[i]
            if parameter:
                gate.set_param(parameter)
                print(f"Parameter: {parameter} attached to Gate({gate.pin})", end="\n")
            else:
                print("Last gate left without parameters", end="\n")
        
    def set_general_sort_parameter(self, general_parameter):
        """Sets general sorting parameter ("color" / "size" / "colorsize")

        Args:
            general_parameter (str): A global parameter for the machine
        """
        self.sorting_param = general_parameter
        print(f"General sort parameter set to: {general_parameter}", end="\n")
    
    def set_session_id(self, session_id):
        """Sets Session ID

        Args:
            session_id (int): Session ID
        """
        self.session_id = session_id
        self.session_name = f"{self.session_id}-{self.date_info.split(' - ')[0]}"
        print(f"Session Name generated to be: {self.session_name}")
        print(f"Session ID set to: {session_id}", end="\n")
        
    def take_picture(self, file_name):
        """Image Capturing function

        Args:
            file_name (string): image file name and path
        """
        # Using Picamera2() object to deal with Raspberry-Pi Camera 
        with Picamera2() as cam:
            # Initaite the camera
            cam.start()
            # Capture an image and saving it in file_name location
            cam.capture_file(file_name)
            print(f"Captured and saved file to: {file_name}", end="\n")
        
        time.sleep(1.5)
        
    def ir_listener(self):
        """IR obstacle sensor listener function

        Returns:
            Boolean: True if obstacle detected, else False
        """
        # The Pymata4() function digital_read(pin) returns two arguments: Value, TimeStamp
        # We are intrested in one of them, the Value on the sensor, so using it
        # Getting sensor value
        val, timestamp = self.board.digital_read(self.ir_sensor_pin)
        # Returning True if obstacle detected, False if no obstacles
        return True if val == self.ir_trig_val else False

    def timer(self, duration):
        """Timer function, because "time is a valuble thing" (In The End - Linking Park)

        Args:
            duration (int): The desired duration of the timer
        """
        # Getting current time using time() function
        start_time = time.time()
        print(f"Timer started at: {start_time} and will work for {duration} sec", end="\n")
        # Start while loop for passed duration as acondition
        while time.time() - start_time < duration:
            # Checking the value of IR-Sensor
            # If IR detects an obstacle, the return expression gets us out of the loop and the function 
            if self.ir_listener():
                self.timer_interrupted = True
                print("Timer interrupted !!!", end="\n")
                return
        # If during timer working there was not any obstacles then:
        # We check at which stage of sorting process we are
        # If the cassette was feeded earlier, then we move to next stages: sort() -> distribute() -> finish_and_report()
        self.timer_interrupted = False
        return
                         
    def feed(self):
        """Cassette feeding function
        """
        if self.cassette.not_full():
            print("Feeding an object to the machine", end="\n")
            time.sleep(0.5)
            # Generating image file name and path based on the path of the session folder and items index during the process
            img_file_name = f'{self.images_path}/{self.total_objects + 1}.jpg'
            # Capture image of the item passed to the machine
            self.take_picture(img_file_name)
            # Creating an Item() object for the item passed
            print("Creating Item object to save item's details", end="\n")
            item = Item()
            # Setting the related image_path to item
            print("Taking an image of the item", end="\n")
            item.set_image_path(img_file_name)
            # Adding item to the cassette's current items[] list
            print("Adding item to the cassette's current item list", end="\n")
            self.cassette.add_item(item)
            # Incrementing the number of the objects passed 
            self.total_objects += 1
            print(f"incrementing total objects number to become: {self.total_objects}", end="\n")
            time.sleep(0.5)
            # Rotating the cassette to prepare for next item
            self.cassette.rotate(self.cassette.feed_step)
            print("Moving to the next sector. Preparing for new item", end="\n")
            time.sleep(0.5)
        else:
            self.sort()
            self.distribute()
        
    def classify_color(self, item, model_function=None):
        """Classification funcrion for Color parameter

        Args:
            item (Item()): Item() object to be processed and classified
            model_function (Function): The function that triggers specific CNN model

        Returns:
            str: The name of the class that the object belongs to 
        """
        # Getting object's image path to be processed
        image_path = item.get_image_path()
        # Passing the image_path to the model function to be processed and saving the list results to result varible
        result = model_function(image_path)
        # getting the class_name from the result[] list 
        class_name = result[1]
        # Setting the color parameter to the Item() object 
        item.set_color(class_name)
        # Setting prediction results to Item() object 
        item.set_prediction_info("color", result) 
        print(result, end="\n")
        return class_name 
    
    def classify_size(self, item, model_function=None):
        """Classification funcrion for Size parameter

        Args:
            item (Item()): Item() object to be processed and classified
            model_function (Function): The function that triggers specific CNN model

        Returns:
            str: The name of the class that the object belongs to 
        """
        # Getting object's image path to be processed
        image_path = item.get_image_path()
        # Passing the image_path to the model function to be processed and saving the list results to result varible
        result = model_function(image_path)
        # getting the class_name from the result[] list
        class_name = result[1]
        # Setting the size parameter to the Item() object 
        item.set_size(class_name)
        # Setting prediction results to Item() object
        item.set_prediction_info("size", result) 
        print(result, end="\n")
        return class_name
        
    def sort(self):
        """Sorting process function
        """
        # Based on the general sorting parameter iterates throgh all items in the cassette's current item's list
        # And passing them to related classification functions (classify_color() / classify_size())
        # And sorting theme to the related gates by there indexes
        print("Starting Classification and Sorting Process", end="\n")
        if self.sorting_param == "size":
            # Importing size prediction function from size_cnn module
            print("Importing Size CNN Model", end="\n")
            from .size_cnn import size_model_predict as sp 
            print("Model imported successfully", end="\n")
            # Checking each item in the cassette's list
            print("Iterating through items in cassette's current items list", end="\n")
            for i, item in enumerate(self.cassette.items):
                item_added = False
                # Passing the items to classification function to get the class_name that the object belongs to 
                class_name = self.classify_size(item, sp)
                # Adding the item after classification to related list
                self.classified_objects.append(item)
                # Checking if the item belongs to one of two first gates 
                # These gates have a specific sort parameter
                for gate in self.gates[:2]:
                    # Getting the parameter that related to the gate and checking if it matches item's class 
                    item.index = i
                    if gate.get_param() == class_name:
                        item.set_gate(gate)
                        # If the item matches the gate, it's index in the cassette is sent to the gate waiting list  
                        gate.add_item(i)
                        item.distination = gate.position + (i * 36)
                        print(f"Item added to Gate({gate.pin}) waiting list", end="\n")
                    # If not matching, then it should be sent to "others" gate, which is the last gate in of the machine    
                        item_added = True
                        break
                    
                if not item_added:
                    item.set_gate(self.gates[-1])
                    self.gates[-1].add_item(i)
                    item.distination = gate.position + (i * 36)
                    print('Item added to "Others" Gate waiting list', end="\n")
        
        # The same algorithm is applied for other "colorsize" and "color" general sorting parameters
        
        elif self.sorting_param == "colorsize":
            print("Importing Size CNN Model", end="\n")
            from .size_cnn import size_model_predict as sp 
            print("Model imported successfully", end="\n")
            print("Importing Color CNN Model", end="\n")
            from .color_cnn import color_model_predict as cp
            print("Model imported successfully", end="\n")
            print("Iterating through items in cassette's current items list", end="\n")
            for i, item in enumerate(self.cassette.items):
                item_added = False
                size_class = self.classify_size(item, sp)
                color_class = self.classify_color(item, cp)
                mixed_param = f"{size_class}{color_class}"
                self.classified_objects.append(item)
                for gate in self.gates[:2]:
                    item.index = i
                    if gate.get_param() == mixed_param:
                        item.set_gate(gate)
                        gate.add_item(i)
                        item.distination = gate.position + (i * 36)
                        print(f"Item added to Gate({gate.pin}) waiting list", end="\n")
                        item_added = True
                        break
                
                if not item_added:
                    item.set_gate(self.gates[-1])
                    self.gates[-1].add_item(i)
                    item.distination = gate.position + (i * 36)
                    print('Item added to "Others" Gate waiting list', end="\n")
        
        else:
            print("Importing Color CNN Model", end="\n")
            from .color_cnn import color_model_predict as cp
            print("Model imported successfully", end="\n")
            print("Iterating through items in cassette's current items list", end="\n")
            for i, item in enumerate(self.cassette.items):
                item_added = False
                class_name = self.classify_color(item, cp)
                self.classified_objects.append(item)
                item.index = i
                for gate in self.gates[:2]:
                    if gate.get_param() == class_name:
                        gate.add_item(i)
                        item.set_gate(gate)
                        item.distination = gate.position + (i * 36)
                        print(f"Item added to Gate({gate.pin}) waiting list", end="\n")
                        item_added = True
                        break
                        
                if not item_added:
                    item.set_gate(self.gates[-1])
                    self.gates[-1].add_item(i)
                    item.distination = gate.position + (i * 36)
                    print('Item added to "Others" Gate waiting list', end="\n")
   
    
    def distribute(self):
        sorted_distances = sorted(item.distination for item in self.classified_objects)
        sorted_items = []
        for val in sorted_distances:
            for j, item in enumerate(self.classified_objects):
                if item.distination == val:
                    sorted_items.append(item)
                    self.classified_objects.pop(j)
        
        for item in sorted_items:
            distance = item.distination
            self.cassette.rotate(distance)
            item.gate.drop_item()
            time.sleep(1)
            for i in sorted_items:
                i.distination -= distance
        
        self.classified_objects.clear()
        self.cassette.items.clear()
        for gate in self.gates:
            gate.items.clear()
        self.cassette.origin()
        self.sort_circle = True

                
            
    # def distribute(self):
    #     """Item Distributing on the related gates after sort
    #     """
    #     # For loop to iterate on gates 
    #     print("Distributing items from cassette's current items list", end="\n")
    #     print("Iterating through gates and getting waiting lists", end="\n")
    #     for gate in self.gates:
    #         print(f"At Gate({gate.pin})", end="\n")
    #         # Set the cassette to the origin position to start with the object with index = 0
    #         self.cassette.origin()
    #         prev_index = 0
    #         # Iterating throgh indexes of objects that listed in gate.items[] list
    #         for i, item_position in enumerate(gate.items):
    #             # because of the difference between the positions of the gates and the origin position of th cassette and the sectors
    #             # The first item in the list moves to the gate directly 
    #             print(f"Moving to item {i}", end="\n")
    #             if i == 0:
    #                 # Rotating the cassette with the angle that represented as gate's position 
    #                 self.cassette.rotate((item_position * 36) + gate.position)
    #                 time.sleep(0.5)
    #             # Other item's in the list move small steps that calculated using the following formule
    #             # The rotation angle = (item's position in the cassette (index) - previous item's index) * 36° the angle between sectors (cassette feed_step)
    #             else:
    #                 # Getting the index of the item based on previous item's position 
    #                 indexed_position = item_position - prev_index
    #                 # Rotating the cassette
    #                 self.cassette.rotate(indexed_position * self.cassette.feed_step)    
    #                 time.sleep(0.5)
                
    #             # Setting the passed item's index as previous index 
    #             prev_index = item_position 
    #             # Dropping the item in the gate
    #             gate.drop_item()
    #         # Clearing gate's waiting list from items 
    #         print(f"Clearing Gate({gate.pin}) waiting list", end="\n")
    #         gate.items.clear()
    #     # Clearing Cassette's current items list
    #     print("Clearing cassette's item list", end="\n")
    #     self.cassette.clear_items()
    #     # Clearing the classified items list
    #     print("Clearing machine's classified items list", end="\n")
    #     self.classified_objects.clear()
    #     # Setting the cassette back to the origin for the next wave of items
    #     print("setting cassette to origin", end="\n")
    #     self.cassette.origin()
            
    def finish_and_report(self):
        print("Finishing and generating report", end="\n")
        """Generating a report list with data about the session

        Returns:
            List: Sorting Report that contains:
            - General sorting parameter
            - Date
            - Total objects passed to sort
            - Sorting parameter and objects counted for each gate 
            - Start and End time of sorting process
        """
        report = []
        report.append(self.session_id)
        report.append(self.date_info)
        report.append(self.start_time)
        end_time = datetime.datetime.now().strftime("%H:%M:%S")
        report.append(end_time)
        report.append(self.total_objects)
        report.append(self.sorting_param)
        for gate in self.gates:
            report.append(gate.get_param())
            report.append(gate.get_objects_quantaty())
       
        self.report = report 
    
    def get_report(self):
        """Returns a report of a session

        Returns:
            list: Session output data
        """
        return self.report
    
    def create_session_folder(self):
        """Creating a folder to store object's picture that captured during sorting session

        """
        working_dir = os.path.dirname(os.path.abspath(__file__))
        target_directory = os.path.join(working_dir, "sessions", self.session_name)
        
        if os.path.exists(target_directory):
            if not os.listdir(target_directory):
                print("Directroy already exists and empty")
                self.images_path = target_directory
                return
            else:
                index = 1
                while True:
                    new_dir_name = f"{target_directory}_{index}"
                    if not os.path.exists(new_dir_name):
                        os.mkdir(new_dir_name)
                        print(f"New directory created {new_dir_name}")
                        self.images_path = new_dir_name
                        return
                    index += 1
            
        else:
            os.mkdir(os.path.join(target_directory))
            self.images_path = target_directory
            print(f"New folder for current session created in: {target_directory}", end="\n")
            print(f"Image default path set to: {self.images_path}", end="\n")    

    def run(self):
        """A function to run the sorting machine in a loop
        """
        self.start_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.create_session_folder()
        print("Machine working cycle started", end="\n")
        prev_item_detected = False
        while True:
            item_detected = self.ir_listener()
            if self.sort_circle:
                break
            if item_detected:
                prev_item_detected = item_detected  
                self.feed()
            else:
                
                self.timer(15)
                if self.timer_interrupted:
                    prev_item_detected = item_detected
                    self.feed()
                    self.timer_interrupted = False
                else:
                    if prev_item_detected:
                        self.sort()
                        self.distribute()
                        self.finish_and_report()
                        break
                    else:
                        self.finish_and_report()
                        break
                         
        