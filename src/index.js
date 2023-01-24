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

function file_parser(file_contents)
{
    const output = document.getElementById("output")
    const jobj = JSON.parse(file_contents);

    nodes = jobj["nodes"]

    //print out the nodes
    let out = "";
    for(let i = 0; i < nodes.length;i++)
    {
        let state = "state";
        let loc_prev_x = 0;
        let loc_prev_y = 0;

        if (jobj["fsa"].startState == nodes[i].label)
        {
            state += ",initial";
        }
        if (nodes[i].acceptState == true)
        {
            state += ",accepting";
        }

        if(i > 0)
        {
            loc_prev_x = nodes[i - 1].loc.x;
            loc_prev_y = nodes[i - 1].loc.y;
        }
        let loc_current_x = nodes[i].loc.x;
        let loc_current_y = nodes[i].loc.y;

        let loc = "";
        if(i == 0)
        {
            loc = loc + " ";
        }
        else{
            if(loc_current_y > loc_prev_y) {
                loc = loc + "above ";
            }
            if(loc_current_y < loc_prev_y) {
                loc = loc + "below ";
            }

            if(loc_current_x > loc_prev_x) 
            {
                loc = loc + "right ";
            }
            if(loc_current_x < loc_prev_x)
            {
                loc = loc + "left ";
            }
            
            loc = loc + " of = " + nodes[i-1].label
        }

        out = out + "\\node["+state+"] (" + nodes[i].label + ") [" + loc + "] {$" + nodes[i].label + "$};\n"
    }

    //print out the paths
    for(let i = 0; i < nodes.length;i++)
    {
        for(let j = 0; j < nodes.length;j++)
        {
            if(nodes[i].transitionText[nodes[j].label])
            {
                plabel = nodes[i].transitionText[nodes[j].label];

                for(let k = 0; k < plabel.length;k++)
                {
                    if (plabel[k] == '\u03B5')
                    {
                        plabel[k] = "\\epsilon";
                    }
                }
                if(i == j)
                {
                    out += "\\path (" + nodes[i].label + ") edge [loop above]   node {$" + plabel + "$} (" + nodes[j].label + ");\n";
                }
                else
                {
                    
                    out += "\\path (" + nodes[i].label + ") edge [bend right]   node {$" + plabel + "$} (" + nodes[j].label + ");\n";
                } 
            }
        }
    }

    output.innerText = out
}

function selectFile() {
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