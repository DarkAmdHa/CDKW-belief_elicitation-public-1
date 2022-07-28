function checkFullScreen(e) {
    if (e.matches) {
        // console.log("In test_app mode.");
        document.getElementById("fullscreen_instructions").style.display = 'none';
        document.getElementById("active_screen").style.display = 'block';

        if (audio) {
            if (!audio_ended) {
                if (audio_started) {
                    parts[current_part - 1].play();
                } else {
                    // check_autoplay();
                    play_part(current_part);
                    audio_started = true;
                }
            }
        } else {
        }

    } else {
        // console.log("Not in test_app mode.");
        document.getElementById("fullscreen_instructions").style.display = 'block';
        document.getElementById("active_screen").style.display = 'none';
        if (audio) {
            document.getElementById("start_audio").style.display = 'none';
            if (audio_started && !audio_ended) {
                parts[current_part - 1].pause();
            }
        }
    }
}
