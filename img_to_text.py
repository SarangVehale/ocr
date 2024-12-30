import cv2
import pytesseract
import os
import sys
import platform
import pyttsx3

def get_tesseract_path():
    """Dynamically determine Tesseract path based on operating system."""
    system = platform.system().lower()
    paths = {
        'windows': r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        'darwin': '/usr/local/bin/tesseract',
        'linux': '/usr/bin/tesseract'
    }
    return paths.get(system, 'tesseract')

def validate_image_path(image_path):
    """Validate and normalize image path."""
    image_path = os.path.expanduser(image_path)
    if not os.path.exists(image_path):
        print(f"Error: Image path '{image_path}' does not exist.")
        return None
    return image_path

def extract_text_from_image(image_path):
    """Extract text from image using Tesseract OCR."""
    pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

    try:
        # Read image
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Could not read image: {image_path}")
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Thresholding
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Create output directory
        os.makedirs('ocr_outputs', exist_ok=True)

        # Perform OCR
        text = pytesseract.image_to_string(binary)

        # Save preprocessed image
        cv2.imwrite('ocr_outputs/preprocessed_image.jpg', binary)

        # Save extracted text
        with open('ocr_outputs/extracted_text.txt', 'w', encoding='utf-8') as f:
            f.write(text)

        return text

    except Exception as e:
        print(f"Error in text extraction: {e}")
        return None

def speak_text(text):
    """Convert text to speech using pyttsx3."""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1)
        
        print("\nSpeaking the extracted text...")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")

def get_user_image_path():
    """Prompt user for image path with cross-platform support."""
    while True:
        image_path = input("Enter the full path to the image: ").strip()
        validated_path = validate_image_path(image_path)
        
        if validated_path:
            return validated_path
        
        choice = input("Would you like to try again? (y/n): ").lower()
        if choice != 'y':
            sys.exit()

def main():
    print("🖼️ OCR Text Extraction Tool 🔍")
    print("------------------------------")

    # Get image path from user
    image_path = get_user_image_path()

    # Extract text
    extracted_text = extract_text_from_image(image_path)

    # Process and speak text
    if extracted_text:
        print("\n--- Extracted Text ---")
        print(extracted_text)

        # Optional: Text-to-Speech
        speak_option = input("Would you like to hear the text? (y/n): ").lower()
        if speak_option == 'y':
            speak_text(extracted_text)
    else:
        print("No text could be extracted.")

if __name__ == "__main__":
    main()

