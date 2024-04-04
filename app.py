# Import necessary libraries
from flask import Flask, render_template, request, jsonify, send_file
import requests
import speech_recognition as sr
import pyttsx3
import os
import time

# Initialize Flask app
app = Flask(__name__)

# Define a flag to control question generation
generating_question = False

@app.route('/')
def index():
    return render_template('index.html')

# Define API keys and global variables
api_key = 'YOUR_API_KEY'
api_key2 = 'YOUR_API_KEY'
api_secret = 'YOUR_API_KEY'
current_question_index = 0
questions = []
user_answers = []
x=''
str=['arrays','linked lists','stacks','trees','graphs','queues','hashing','heaps','algorithm analysis','advanced data structures']
diff=['easy','medium','hard']

# Store the start time of the quiz
quiz_start_time = None

# Define base URL for Gemini API
base_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key

# Function to make requests to Gemini API
def make_gemini_request(prompt, method='POST'):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    url = base_url
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

# Route to generate a question
def generate_question_audio(question_text, question_index):
    engine = pyttsx3.init()
    engine.save_to_file(question_text, f'static/question_{question_index}.mp3')
    engine.runAndWait()

# Route to generate a question
@app.route('/generate_question')
def generate_question():
    global current_question_index, k, generating_question, d, quiz_start_time
    # Start the timer when the quiz begins
    if quiz_start_time is None:
        quiz_start_time = time.time()  # Record the current time as the start time of the quiz
    if not generating_question and current_question_index < 10:
        generating_question = True
        if 'k' not in globals():
            k = 0  
            d = 0
        try:
            question_response = make_gemini_request("Ask an "+diff[d]+" question(without answer) about data structures only from the topic "+str[k])
            print(str[k],diff[d])
            k += 1
            try:
                question_text = question_response['candidates'][0]['content']['parts'][0]['text']
                questions.append(question_text)
                current_question_index += 1
                generate_question_audio(question_text, current_question_index)
                generating_question = False 
                return jsonify({'question': question_text})  # Return the question text
            except IndexError:
                generating_question = False
                return jsonify({'error': 'Unable to access question text'})
        except requests.exceptions.RequestException as e:
            generating_question = False
            return jsonify({'error': 'Unable to generate question'})
    else:
        return jsonify({'error': 'Question generation in progress or quiz completed'})

#Adjust difficulty
def adjust_difficulty():
    global d
    if mark<=2:
        if d==1:
            d=0
        elif d==2:
            d=1
    elif mark>3:
        if d==0:
            d=1
        elif d==2:
            d=2

# Route to evaluate user answer
@app.route('/evaluate_answer', methods=['POST'])
def evaluate_answer():
    global current_question_index, sum, mark
    data = request.get_json()
    user_answer = data.get('user_answer')

 
    evaluation_response = make_gemini_request(f"Evaluate the correctness of following answer: {user_answer} for the question: {questions[current_question_index - 1]}. Provide the correct answer for the {questions[current_question_index - 1]}.")
    evaluation_score = make_gemini_request(f"Assign a score out of 5 for the following answer: {user_answer} to the question: {questions[current_question_index - 1]} based on its correctness")

    if not evaluation_response or 'candidates' not in evaluation_response:
        return jsonify({'error': 'Unable to evaluate answer'})
    if not evaluation_score or 'candidates' not in evaluation_score:
        return jsonify({'error': 'Unable to evaluate answer'})

    score = evaluation_score['candidates'][0]['content']['parts'][0]['text']
    feedback = evaluation_response['candidates'][0]['content']['parts'][0]['text']

    if 'sum' not in globals():
        sum = 0
        
    for x in score:              #extracting the first digit bcoz that will be the score
        if x.isdigit():
            break    
    sum+=int(x)
    mark=int(x)
    print(mark)
    adjust_difficulty()
    return jsonify({'feedback': feedback, 'score': score})

# Route to fetch question audio
@app.route('/question_audio')
def question_audio():
    global current_question_index
    if current_question_index <= 10:
        question_audio_path = f'static/question_{current_question_index}.mp3'
        if os.path.exists(question_audio_path):
            return send_file(question_audio_path, as_attachment=True)
    return jsonify({'error': 'Question audio not found'})

# Route to receive user audio answer
@app.route('/receive_audio', methods=['POST'])
def receive_audio():
    audio_data = request.files['audio_data']
    with open(f'user_answer_{current_question_index}.wav', 'wb') as f:
        f.write(audio_data.read())
    recognizer = sr.Recognizer()
    with sr.AudioFile(f'user_answer_{current_question_index}.wav') as source:
        audio_data = recognizer.record(source)
        user_answer = recognizer.recognize_google(audio_data)
    return jsonify({'user_answer': user_answer})

# Route to calculate final score
@app.route('/final_score')
def calculate_final_score():
    global sum, quiz_start_time
    final_score = sum if 'sum' in globals() else 0
    return jsonify({'final_score': final_score})

# Add a route to start the timer when the quiz starts
@app.route('/start_timer', methods=['GET'])
def start_timer():
    global quiz_start_time,sum
    final_score = sum if 'sum' in globals() else 0
    if quiz_start_time is not None:
        total_time_seconds = int(time.time() - quiz_start_time)  # Calculate the total time in seconds
        return jsonify({'final_score': final_score, 'total_time_seconds': total_time_seconds})
    else:
        return jsonify({'error': 'Timer not started'})
    quiz_start_time = time.time()  # Record the current time as the start time of the quiz
    return jsonify({'message': 'Timer started'})

# Add a route to stop the timer and calculate the total time when the quiz ends
@app.route('/stop_timer', methods=['GET'])
def stop_timer():
    global quiz_start_time
    if quiz_start_time is not None:
        total_time_seconds = int(time.time() - quiz_start_time)  # Calculate the total time in seconds
        return jsonify({'total_time_seconds': total_time_seconds})
    else:
        return jsonify({'error': 'Timer not started'})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
