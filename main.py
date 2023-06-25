import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font as tkfont
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

# Initialize NLTK and SpaCy variables
nltk.download('stopwords')
nltk.download('wordnet')
nlp = spacy.load('en_core_web_sm')

# Initialize WordNet lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to the Preprocess text
def preprocess(text):
    # Tokenize text
    tokens = nltk.word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
    
    # Lemmatize tokens
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return tokens

# Generate a response based on the user's input
def generate_response(message):
    # Preprocess the user's message
    tokens = preprocess(message)
    
    # Check if any specific keywords or phrases are present in the tokens
    if 'documents' in tokens or 'files' in tokens:
        response = "Sure, I can help you with that. Please provide the necessary documents."
    elif 'chase' in tokens or 'follow up' in tokens:
        response = "I will follow up with the client to request the documents."
    elif 'check' in tokens or 'verify' in tokens:
        response = "Let me verify the documents for you."
    elif message.startswith('find me '):
        prefix = message.replace('find me ', '').strip()
        matching_files = find_files_starting_with(prefix)
        if matching_files:
            # Store the matching files in a global variable
            global retrieved_files
            retrieved_files = matching_files
            response = "Here are the files starting with '{}':\n".format(prefix)
            for i, file in enumerate(matching_files, start=1):
                response += "{}) {}\n".format(i, file)
            response += "Please enter the file number to open it or type 'open' followed by the file name."
        else:
            response = "No files starting with '{}' found.".format(prefix)
    elif message.lower() == 'cancel':
        retrieved_files.clear()
        response = "File retrieval canceled."
    elif message.lower().startswith('open '):
        file_name = message.replace('open ', '').strip()
        matching_files = [file for file in retrieved_files if file.lower().startswith(file_name.lower())]
        if matching_files:
            if len(matching_files) == 1:
                file_path = os.path.join(os.getcwd(), matching_files[0])
                if os.path.isfile(file_path):
                    open_file(file_path)
                    response = "Opening the file."
                else:
                    response = "The file does not exist."
            else:
                response = "Multiple files match the given name. Please specify the file number."
        else:
            response = "No files matching the given name found."
    elif message.isdigit() and retrieved_files:
        file_index = int(message)
        if file_index > 0 and file_index <= len(retrieved_files):
            file_path = os.path.join(os.getcwd(), retrieved_files[file_index - 1])
            if os.path.isfile(file_path):
                open_file(file_path)
                response = "Opening the file."
            else:
                response = "The file does not exist."
        else:
            response = "Invalid file number."
    else:
        response = "I'm sorry, I cannot help with that request."

    return response

# Find files starting with the specified prefix
def find_files_starting_with(prefix):
    matching_files = []
    current_dir = os.getcwd()
    for file in os.listdir(current_dir):
        if file.lower().startswith(prefix.lower()):
            matching_files.append(file)
    return matching_files

# Open the file using the default associated program
def open_file(file_path):
    os.startfile(file_path)

# Function to handle the "Send" button click event
def send_message():
    user_input = user_input_text.get("1.0", tk.END).strip()

    # Clear the user input field
    user_input_text.delete("1.0", tk.END)

    # Append user input to the chat history
    chat_history_text.configure(state='normal')
    chat_history_text.insert(tk.END, "You: " + user_input + "\n")

    # Generate response
    response = generate_response(user_input)

    # Append chatbot response to the chat history
    chat_history_text.insert(tk.END, "Chatbot: " + response + "\n")

    # Disable chat history text widget
    chat_history_text.configure(state='disabled')

# Function to handle sending message on Enter key press
def send_message_on_enter(event):
    send_message()

def toggle_dark_mode():
    if dark_mode.get():
        # Dark Mode
        window.configure(background='#212121')
        text_bg_color = '#424242'
        text_fg_color = '#FFFFFF'
        button_bg_color = '#FFFFFF'
        button_fg_color = '#000000'
    else:
        # Light Mode
        window.configure(background='#F2F2F2')
        text_bg_color = '#FFFFFF'
        text_fg_color = '#000000'
        button_bg_color = '#1E90FF'
        button_fg_color = '#000000'

    # Update the text field colors
    chat_history_text.configure(bg=text_bg_color, fg=text_fg_color)
    user_input_text.configure(bg=text_bg_color, fg=text_fg_color)

    # Update the button colors
    style.configure('SendButton.TButton', background=button_bg_color, foreground=button_fg_color)

# Create the GUI
window = tk.Tk()
window.title("AI Chatbot")

# Set the window minimum size
window.minsize(500, 400)

# Configure the default color scheme (Light Mode)
window.configure(background='#F2F2F2')
text_bg_color = '#FFFFFF'
text_fg_color = '#000000'
button_bg_color = '#1E90FF'
button_fg_color = '#000000'

# Create a custom font style for the chat history and user input
chat_font = tkfont.Font(family="Arial", size=12)

# Create the chat history display
chat_history_text = scrolledtext.ScrolledText(window, state='disabled', font=chat_font, wrap='word', bg=text_bg_color, fg=text_fg_color)
chat_history_text.pack(fill='both', expand=True, padx=10, pady=(10, 0))

# Create the user input field
user_input_text = tk.Text(window, height=4, font=chat_font, bg=text_bg_color, fg=text_fg_color)
user_input_text.pack(fill='x', padx=10, pady=10)

# Create a frame to hold the send button and dark mode toggle button
button_frame = tk.Frame(window, bg=window.cget('background'))
button_frame.pack(fill='x', padx=10, pady=(0, 10), anchor='s')

# Create the send button
send_button = ttk.Button(button_frame, text="Send", command=send_message, style='SendButton.TButton')
send_button.pack(side='right', padx=(5, 0))

# Create the dark mode toggle button
dark_mode = tk.BooleanVar()
dark_mode_toggle = ttk.Checkbutton(button_frame, text="Dark Mode", variable=dark_mode, command=toggle_dark_mode)
dark_mode_toggle.pack(side='left', padx=(0, 5))

# Style the send button
style = ttk.Style()
style.configure('SendButton.TButton', background=button_bg_color, foreground=button_fg_color)

# Display the introductory message
chat_history_text.configure(state='normal')
chat_history_text.insert(tk.END, "Chatbot: Hello, how can I help?\n")
chat_history_text.configure(state='disabled')

# Bind the Enter key to send the message
user_input_text.bind('<Return>', send_message_on_enter)

# Run the GUI event loop
window.mainloop()
