let audio_started = false;
let audio_ended = false;

const n_parts = 2;
let parts = new Array(n_parts);
let current_part = 1;


$(document).ready(function () {
    for (let i = 1; i <= 4; i++) {
        parts[i - 1] = document.getElementById('part_' + i);
    }

    document.getElementById("start_audio").addEventListener("click", function () {
        play_part(current_part);
        audio_started = true;
    });

    if (!full_screen) {
        check_autoplay();
    }

});

function check_autoplay() {
    let promise = parts[0].play();
    if (promise !== undefined) {
        promise.then(_ => {
            parts[0].addEventListener('ended', function (e) {
                current_part += 1;
                play_part(current_part);
            })
        }).catch(error => {
            document.getElementById("start_audio").style.display = "block";
        });
    }
}

function play_part(_current_part) {

    document.getElementById("start_audio").style.display = "none";

    if (_current_part === 1) {
        check_autoplay();
    } else {
        parts[_current_part - 1].play();
        if (_current_part < n_parts) {
            parts[_current_part - 1].addEventListener('ended', function (e) {
                current_part += 1;
                play_part(_current_part + 1);
            })
        } else {
            parts[_current_part - 1].addEventListener('ended', function (e) {
                document.getElementById("input_line").style.visibility = "visible";
                audio_ended = true;
            })
        }
    }
}

