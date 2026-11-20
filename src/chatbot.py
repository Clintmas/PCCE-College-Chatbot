
import joblib
import random

from pathlib import Path

from src.preprocess import preprocess_text
from src.database import get_college_detail, get_all_courses


# 1. Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "chatbot_model.pkl"


# 2. Load the trained ML model
saved_data = joblib.load(MODEL_PATH)

model = saved_data["model"]
vectorizer = saved_data["vectorizer"]


# 3. Define a confidence threshold
CONFIDENCE_THRESHOLD = 0.15


# 4. Predict the user's intent

def predict_intent(user_input):

    cleaned_text = preprocess_text(user_input)

    print("Original question:", user_input)
    print("Cleaned question:", cleaned_text)

    numerical_text = vectorizer.transform([cleaned_text])

    probabilities = model.predict_proba(numerical_text)[0]

    best_index = probabilities.argmax()

    predicted_intent = model.classes_[best_index]

    confidence = probabilities[best_index]

    print("Predicted intent:", predicted_intent)
    print("Confidence:", round(confidence * 100, 2), "%")

    if confidence < CONFIDENCE_THRESHOLD:
        print("Result: Unknown (below threshold)")
        return "unknown"

    return predicted_intent



# 5. Retrieve course information
def get_courses_response():

    courses = get_all_courses()

    if not courses:
        return "Sorry, course information is currently unavailable."

    response = "The courses offered at PCCE are:\n"

    for course, level in courses:
        response += f"\n• {course} ({level})"

    return response


# 6. Retrieve contact information
def get_contact_response():

    email = get_college_detail("email")
    phone = get_college_detail("administration_phone")

    return (
        f"College Email: {email}\n"
        f"Administration Phone: {phone}"
    )


# 7. Generate the chatbot response
def generate_response(intent):

    # Map predicted intents to database topics
    database_mapping = {
        "college_info": "about_college",
        "affiliation_enquiry": "affiliation",
        "admission_enquiry": "admission_process",
        "eligibility_enquiry": "admission_eligibility",
        "fee_enquiry": "fees",
        "hostel_enquiry": "hostel",
        "transport_enquiry": "transport",
        "library_enquiry": "library",
        "placement_enquiry": "placements",
        "location_enquiry": "address"
    }

    # Special handling for course enquiries
    if intent in ["course_enquiry", "department_enquiry"]:
        return get_courses_response()

    # Special handling for contact enquiries
    if intent == "contact_enquiry":
        return get_contact_response()

    # Handle database-based enquiries
    if intent in database_mapping:

        topic = database_mapping[intent]

        answer = get_college_detail(topic)

        if answer:
            return answer

        return "Sorry, I don't have that information right now."

    # Handle greetings
    if intent == "greeting":
        return (
            "Hello! Welcome to Padre Conceicao College of Engineering. "
            "How can I help you?"
        )

    # Handle goodbye
    if intent == "goodbye":
        return "Thank you for contacting PCCE. Have a great day!"

    # Handle thanks
    if intent == "thanks":
        return "You're welcome! Feel free to ask me anything about PCCE."

    # Handle unknown questions
    return (
    "Sorry, I couldn't understand your question. "
    "I can help you with PCCE-related enquiries such as "
    "courses, admissions, fees, eligibility, hostel, "
    "transport, library and placements. "
    "Please try asking me something related to the college."
)


# 8. Main chatbot function
def chatbot_reply(user_input):

    if not user_input or not user_input.strip():
        return "Please enter a question."

    intent = predict_intent(user_input)

    response = generate_response(intent)

    return response


# 9. Test chatbot directly
if __name__ == "__main__":

    print("PCCE College Enquiry Chatbot")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nYou: ")

        if question.lower().strip() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        answer = chatbot_reply(question)

        print("Chatbot:", answer)
