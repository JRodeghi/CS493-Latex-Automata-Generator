function draw_circle(e)
{
    const automata_canvas = document.getElementById('grph');
    const drawer = automata_canvas.getContext('2d');
    var pos = getMousePos(automata_canvas, e);
    posx = pos.x;
    posy = pos.y;
    alert("circle is at: x:" + posx + " y: " + posy);
    drawer.fillStyle = "#000000";
    drawer.beginPath();
    drawer.arc(posx, posy, 10, 10, 2 * Math.PI);
    drawer.fill();
}

function getMousePos(automata_canvas, evt) {
    var rect = automata_canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}
