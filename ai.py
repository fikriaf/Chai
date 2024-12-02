import requests, json
import spacy
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

nlp = spacy.load("en_core_web_sm")

conn = sqlite3.connect("users.db")

# Define a function to extract the user's intent from their input
def extract_intent(input_text):
    doc = nlp(input_text)
    for token in doc:
        if token.pos_ == "VERB":
            return token.lemma_
    return None

# Define a function to preprocess the input using a TF-IDF vectorizer
def preprocess_input(input_text):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([input_text])
    return X

# Define a function to generate a response using an SVM model
def generate_response(input_text, user_id):
    clf = SVC(kernel="linear")
    train_data = get_user_conversations(user_id)
    if len(train_data) == 0:
        train_data = [
            ("What time is it?", "I don't know."),
            ("What's the weather like?", "I don't know."),
            ("How old are you?", "I'm a chatbot, I don't have an age."),
            ("What's your name?", "My name is Chatbot.")
        ]
    X_train = vectorizer.fit_transform([example[0] for example in train_data])
    y_train = [example[1] for example in train_data]
    clf.fit(X_train, y_train)
    X_test = preprocess_input(input_text)
    y_pred = clf.predict(X_test)
    return y_pred[0]

# Define a function to handle the user's input and generate a response
def handle_input(user_input, user_id):
    intent = extract_intent(user_input)
    if intent == "greet":
        return "Hello! How can I assist you today?", None
    elif intent == "farewell":
        return "Goodbye! Have a great day.", None
    elif intent == "question":
        response = generate_response(user_input, user_id)
        if response == "I don't know.":
            return "I'm sorry, I don't have an answer to that question.", None
        else:
            save_user_conversation(user_id, user_input, response)
            return response, user_id
    else:
        return "I'm sorry, I didn't understand your input. Please try again.", None

# Define a function to store and retrieve user information in a SQLite database
def create_table():
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    conn.execute("CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY, user_id INTEGER, input TEXT, response TEXT)")

def insert_user(name, age):
    conn.execute(f"INSERT INTO users (name, age) VALUES ('{name}', {age})")
    conn.commit()

def get_user_by_name(name):
    cursor = conn.execute(f"SELECT * FROM users WHERE name='{name}'")
    row = cursor.fetchone()
    if row is not None:
        return {"id": row[0], "name": row[1], "age": row[2]}
    else:
        return None

def save_user_conversation(user_id, input_text, response):
    conn.execute(f"INSERT INTO conversations (user_id, input, response) VALUES ({user_id}, '{input_text}', '{response}')")
    conn.commit()

def get_user_conversations(user_id):
    cursor = conn.execute(f"SELECT * FROM conversations WHERE user_id={user_id}")
    rows = cursor.fetchall()
    return [(row[2], row[3]) for row in rows]

# Define a function to handle the user's input and generate a response
def handle_input(user_input, user_id):
    intent = extract_intent(user_input)
    if intent == "greet":
        return "Hello! How can I assist you today?", None
    elif intent == "farewell":
        return "Goodbye! Have a great day.", None
    elif intent == "question":
        response = generate_response(user_input, user_id)
        if response == "I don't know.":
            return "I'm sorry, I don't have an answer to that question.", None
        else:
            save_user_conversation(user_id, user_input, response)
            return response, user_id
    else:
        return "I'm sorry, I didn't understand your input. Please try again.", None

# Define a function to handle the user's input and maintain state across multiple conversations
def chat():
    create_table()
    user_id = None
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        if user_id is not None:
            user = get_user_by_id(user_id)
            print(f"{user['name']}: ", end="")
        response, new_user_id = handle_input(user_input, user_id)
        if new_user_id is not None:
            user_id = new_user_id
            user = get_user_by_id(user_id)
            print(f"Welcome back, {user['name']}! ", end="")
        print(f"{response}")

chat()

