let score = 0;
let countdown = 10;
const list_words = [];

$('.score').text(score)

$('#id_guess').on("submit", async function getAnswer(e){
    e.preventDefault();
    let word = $('#id_input').val()
    

    const resp = await axios.get("/check-word", { params: { word: word }});
    let answer = resp.data.result

    if (list_words.includes(word)) {
        return $('.alert').text("You already guessed that!")
    }

    if(answer == "not-word"){
        $('.alert').text("Not a word")
    } else if (answer == "not-on-board") {
        $('.alert').text("Word not on board")
    } else if (answer == "ok") {
        $('.alert').text("Point!");
        score += word.length;
        $('.score').text(score)
        list_words.push(word)
        $('.answers').append(`<li>${word}</li>`)
    }
})

let timer = setInterval(function(){
    if (countdown == 0){
        $('#id_guess').attr('disabled', true);
        $('#butt').attr('disabled', true);
        $('.alert').text("Times Up!");
        // $('.HUD').hide();
        $('.answers').hide();
        clearInterval(timer);
        totalScores();
    } else {
    countdown -= 1;
    $('.timer').text(countdown);
    }
},1000)

async function totalScores() {
    const resp = await axios.post('/get-score', {score: score});
    let highscore = resp.data.highscore
    if(resp.data.highscore < score){
        $('.HUD').html(`Congratulations! <br> New Highscore: <strong>${score}</strong>`)
    } else if (highscore == score){
        $('.HUD').html(`Close but not close enough! <br> Your score: <strong>${score}</strong>`)
    } else {
        $('.HUD').html(`Better Luck Next Time! <br> Your score: <strong>${score}</strong> <br> Score to beat: ${highscore}!`);
    }
}
