var button = document.getElementById("btn-add-qa");
var currentQuestionNos = 1;
console.log(button);
button.addEventListener("click", function(){
    console.log("Clicking")
    document.getElementById("fields");
    currentQuestionNos+=1;
    question = document.createElement("input")
    question.type="text"
    question.name="question-"+ currentQuestionNos
    question.classList.add("questions")
    question.id="btn-question-"+ currentQuestionNos
    answer = document.createElement("textarea")
    //<textarea name="answer" id="ta-answer" cols="30" rows="10"></textarea>
    answer.name = "answer-"+currentQuestionNos
    answer.id = "ta-answer-"+currentQuestionNos
    answer.cols="30"
    answer.rows="10"
    answer.classList.add("answers")
    questionLabel = document.createElement("label")
    questionLabel.for=question.id
    questionLabel.innerHTML = "Question "+(currentQuestionNos)
    answerLabel = document.createElement("label")
    answerLabel.for=answer.id
    answerLabel.innerHTML = "Answer "+(currentQuestionNos)
    fields.appendChild(questionLabel)
    fields.appendChild(question)
    fields.appendChild(answerLabel)
    fields.appendChild(answer)
})


let value = function(){return $(this).val()};

$("#btn-submit").click(function(){
    $.ajax({
        type: "POST",
        url: "/feedqa",
        data: { 
            link: $("#txt-link").val() || "", 
            questions: $(".questions").map(value).toArray().join(","), 
            answers: $(".answers").map(value).toArray().join(",")
        },
        success: function() {
            window.location.href = "/success";
        },
    });
})