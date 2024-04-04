<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Question Generator</title>
    <link rel="stylesheet" href="static/styles.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="start-container">
        <button id="startButton" onclick="startTest()">
            <i class="fa-regular fa-circle-play fa-7x"></i>
        </button>
    </div>
    <div class="title" style="display: none;">
        <span id="questionNumber"></span>
        <h1>Data Structures Question</h1>
        <span id="timer"></span>
    </div>
    <div class="question-container" style="display: none;">
        <h1 id="question"></h1>
        <div class="blk">
            <label for="userAnswer">Your Answer:</label>
            <textarea id="userAnswer"></textarea>
            <div class="btn-container">
                <button id="recordButton" onclick="recordAnswer()">Record Answer</button>
            </div>
        </div>
        <div id="feedback" onclick="openFeedbackPopup()"></div>
        <button id="nextButton" onclick="nextQuestion()">
            <i class="fas fa-forward fa-2x"></i>
        </button>
        <div id="feedbackPopup" class="feedback-popup">
            <div class="feedback-popup-content">
                <span class="close" onclick="closeFeedbackPopup()">&times;</span>
                <div id="feedbackPopupContent"></div>
            </div>
        </div>
        
    </div>
    <audio id="questionAudio" autoplay></audio>
    <div id="otherfeedback" style="display: none;"></div>
    <div id="endPage" style="display: none;">
        <h1>Quiz Completed!</h1>
        <h2>Your Final Score: <span id="finalScore"></span>/50</h2>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.2/dist/confetti.browser.min.js"></script>
    <script>
        let questionIndex = 1;
        let startTime = Date.now();

        function startTest() {
            document.querySelector('.start-container').style.display = 'none';
            document.querySelector('.title').style.display = 'flex';
            document.querySelector('.question-container').style.display = 'block';
            // Call the function to generate the first question
            generateQuestion();

        }

        function generateQuestion() {
            fetch('/generate_question')
            .then(response => response.json())
            .then(data => {
                // Check if quiz is completed after generating each question
                if (questionIndex > 10) {
                    showEndPage(); // Show end page if quiz is completed
                    return;
                }
                document.getElementById('recordButton').disabled = false;     
                document.getElementById('feedback').innerText = '';
                document.getElementById('questionNumber').innerText = `${questionIndex}/10`;
                document.getElementById('question').innerText = data.question;
                document.getElementById('questionAudio').src = `/question_audio?${Date.now()}`;
                document.getElementById('questionAudio').play();
                startTime = Date.now(); // Reset timer
                startTimer(); // Start timer for 45 seconds
                document.getElementById('nextButton').style.display = 'block';
            })
            .catch(error => console.error('Error:', error));
        }

        function showEndPage() {
            // Hide question container and show end page
            document.querySelector('.question-container').style.display = 'none';
            document.getElementById('endPage').style.display = 'block';

            throwConfetti();

            // Fetch final score and display it
            fetch('/final_score')
            .then(response => response.json())
            .then(data => {
                document.getElementById('finalScore').innerText = data.final_score;
            })
            .catch(error => console.error('Error:', error));
        }


        function startTimer() {
            let timerElement = document.getElementById('timer');
            let duration = 45; // Time duration in seconds
            let timerInterval = setInterval(function() {
                let elapsed = Math.floor((Date.now() - startTime) / 1000);
                let remainingSeconds = duration - elapsed;
                let minutes = Math.floor(remainingSeconds / 60);
                let seconds = remainingSeconds % 60;
                
                let formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}s`;
                
                if (remainingSeconds < 0) {
                    clearInterval(timerInterval);
                    // Automatically evaluate answer when time's up
                    document.getElementById('feedback').innerText = '';
                    document.getElementById("feedbackPopup").style.display = "none";        //close feedback popup if open
                    nextQuestion();
                } else {
                    timerElement.innerText = formattedTime;
                }
            }, 1000);
        }

        //to record answer when record button is clicked
        function recordAnswer() {                    
            document.getElementById('feedback').innerText = '';                  //first clear feedback box coz it may have something in some cases
            var recognition = new webkitSpeechRecognition();           
            recognition.onresult = function(event) {                             //speech recognition function
                var transcript = event.results[0][0].transcript;                 //getting the transcript of audio i.e storing the text of audio in transcript 
                document.getElementById('userAnswer').value = transcript;        //set the user answer box with the transcript
                evaluateAnswer(transcript);                                      //evaluating the transcript
            };
            recognition.start();
            
            // Set a timeout to handle cases where no speech is detected
            setTimeout(function() {     
                recognition.stop();
                if (document.getElementById('userAnswer').value === '') {                 // if the box has no content i.e it is empty
                    document.getElementById('feedback').innerText = "Sorry, couldn't hear anything. Try again";
                    document.getElementById('nextButton').style.display = 'block';         // Show next button
                    document.getElementById('recordButton').disabled = false;        //enable record button
                }else{
                    document.getElementById('recordButton').disabled = true;         // Disable record button if answer is provided
                }
            }, 10000);      // 10 seconds timeout-within 10 seconds if nothing appears in the feedback box, then display the message
        }



        function evaluateAnswer(userAnswer) {
            
            // If there is a user answer, proceed with the evaluation
            fetch('/evaluate_answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_answer: userAnswer })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('feedback').innerText = `Feedback: ${data.feedback}, Score: ${data.score}`;
                document.getElementById('nextButton').style.display = 'block'; // Show next button
            })
            .catch(error => console.error('Error:', error));
        }

        function nextQuestion() {
            questionIndex++;
            document.getElementById('userAnswer').value = ''; // Clear user answer textarea
            document.getElementById('feedback').innerText = '';  //Clear feedback area
            generateQuestion();
        }

        function openFeedbackPopup() {
            document.getElementById("feedbackPopup").style.display = "block";
            // Set the content of the popup box
            document.getElementById("feedbackPopupContent").innerHTML = document.getElementById("feedback").innerHTML;
        }

        function closeFeedbackPopup() {
            document.getElementById("feedbackPopup").style.display = "none";
        }

        function throwConfetti(){
            (function frame() {
            // launch a few confetti from the left edge
            confetti({
                particleCount: 150,
                angle: 60,
                spread: 55,
                origin: { x: 0 }
            });
            // and launch a few from the right edge
            confetti({
                particleCount: 150,
                angle: 120,
                spread: 55,
                origin: { x: 1 }
            });
            }());
        }
    </script>
</body>
</html>