import os
import re
import json
import openai
import time

def get_response(userText, chat_history, name, chatgpt_output,impersonated_role, explicit_input, history_file):
    return chat(userText,chat_history, name, chatgpt_output,impersonated_role, explicit_input, history_file)


def parse_discussion(discussion):
    user_messages = re.findall(r'\d+/\d+ \d+:\d+:\d+ User: (.+)', discussion)
    bot_messages = re.findall(r'\d+/\d+ \d+:\d+:\d+ BOT: (.+)', discussion)

    # Merge user and bot messages while keeping their order
    discussion_pairs = list(zip(user_messages, bot_messages))

    return discussion_pairs

def chat(user_input, chat_history, name, chatgpt_output,impersonated_role, explicit_input, history_file):
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    chatgpt_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:', '')
    chatgpt_output = f'{name}: {chatgpt_raw_output}'
    chat_history += chatgpt_output + '\n'
    with open(history_file, 'a') as f:
        f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' +  chatgpt_output + '\n')
        f.close()
    return chatgpt_raw_output,chat_history


def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": f"{impersonated_role}. Conversation history: {chat_history}"},
            {"role": "user", "content": f"{user_input}. {explicit_input}"},
        ]
    )

    for item in output['choices']:
        chatgpt_output = item['message']['content']

    return chatgpt_output
def get_history_list(path):
    path_list = os.listdir(path)
    content = {}

    for file_name in path_list:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):  # Check if it's a file
            with open(file_path, 'r') as file:
                file_content = file.read()
            i = int(file_name.split('chat_history')[1].split('.txt')[0])
            content[i] = file_content
    return content
def create_chat(path):
    i = 1
    # Find an available chat history file
    while os.path.exists(os.path.join(path, f'chat_history{i}.txt')):
        i += 1
    history_file = os.path.join(path, f'chat_history{i}.txt')
    return history_file
