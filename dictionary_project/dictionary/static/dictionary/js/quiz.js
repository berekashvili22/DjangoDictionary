// get answear containers
var question = document.getElementsByClassName('question-container')

// gerenate progress bar based on question lenght
var startBtn = document.getElementById('startQuizBtn');
var firstQuestion = document.getElementsByClassName('question-container 1')[0];
startBtn.addEventListener('click', function(){
    document.getElementById('startBtnCont').remove();
    // create result bar
    let div = document.createElement('div');
    div.id = 'progressBar';
    div.className = 'progress-bar-cont';

    for(var i=0; i<question.length; i++) {
        let id = question[i].dataset.id;
        let box = document.createElement('div');
        box.id = 'progressBar' + id;
        box.className = 'progress-bar';
        div.appendChild(box);
    }

    document.body.appendChild(div);
    // end create result bar

    firstQuestion.style.display = "block";

});

var answear = document.getElementsByClassName('answear-container');
// create variables for result
var CorrectAnswears = [];
var IncorrectAnswears = [];

// add eventlistener to each answear button click
for(var i=0; i<answear.length; i++) {
answear[i].addEventListener('click', function(){
        // answear id
        var id = this.dataset.id;
        // answear correctness
        var isTrue = this.dataset.is_true;
        // answear's question ID
        var parentId = this.dataset.parentid;

        // disable all answear buttons
        var answearCont = document.getElementsByClassName('answear-container ' + parentId);
        for(var i=0; i<answearCont.length; i++) {
            answearCont[i].disabled = true;
        }
        // if answear is true
        if (isTrue === "True"){
            this.classList.add("true");
            CorrectAnswears.push(parentId);
            document.getElementById('progressBar'+parentId).style.backgroundColor = "green";
        // if answear is false
        } else {
            this.classList.add("false");
            IncorrectAnswears.push(parentId);
            // show correct answear
            document.getElementById('progressBar'+parentId).style.backgroundColor = "red";
            var answears = document.getElementsByClassName('answear-container ' + parentId)
            for(var i=0; i<answears.length; i++) {
                if (answears[i].dataset.is_true === "True") {
                    answears[i].classList.add("true")
                }
            }
        }
        document.getElementById('nextBtn' + parentId).disabled = false;
        
    })
}


var nextBtns = document.getElementsByClassName('nextBtns');
for(var i=0; i<nextBtns.length; i++) {
nextBtns[i].addEventListener('click', function(){
        var contId = this.dataset.contid;
        var quizLength = nextBtns.length;
        if (contId != quizLength) {
            document.getElementsByClassName('question-container ' +contId)[0].style.display = "none"
            let nextContId = parseInt(contId) + 1
            document.getElementsByClassName('question-container ' +nextContId)[0].style.display = "block"
        } else {
            document.getElementsByClassName('question-container ' +contId)[0].style.display = "none"

            document.getElementById('progressBar').style.display = "none";

            document.getElementById('quizResult').style.display = "block";

            document.getElementById('total').innerHTML = "Total Questions: " + quizLength;

            document.getElementById('corrects').innerHTML = "Correct answears: " + CorrectAnswears.length;
            document.getElementById('incorrects').innerHTML = "Incorrect answears: " + IncorrectAnswears.length;
            document.getElementById('score').innerHTML = "Score: " + (CorrectAnswears.length * 100) / quizLength + "%";
            
            var quizId = document.getElementById('quizContainer').dataset.id

            
            getResult(CorrectAnswears, IncorrectAnswears, quizId);
            console.log('quiz completed')
        }
    })
}



function getResult(CorrectAnswears, IncorrectAnswears, quizId){
    var url = '/quiz/result/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'appliaction/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'CorrectAnswears': CorrectAnswears, 'IncorrectAnswears': IncorrectAnswears, 'quizId': quizId})
    })

    .then((response) =>{
        return response.json()
    })
}



