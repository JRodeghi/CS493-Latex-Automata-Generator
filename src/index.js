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
function stem_file_parser(file_contents)
{
    const output = document.getElementById("output");
    file_lines=file_contents.split("\n");

    let out = "";

    let prev_x;
    let prev_y;
    let prev_lable;

    let i = 5;
    //create nodes
    for(i;i < file_lines.length;i++)
    {
        if (file_lines[i] == "") {
            break;
        }

        node = file_lines[i].split(" ");
        node[0] = node[0].replace("\t","");
        
        let lable = node[0];
        let x= node[1];
        let y = node[2];
        let start = node[3];
        let accept = node[4];

        let loc = "";

        if(i != 5)
        {
            if (y > prev_y) {
                loc = loc + "above ";
            }
            if (y < prev_y) {
                loc = loc + "below ";
            }

            if (x > prev_x) {
                loc = loc + "right ";
            }
            if (x < prev_x) {
                loc = loc + "left ";
            }

            loc = loc + " of = " + prev_lable;
        }

        let state = "state";
        if(start == "true")
        {
            state += ",initial"; 
        }
        if(accept == "true")
        {
            state += ",accepting";
        }

        out = out + "\\node[" + state + "] (" + lable + ") [" + loc + "] {$" + lable + "$};\n"

        prev_x = x;
        prev_y = y;
        prev_lable = lable;

    }
    //create paths

    for(i = i+4;i < file_lines.length;i++)
    {
        if (file_lines[i] == "") {
            break;
        }
        path = file_lines[i].split(" ");
        path[0] = path[0].replace("\t","");
        
        let from = path[0];
        let to = path[1];

        let plabel = path[2] + "|" + path[3] +"|" + path[path.length-1];

        if(from == to)
        { 
            out += "\\path (" + from + ") edge [loop above]   node {$" + plabel + "$} (" + to + ");\n"; 
        }
        else
        {
            out += "\\path (" + from + ") edge [bend right]   node {$" + plabel + "$} (" + to + ");\n";
        }
        
    }

    output.innerText = out;
}

function file_parser(file_contents)
{
    const output = document.getElementById("output");
    let jobj;
    try{
         jobj = JSON.parse(file_contents);
    }catch(error)
    {
        stem_file_parser(file_contents);
        return 0;
    }

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
            if(loc_current_y < loc_prev_y + 30 && loc_current_y > loc_prev_y - 30)
            {

            }
            else if(loc_current_y < loc_prev_y) {
                loc = loc + "above ";
            }
            else if(loc_current_y > loc_prev_y) {
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

    out += "\n";

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

    output.innerText = out;
    return 0;
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