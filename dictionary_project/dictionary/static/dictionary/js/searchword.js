var searchBtn = document.getElementById('search-btn')
var addWordForm = document.getElementsByClassName('input-word-form')[0]
var searchWordForm = document.getElementsByClassName('search-word-form')[0]
var arrowBtn = document.getElementById('arrowBtn')

// toggle search and add word  forms
searchBtn.addEventListener('click', function(){
  addWordForm.classList.add('hidden')
  searchWordForm.classList.remove('hidden')
});
arrowBtn.addEventListener('click', function(){
  addWordForm.classList.remove('hidden')
  searchWordForm.classList.add('hidden')
});

// live search 
var searchinput = document.getElementById('searchWordInput')
var dictId = searchinput.dataset.dictid;

// add evenlistener to search form 
searchinput.addEventListener('keyup', (e) => {
  // record every key written in form
  var searchValue = e.target.value;

  // send search value to server
  if (searchValue.length > 0) {
    var url = '/dictionary/filter/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'appliaction/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'dictId': dictId, 'searchValue': searchValue})
    })

    .then((response) =>{
        return response.json()
    })

    // get all filtered word
    .then((data) =>{  
      // if no matching word is found ...
      if (data.length === 0) {
        document.getElementById('searchTable').style.display = "none";
        document.getElementById('wordsTable').style.display = "none";
        document.getElementsByClassName('pagination')[0].style.display = "none";
        document.getElementById('msgBox').style.display = "block";

      // if matching word is found ...
      } else {
        document.getElementById('wordsTable').style.display = "none";
        document.getElementById('searchTable').style.display = "";
        document.getElementsByClassName('pagination')[0].style.display = "none";
        document.getElementById('msgBox').style.display = "none";
        
        // dynamically update table with found words data
        var tbody = document.getElementById('searchTbody');
        tbody.innerHTML = "";
        let count = 1;
        data.forEach(item => {
          tbody.innerHTML+=`
          <tr class="tableRow ${item.id} search">
            <th scope="row">${count++}</th>
            <td class="tableData originalCol">
              <input type="text" class="form tbl-input ${item.id} original search" style="border: none;" value="${item.original_word}" readonly>
            </td>
            <td class="tableData translatedCol">
              <input type="text" class="form tbl-input ${item.id} translated search" style="border: none;" value="${item.translated_word}" readonly>
            </td>
            <td class="tableData definitionCol">
                <input type="text" class="form tbl-input ${item.id} definition search" style="border: none;" value="${item.definition}" readonly>
            </td>
            <td class="tableData btnsCol">
              <!-- buttons for inline edit -->
              <!-- edit btn -->
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#848ee6" viewBox="0 0 16 16"
                  class="bi bi-pencil-fill update-row" 
                  data-word=${item.id} 
                  id="editBtn${item.id} search"
                  data-action="edit"> 
                <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
              </svg>
              <!-- delete btn -->
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ee0034" viewBox="0 0 16 16"
                  class="bi bi-trash-fill update-row" 
                  id="delBtn${item.id} search"
                  data-word=${item.id} 
                  data-action="delete">
                <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
              </svg>
              <!-- done btn  -->
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="green" style="display: none;" viewBox="0 0 16 16" 
                  class="bi bi-x-circle-fill update-row" 
                  data-word=${item.id}
                  id="doneBtn${item.id} search"
                  data-action="save">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
              </svg>
              <!-- cancel btn -->
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" style="display: none;" viewBox="0 0 16 16"
                  class="bi bi-x-circle-fill update-row"
                  data-word=${item.id}
                  id="cancelBtn${item.id} search"
                  data-action="cancle">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
              </svg>
            </td>
          </tr>
          `
        });

        // --
        // addEventsForBtns
        var updateBtns = document.getElementsByClassName('update-row');
        for(var i=0; i<updateBtns.length; i++) {
            updateBtns[i].addEventListener('click', function(){
                var wordId = this.dataset.word;
                var action = this.dataset.action;
                var search = true;
                // select row with self.id , hide data and show edit field 
                // original world
                var origInput = document.getElementsByClassName('tbl-input ' + wordId + ' original search')[0]
                // translated world
                var transInput = document.getElementsByClassName('tbl-input ' + wordId + ' translated search')[0]
                // definition
                var definInput = document.getElementsByClassName('tbl-input ' + wordId + ' definition search')[0]
                // buttons
                var delBtn = document.getElementById('delBtn' + wordId + ' search')
                var doneBtn = document.getElementById('doneBtn' + wordId + ' search')
                var cancelBtn = document.getElementById('cancelBtn' + wordId + ' search')
                var editBtn = document.getElementById('editBtn' + wordId + ' search')

                // check if action is cancle or edit
                if (action == "edit") {  
                    // change row element display styles  
                    // for origianl world
                    origInput.readOnly = false;
                    origInput.classList.add('active-input')
                    // for origianl world
                    transInput.readOnly = false;
                    transInput.classList.add('active-input')
                    // for definition
                    definInput.readOnly = false;
                    definInput.classList.add('active-input')
                    // for buttons
                    delBtn.style.display = "none";
                    doneBtn.style.display = "block";
                    cancelBtn.style.display = "block";
                    this.style.display = "none";
        
                } else if (action == "cancle") {
                    // change row element display styles  
                    // for origianl world
                    origInput.readOnly = true;
                    origInput.classList.remove('active-input')
                    // for origianl world
                    transInput.readOnly = true;
                    transInput.classList.remove('active-input')
                    // for definition
                    definInput.readOnly = true;
                    definInput.classList.remove('active-input')
                    // for buttons
                    editBtn.style.display = "block";
                    delBtn.style.display = "block"
                    doneBtn.style.display = "none";
                    this.style.display = "none";
        
                } else if (action == "save") {
                    // get edited data from forms
                    var originalWord = origInput.value;
                    var translatedWord =  transInput.value;
                    var definition = definInput.value;
                    // send data to function
                    updateWord(originalWord, translatedWord, definition, wordId, action, search)
                } else if (action == "delete") {
                    var originalWord = '';
                    var translatedWord = '';
                    var definition = '';
                    updateWord(originalWord, translatedWord, definition, wordId, action, search)
                }
            });
        }
        // ---

      }
    })
    
  } else {
    document.getElementById('msgBox').style.display = "none";
    document.getElementById('searchTable').style.display = "none";
    document.getElementById('wordsTable').style.display = "";
    document.getElementsByClassName('pagination')[0].style.display = "";
  }
});