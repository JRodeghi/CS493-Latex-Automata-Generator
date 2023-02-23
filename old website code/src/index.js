function draw_circle(label,x,y)
{
    const c = document.getElementById('canvas');
    const ctx = c.getContext('2d');
    posx = x;
    posy = y;


    console.log(posx);
    console.log(posy);
    console.log("\n");
    ctx.font = "25px Georgia";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(posx, posy,32,0,2 * Math.PI);
    ctx.fillText(label, posx, posy);
    ctx.stroke();
}

function stem_file_parser(file_contents)
{
    const output = document.getElementById("output");
    file_lines=file_contents.split("\n");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);

    let out = "";


    let prev_x;
    let prev_y;
    let prev_lable;
    let posx = 0;
    let posy = 0;

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
            if (y < prev_y + 30 && y > prev_y - 30) {

            }
            else if (y > prev_y) {
                loc = loc + "above ";
                posy -= 100;
            }
            else if (y < prev_y) {
                loc = loc + "below ";
                posy += 100;
            }

            if (x < prev_x) {
                loc = loc + "right ";
                posx += 100;
            }
            if (x > prev_x) {
                loc = loc + "left ";
                posx -= 100;
            }

            loc = loc + " of = " + prev_lable;
        }
        else
        {
            posy = canvas.height/2;
            posx = canvas.width/2;
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
        draw_circle(lable, posx, posy);

        prev_x = x;
        prev_y = y;
        prev_lable = lable;

    }
    //create paths

    out += "\n";

    for(i = i+4;i < file_lines.length;i++)
    {
        if (file_lines[i] == "") {
            break;
        }
        path = file_lines[i].split(" ");
        path[0] = path[0].replace("\t","");
        
        let from = path[0];
        let to = path[1];

        if (path[path.length - 1] == "RIGHT")
        {
            path[path.length - 1] = "R";
        }
        if (path[path.length - 1] == "LEFT") {
            path[path.length - 1] = "L";
        }


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
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);

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
    let posx = 0;
    let posy = 0;

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
            posx = canvas.width / 2;
            posy = canvas.height/2;
        }
        else{
            if(loc_current_y < loc_prev_y + 30 && loc_current_y > loc_prev_y - 30)
            {

            }
            else if(loc_current_y < loc_prev_y) {
                loc = loc + "above ";
                posy -= 100;
            }
            else if(loc_current_y > loc_prev_y) {
                loc = loc + "below ";
                posy += 100;
            }

            if(loc_current_x > loc_prev_x) 
            {
                loc = loc + "right ";
                posx += 100;
               
            }
            if(loc_current_x < loc_prev_x)
            {
                loc = loc + "left ";
                posx -= 100;
            }
            
            loc = loc + " of = " + nodes[i-1].label
        }

        out = out + "\\node["+state+"] (" + nodes[i].label + ") [" + loc + "] {$" + nodes[i].label + "$};\n"
        draw_circle(nodes[i].label,posx,posy);
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