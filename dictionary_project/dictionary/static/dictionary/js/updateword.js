
var updateBtns = document.getElementsByClassName('update-row');

// hide / show different buttons while editing
for(var i=0; i<updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var wordId = this.dataset.word;
        var action = this.dataset.action;
        // check if action is cancle or edit
        
        if (action == "edit") {    
            // select row with self.id , hide data and show edit field 
            // for origianl world
            document.getElementsByClassName('tbl-input ' + wordId + ' original')[0].style.display = "block";
            document.getElementsByClassName('tbl-data ' + wordId + ' original')[0].style.display = "none";

            // for origianl world
            document.getElementsByClassName('tbl-input ' + wordId + ' translated')[0].style.display = "block";
            document.getElementsByClassName('tbl-data ' + wordId + ' translated')[0].style.display = "none";
            
            // for definition
            document.getElementsByClassName('tbl-input ' + wordId + ' definition')[0].style.display = "block";
            document.getElementsByClassName('tbl-data ' + wordId + ' definition')[0].style.display = "none";


            document.getElementsByClassName('delete-row ' + wordId)[0].style.display = "none";
            document.getElementsByClassName('update-row ' + wordId)[0].style.display = "block";
            document.getElementsByClassName('save-row ' + wordId)[0].style.display = "block";

            this.style.display = "none";

        } else {
            console.log('cancel')
        }
    });
}

// gets and sends data of edited rows to function
  
var doneBtns = document.getElementsByClassName('save-row');

for(var i=0; i<doneBtns.length; i++) {
    doneBtns[i].addEventListener('click', function(){
      var rowId = this.dataset.rowid;
      // get edited data from forms
      var originalWord = document.getElementsByClassName('tbl-input ' + rowId + ' original')[0].value;
      var translatedWord = document.getElementsByClassName('tbl-input ' + rowId + ' translated')[0].value;
      var definition = document.getElementsByClassName('tbl-input ' + rowId + ' definition')[0].value;
      // send data to function
      updateWord(originalWord, translatedWord, definition, rowId)
    });
} 


// get csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


// sends data to server 
function updateWord(original, translated, definition, id){
    console.log('params passed to function')

    var url = '/dictionary/update/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'appliaction/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'original': original, 'translated': translated, 'definition': definition, 'wordId': id})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })

}

