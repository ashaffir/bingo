
function next(el, value) {
    if (isNaN(el.value)) return el.value = "";
    document.querySelector('#' + value).focus();
}

function openPlay() {
    document.querySelector('.playCode').style.right = 0;
    document.querySelector('#pin1').focus();
}

function closePlay() {
    document.querySelector('.playCode').style.right = '100vw';
}

// var form = document.querySelector(".modal.play");
// form.addEventListener('submit', openBingo);

function openBingo(url) {
    // e.preventDefault();
    document.querySelector('#submitError').style.display = '';
    let code = document.querySelector('#pin1').value + document.querySelector('#pin2').value + document
        .querySelector('#pin3').value + document.querySelector('#pin4').value;
    let name = document.querySelector('#name').value;

    console.log(`URL: ${url}`)
    // Check with the API if the game pin is valid
    //
    //
    //

    let valid = false;

    // Send data to API and get game code in return.
    $.ajax({
        url: url,
        data: {
            'code':code
        },
        success: function (){
            // alert('Album saved!');
            // window.location.href = '{% url "bingo_main:create_bingo" %}';
            console.log('START BROADCAST...')
            valid = true;
            window.location.href = `${location.href}game/${code}`;
        },
        error: function(xhr, errmsg, err) {
            valid = false;
            console.log('WRONG KEY...')
            if (!valid) {
                document.querySelector('#submitError').innerHTML = 'Please enter a valid game pin!'
                return document.querySelector('#submitError').style.display = 'block';
            }
        }
    })


    

    
}