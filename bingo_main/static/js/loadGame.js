
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
    playButton = document.getElementById('playButton');
    playButton.disabled = true;
    //document.querySelector('#submitError').style.display = '';
    let code = document.querySelector('#pin1').value + document.querySelector('#pin2').value + document
        .querySelector('#pin3').value + document.querySelector('#pin4').value;

    let name = document.querySelector('#name').value;

    console.log(`URL: ${url}`)
    //console.log(`NAME: ${name}`)
    // Check with the API if the game pin is valid
    //
    //
    //

    let valid = false;

    // Send data to API and get game code in return.
    $.ajax({
        url: url,
        data: {
            'code': code,
            'name': name
        },
        success: function (response) {
            // alert('Album saved!');
            // window.location.href = '{% url "bingo_main:create_bingo" %}';

            playButton.disabled = true;
            console.log('START BROADCAST...')
            valid = true;
            const data = JSON.parse(response)
            console.log(`DATA: ${JSON.stringify(data)}`)

            if (data.player_id){
                const playerID = data.player_id;
                console.log(`PLAYER: ${playerID}`)
                window.location.href = `${window.location.origin}/bingo/${playerID}`;
            } else if (data.finished){
                console.log(`GAME FINISHED: ${data.finished}`)
                document.querySelector('#submitError').innerHTML = 'This game is finished or in progress. Please try another game that you are invited to.'
                document.querySelector('#submitError').style.display = 'block';                
                setTimeout(function () {
                    $("#submitError").hide();
                }, 10000);
                playButton.disabled = false;
            } else if (data.full){
                console.log(`GAME FULL: ${data.full}`)
                document.querySelector('#submitError').innerHTML = 'This game is no longer accessible'
                document.querySelector('#submitError').style.display = 'block';                
                setTimeout(function () {
                    $("#submitError").hide();
                }, 10000);
                playButton.disabled = false;

            } else if (data.data){
                console.log(`INVALID GAME: ${data.data}`)
                document.querySelector('#submitError').innerHTML = 'This game is not active. Please enter a valid Game ID'
                document.querySelector('#submitError').style.display = 'block';                
                setTimeout(function () {
                    $("#submitError").hide();
                }, 10000);
                playButton.disabled = false;
            } else {
                console.log(`UNKNOWN GAME: ${JSON.stringify(data)}`)
                document.querySelector('#submitError').innerHTML = 'Please enter a valid Game ID'
                document.querySelector('#submitError').style.display = 'block';                
                setTimeout(function () {
                    $("#submitError").hide();
                }, 10000);
                playButton.disabled = false;

            }



        },
        error: function (xhr, errmsg, err) {
            valid = false;
            console.log('WRONG KEY...')
            if (!valid) {
                return
            }
        }
    })





}