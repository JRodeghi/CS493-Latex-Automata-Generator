function draw_circle(e)
{
    const automata_canvas = document.getElementById('grph');
    const drawer = automata_canvas.getContext('2d');
    var pos = getMousePos(automata_canvas, e);
    posx = pos.x;
    posy = pos.y;
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

export function selectFile() {
    return new Promise(resolve => {
        const input = document.createElement('input')
        input.type = 'file'

        input.onchange = e => {
            const file = e.target.files[0]
            const reader = new FileReader()
            reader.readAsText(file, 'UTF-8')

            reader.onload = readerEvent => {
                const content = readerEvent.target.result
                resolve(content)
            }
        }

        input.click()
    })
}

const import_NFA = document.getElementById("import_NFA");
import_NFA.addEventListener("change",() => {
    alert("Test")
    selectFile().then(contents => alert(contents))

});