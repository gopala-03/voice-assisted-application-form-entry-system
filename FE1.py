import pyttsx3
import speech_recognition as sr
import re
import time
from PIL import Image
import pytesseract
from fuzzywuzzy import fuzz

# Path to the Tesseract executable (update this to the correct path on your system)
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/LALITH VARMA/Dropbox/My PC (LAPTOP-MAB3T823)/Desktop/NITK/tesseract.exe'

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return str(e)

def speak_text(text, language="en"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', language)
    engine.say(text)
    engine.runAndWait()

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak...")
        audio = recognizer.listen(source, timeout=10)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Could not request results"

def generate_question(field_name):
    # Generate a question based on the field name
    return f"Please tell me your {field_name}."

if __name__ == "__main__":
    image_path = "C:/Users/LALITH VARMA/Dropbox/My PC (LAPTOP-MAB3T823)/Desktop/NITK/Try2.png"
    extracted_text = extract_text_from_image(image_path)
    print("Extracted Text:", extracted_text)

    # Identify form fields based on keywords
    form_fields = []
    if re.search(r"\bfull name\b", extracted_text, re.IGNORECASE):
        form_fields.append("full name")
    if re.search(r"\bgender\b", extracted_text, re.IGNORECASE):
        form_fields.append("gender")
    if re.search(r"\bdate of birth|dale of birth\b", extracted_text, re.IGNORECASE):
        form_fields.append("date of birth")
    if re.search(r"\bphone number\b", extracted_text, re.IGNORECASE):
        form_fields.append("phone number")
    if re.search(r"\bemail\b", extracted_text, re.IGNORECASE):
        form_fields.append("email")
    if re.search(r"\bfather name\b", extracted_text, re.IGNORECASE):
        form_fields.append("father name")
    if re.search(r"\bmother name\b", extracted_text, re.IGNORECASE):
        form_fields.append("mother name")
    if re.search(r"\baddress\b", extracted_text, re.IGNORECASE):
        form_fields.append("address")
    # Add more field checks as needed

    if not form_fields:
        print("No form fields found in the extracted text.")

    speak_text("Welcome! Let's fill out the form.")
    time.sleep(1)

    answers = {}
    for field in form_fields:
        question = generate_question(field)
        speak_text(question)
        user_response = get_voice_input()

        # Gender recognition
        if field == "gender":
            expected_genders = ["male", "female"]
            best_match_gender = max(expected_genders, key=lambda gender: fuzz.ratio(user_response.lower(), gender))
            user_response = best_match_gender

        # Date of Birth formatting
        if field == "date of birth":
            # Use regular expressions to reformat the date if necessary
            user_response = re.sub(r'\b(\d{1,2})[ /-](\d{1,2})[ /-](\d{4})\b', r'\1/\2/\3', user_response)

        # Email address recognition
        if field == "email":
            # Check if "@" is missing and add it
            if " at " in user_response:
                user_response = user_response.replace(" at ", "@")
            elif " at the rate of " in user_response:
                user_response = user_response.replace(" at the rate of ", "@")

        # Address formatting
        if field == "address":
            # Replace "dash" with "-"
            user_response = user_response.replace(" dash ", "-")

        answers[field] = user_response

    speak_text("Thank you for filling out the form. Here are your answers:")
    for field, answer in answers.items():
        print(f"{field.capitalize()}: {answer}")
        speak_text(f"Your {field} is: {answer}")

    # Ask the user if they want to print the form
    speak_text("Do you want to print the form? Please say yes or no.")
    user_response = get_voice_input().lower()

    if user_response == "yes":
        print("Printing the form:")
        for field, answer in answers.items():
            print(f"{field.capitalize()}: {answer}")
        speak_text("Form printed successfully.")
    elif user_response == "no":
        speak_text("Alright, the form will not be printed.")
    else:
        speak_text("Sorry, I didn't understand your response.")
