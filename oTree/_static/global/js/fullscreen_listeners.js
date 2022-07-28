$(document).ready(function () {
    let mediaQueryList = window.matchMedia('(display-mode: fullscreen)');
    checkFullScreen(mediaQueryList);
    addEventListener("load", function () {
        window.matchMedia('(display-mode: fullscreen)')
            .addEventListener("change", (e) => {
                // console.log('In addEventListener change.');
                checkFullScreen(e);
            });
    })
});
