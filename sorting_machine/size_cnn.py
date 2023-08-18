import keras # TensorFlow is required for Keras to work
import PIL as pil   # Pillow [PIL] library to manipulate with images
import numpy as np # NumPy to manipulate with image matrix

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = keras.models.load_model("./size_model.h5", compile=False)

# Load the labels
class_names = open("./size_labels.txt", "r").readlines()


def size_model_predict(img_path):
    '''
    - Input: Path of th Image to be processed by the CNN model
    - Returns : A list of parameters:
        - [0] class index 
        - [1] class_name 
        - [2] confidence_score
    '''
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = pil.Image.open(img_path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = pil.ImageOps.fit(image, size, pil.Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    # print("Class:", class_name[2:], end="")
    # print("Confidence Score:", confidence_score)

    return [index, class_name, confidence_score]





