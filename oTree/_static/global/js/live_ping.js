let ping_id = 0;

$(document).ready(function () {

    if (!audio) {
        document.getElementById("next_button").style.visibility = "hidden";
        setTimeout(function () {
            document.getElementById("next_button").style.visibility = "visible";
            document.getElementById("ping_delay_next").style.display = "none";
        }, 5000);
    };

    let iter = 0;
    let ping_sequence = window.setInterval(function () {
        ping();
        if (++iter === 5) {
            window.clearInterval(ping_sequence);
            ping_id = 0;
        }
    }, 1000);

});

function ping() {
    ping_id = ping_id + 1;
    liveSend({
        'type': 'ping',
        'ping_id': ping_id,
        'time_send': Number(performance.now())
    });
}

function liveRecv(data) {
    let responseTime = Math.round(performance.now() - data['time_send']);
    // console.log(`ping ${data['ping_id']} response time in ms: `, responseTime);
    document.getElementById(`latency_${data['ping_id']}`).value = responseTime;
}