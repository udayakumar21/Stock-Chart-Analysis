import cv2
import pytesseract
from pytesseract import Output

# Set the path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to check if a string can be converted to a float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# Function to extract values from an image
def extract_values_from_image(filepath):
    # Read the image using OpenCV
    image = cv2.imread(filepath)

    # Convert the image to grayscale
    BWimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Tesseract configuration with Page segmentation mode and Engine mode
    myconfig = r"--psm 11 --oem 3"

    # Perform OCR on the preprocessed image
    data = pytesseract.image_to_data(BWimage, config=myconfig, output_type=Output.DICT)

    extracted_data = []
    amount_boxes = len(data['text'])

    for i in range(amount_boxes):
        if float(data['conf'][i]) > 45:
            text = data['text'][i]

            # Check if the text starts with "P" or "L" and is short (less than 4 characters)
            if (("P" in text) or ("L" in text)) and len(text) < 4:
                x, y, width, height = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                answers = [text]
                x_axis, y_axis = 0, 0

                for j in range(amount_boxes):
                    if (x_axis == 1 and y_axis == 1):
                        break

                    for k in range(20, 100, 10):
                        # Checking for the closest value in the price axis
                        if (y_axis == 1):
                            break

                        # Check if the position of the text suggests it's on the price axis
                        if (x + 40 < data["left"][j]) and (y >= data["top"][j] - k and y <= data["top"][j] + (k / 5)):
                            # Check if the text can be converted to a float and is greater than 0.05
                            if isfloat(data["text"][j]) and (float(data["text"][j]) > 0.05):
                                answers.append(data['text'][j])
                                y_axis = 1
                                break

                    for k in range(20, 100, 10):
                        # Checking for the closest value in the time axis
                        if (x_axis == 1):
                            break

                        # Check if the position of the text suggests it's on the time axis
                        if (y < data["top"][j]) and (x >= data["left"][j] - k and x <= data["left"][j] + k):
                            # Check if the text can be converted to a float
                            if isfloat(data["text"][j]):
                                answers.append(data['text'][j])
                                x_axis = 1
                                break

                # If we found at least 2 relevant answers, add them to the extracted data
                if len(answers) >= 2:
                    extracted_data.append(answers)

    return extracted_data

def main():
    # Specify the path to the image you want to process
    image_path = "AssignmentImage-1.png"
    #image_path = "AssignmentImage-2.png" 

    # Extract values from the image
    extracted_values = extract_values_from_image(image_path)
    
    if not extracted_values:
        print("No relevant values extracted.")
    else:
        for i, values in enumerate(extracted_values, 1):
            print(f"Set {i}: {', '.join(values)}")

if __name__ == "__main__":
    main()
