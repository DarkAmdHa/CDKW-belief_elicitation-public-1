$(document).ready(function () {

    document.getElementById("replay_button").addEventListener("click", function () {
        // console.log('Replay button clicked.')
        play_part(2);
    });

    document.getElementById("next_button").addEventListener("click", function () {
        const answer = document.getElementById('audio_test').value;
        if (answer == 42) {
            document.getElementById("form").submit();
        } else {
            document.getElementById("audio_error").style.display = 'block';
        }
    });
});