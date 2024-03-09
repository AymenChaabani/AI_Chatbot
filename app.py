# Import necessary libraries
from flask import Flask, render_template, request, redirect,url_for,jsonify
import openai
import os
import time
from utils import *
# Set the OpenAI API key
openai.api_key = ""

# Define the name of the bot
name = 'BOT'


# Define the impersonated role with instructions
impersonated_role = ""

# Initialize variables for chat history
explicit_input = ""
chatgpt_output = 'Chat log: /n'
cwd = r"C:\Users\aymen\Desktop\chaatbot\Flask-OpenAI-Chatbot-main\chat_history"
# Create a new chat history file

# Initialize chat history
chat_history = ''
history_file = ''
discussion_list = {}
# Create a Flask web application
app = Flask(__name__)

# Function to complete chat input using OpenAI's GPT-3.5 Turbo

# Function to handle user chat input

# Function to get a response from the chatbot

# Define app routes
@app.route("/")
def index():
    return render_template("root.html")
@app.route("/new_discussion")
def index2():
    global cwd,history_file
    history_file = create_chat(cwd)
    with open(history_file, 'w') as f:
        f.write('\n')
    return render_template("new_discussion.html")

@app.route("/get")
# Function for the bot response

def get_bot_response():
    global chat_history
    userText = request.args.get('msg')
    response,chat_history = get_response(userText, chat_history, name, chatgpt_output,impersonated_role, explicit_input, history_file)
    return str(response)

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')
@app.route('/discussion_list')
def discussion_list():
    global discussion_list
    discussion_list = get_history_list(cwd + '/')
    return render_template('discussion_list.html', discussions = discussion_list)
@app.route('/delete', methods=['POST'])
def delete_discussion():
    global discussion_list, chat_history
    discussion_list = get_history_list(cwd + '/')
    key = (int(request.form['key'][1]),int(request.form['key'][4]))
    print(key)
    if key[0] == 0 :
        key_to_delete = key[1]
        file_to_delete = os.path.join(cwd,  f'chat_history{key_to_delete}.txt')
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
        discussion_list = get_history_list(cwd + '/')

        return render_template('discussion_list.html',discussions = discussion_list)
    else :
        key_to_load= key[1]
        file_to_load = os.path.join(cwd, f'chat_history{key_to_load}.txt')
        with open(file_to_load, "r") as file:
            content = file.read()
        data=parse_discussion(content)
        chat_history = content
        return render_template('new_discussion.html')



# Run the Flask app
if __name__ == "__main__":
    app.run()
