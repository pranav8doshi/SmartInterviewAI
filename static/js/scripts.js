
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("interview-form");
    const questionContainer = document.getElementById("question-container");
    const questionText = document.getElementById("question-text");
    const answerInput = document.getElementById("answer");
    const submitAnswerBtn = document.getElementById("submit-answer");

    let questionIndex = 0;
    let username = "";
    let role = "";

    form.addEventListener("submit", function (event) {
        event.preventDefault();  // Prevent default form submission
        username = document.getElementById("username").value;
        role = document.getElementById("role").value;

        // Open meeting in a new tab
        const meetingTab = window.open("{{ url_for('meeting') }}", "_blank");

        // Wait a few seconds before starting the bot (adjust if needed)
        setTimeout(() => {
            fetch("/start_interview", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, role, question_index: -1, answer: "" })
            })
            .then(response => response.json())
            .then(data => {
                if (data.question) {
                    form.style.display = "none";  // Hide form
                    questionContainer.style.display = "block";  // Show questions
                    questionText.innerText = data.question;
                    questionIndex = data.question_index;
                }
            });
        }, 3000);  // 3-second delay
    });

    submitAnswerBtn.addEventListener("click", function () {
        let userAnswer = answerInput.value.trim();
        if (!userAnswer) {
            alert("Please provide an answer!");
            return;
        }

        fetch("/start_interview", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, role, question_index: questionIndex, answer: userAnswer })
        })
        .then(response => response.json())
        .then(data => {
            if (data.question) {
                questionText.innerText = data.question;
                answerInput.value = "";
                questionIndex = data.question_index;
            } else {
                alert("Interview complete!");
                questionContainer.innerHTML = "<h2>Interview finished! Thank you.</h2>";
            }
        });
    });
});

