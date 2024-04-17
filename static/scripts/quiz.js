let currentQuizData = null; // Global storage for quiz data

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('submitQuiz').addEventListener('click', submitQuiz);
});

function getQuizFromInput() {
    const courseCode = document.getElementById('courseInput').value.trim();
    if (courseCode) {
        displayLoading(true);
        getQuiz(courseCode);
    } else {
        alert('Please enter a valid course code.');
    }
}

function getQuiz(course) {
    fetch(`quiz/generate_quiz/${course}`)
        .then(response => response.json())
        .then(quizData => {
            currentQuizData = quizData; // Store the quiz data globally
            displayQuiz(quizData);
            displayLoading(false);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            displayError('Failed to load quiz: ' + error.message);
            displayLoading(false);
        });
}

function submitQuiz() {
    const questions = document.querySelectorAll('.question');
    let allAnswered = true;  // Flag to check if all questions have been answered

    // Remove any existing alert messages before checking the answers
    const existingAlert = document.querySelector('.alert-message');
    if (existingAlert) {
        existingAlert.remove();
    }

    questions.forEach((questionBlock, index) => {
        const selectedInput = questionBlock.querySelector('input[type="radio"]:checked');
        if (!selectedInput) {
            allAnswered = false;  // Set the flag to false if any question is unanswered
        }
    });

    // If not all questions are answered, display a message just above the submit button and exit the function
    if (!allAnswered) {
        const answerAll = document.createElement('p');
        answerAll.className = 'alert-message';  // A specific class for styling this message
        answerAll.textContent = 'Please answer all of the questions above!';
        answerAll.style.color = 'red';  // Make the text color red for visibility

        const submitButton = document.getElementById('submitQuiz');
        submitButton.parentNode.insertBefore(answerAll, submitButton);

        return;  // Stop the function if there are unanswered questions
    }
    questions.forEach((questionBlock, index) => {
        const selectedInput = questionBlock.querySelector('input[type="radio"]:checked');
        const labels = questionBlock.querySelectorAll('label');
        const inputs = questionBlock.querySelectorAll('input[type="radio"]'); // Select all radio inputs
        const correctAnswer = currentQuizData['Additional Quiz Questions'][index].Answer;

        // Disable all radio buttons to prevent reselection
        inputs.forEach(input => {
            input.disabled = true;
        });

        // Clear previous results before appending new content
        questionBlock.querySelectorAll('.result-text, .explanation-text, .correct_con, .incorrect_con').forEach(el => el.remove());

        labels.forEach(label => {
            const input = label.previousElementSibling;
            if (input.value === correctAnswer) {
                label.classList.add('correct');
                label.classList.remove('incorrect');
            } else {
                label.classList.add('incorrect');
                label.classList.remove('correct');
            }
        });

        if (selectedInput) {
            const isSelectedCorrect = selectedInput.value === correctAnswer;
            const resultContainer = document.createElement('div');
            resultContainer.className = isSelectedCorrect ? 'correct_con' : 'incorrect_con';
        
            const resultText = document.createElement('p');
            resultText.className = isSelectedCorrect ? 'correct' : 'incorrect';
            resultText.textContent = isSelectedCorrect ? 'Correct!' : 'Incorrect!';
            resultContainer.appendChild(resultText); // Append result text to the container

            const correctAnsLabel = document.createElement('p');
            correctAnsLabel.className = isSelectedCorrect ? 'correct' : 'incorrect';
            correctAnsLabel.textContent = `Correct answer: ${correctAnswer}`
            resultContainer.appendChild(correctAnsLabel); // Append result text to the container
        
            // Create and append the "Explanation:" label
            const explanationLabel = document.createElement('p');
            explanationLabel.className = 'explanation-label';
            explanationLabel.textContent = 'Explanation:';
            resultContainer.appendChild(explanationLabel); // Append the label to the container
        
            const explanationText = document.createElement('p');
            explanationText.className = 'explanation-text';
            explanationText.textContent = currentQuizData['Additional Quiz Questions'][index].Explanation;
            resultContainer.appendChild(explanationText); // Append explanation text to the container
        
            questionBlock.appendChild(resultContainer);
        }        
        
    });
}



function displayQuiz(quizData) {
    const quizContainer = document.getElementById('quizForm');
    quizContainer.innerHTML = ''; // Clear the quiz container before adding new content

    quizData['Additional Quiz Questions'].forEach((question, index) => {
        // Container for the entire question block (both question and choices)
        const questionBlock = document.createElement('div');
        questionBlock.className = 'question';

        // Container for the question text
        const questionText = document.createElement('div');
        questionText.className = 'question-text';
        questionText.innerHTML = `<h2>Q${index + 1}: ${question.Question}</h2>`;

        // Container for the choices
        const choicesContainer = document.createElement('div');
        choicesContainer.className = 'choices-container';

        const choicesList = document.createElement('ul');
        choicesList.className = 'choices';

        question.Choices.forEach((choice, choiceIndex) => {
            const choiceItem = document.createElement('li');
            const input = document.createElement('input');
            input.type = 'radio';
            input.id = `choice_${index}_${choiceIndex}`;
            input.name = `question_${index}`;
            input.value = choice;

            const label = document.createElement('label');
            label.htmlFor = input.id;
            label.textContent = choice;
            label.className = 'choice-label';

            choiceItem.appendChild(input);
            choiceItem.appendChild(label);
            choicesList.appendChild(choiceItem);
        });

        choicesContainer.appendChild(choicesList);

        // Append the question text and choices container to the question block
        questionBlock.appendChild(questionText);
        questionBlock.appendChild(choicesContainer);

        // Append the entire question block to the main quiz container
        quizContainer.appendChild(questionBlock);
        document.getElementById('submitContainer').style.display = 'block';

    });

    attachChoiceEventListeners(); // Ensure event listeners are reattached to new dynamic elements
}


function attachChoiceEventListeners() {
    const choices = document.querySelectorAll('.choices li label');
    choices.forEach(choice => {
        choice.addEventListener('click', function() {
            const allChoicesInGroup = choice.closest('ul').querySelectorAll('label');
            allChoicesInGroup.forEach(c => c.classList.remove('selected'));
            choice.classList.add('selected');
        });
    });
}

function displayLoading(show) {
    const loading = document.getElementById('loading');
    loading.style.display = show ? 'block' : 'none';
}

function displayError(message) {
    const quizContainer = document.getElementById('quizForm');
    quizContainer.innerHTML = `<p class="error">${message}</p>`;
}
