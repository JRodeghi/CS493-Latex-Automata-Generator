import json
import sys
import getopt



class Node:
    def __init__(self,l,c,a,i,x,y):
        self.label= l
        self.connections = c
        self.accepting = a
        self.initial = i
        self.x = x
        self.y = y

        self.below_left = ""
        self.below_right = ""
        self.below = ""
        self.above = ""
        self.above_right = ""
        self.above_left = ""
        self.right = ""
        self.left = ""

        self.printed = False

    def print_node(self):
        loc =  ""
        state = "state"

        if(self.printed == True):
            return 0

        if(self.initial == True):
            state += ",initial"
        if(self.accepting == True):
            state += ",accepting"
        
        if(self.right != ""):
            loc = "left of = " + self.right.label
        elif(self.left != ""):
                loc = "right of =" + self.left.label
        elif(self.below != ""):
                loc = "above of = "+ self.below.label
        elif(self.above != ""):
                loc = "below of =" + self.above.label
        elif(self.above_right != ""):
                loc = "below left of = " + self.above_right.label
        elif(self.above_left != ""):
                loc = "below right of = " + self.above_left.label
        elif(self.below_right != ""):
                loc = "above left of = " + self.below_right.label
        elif(self.below_left != ""):
                loc = "above right of =" + self.below_left.label

        if self.initial == True:
            loc = ""

        print("\\node[" + state + "] (" + self.label + ") [" + loc + "] {$" + self.label + "$};")
        self.printed = True
        



#function that will organize the nodes and print the latex code
def layout_nodes(nodes,start):
    start_node = nodes[start]
    for i in nodes:
        if nodes[i] == start_node:
            continue
        #right
        if start_node.x < nodes[i].x and start_node.y + 100 > nodes[i].y and start_node.y - 100 < nodes[i].y:
            if start_node.right == "":
                nodes[i].left = start_node
                start_node.right = nodes[i]
            else:
                prev = start_node
                current = start_node.right
                while True: 
                    #right of current node
                    if current.x < nodes[i].x:
                        if current.right == "":
                            nodes[i].left = current
                            current.right = nodes[i]
                            break
                    #inbetween current and prev
                    elif current.x > nodes[i].x:
                        current.left = nodes[i]
                        nodes[i].right = current
                        nodes[i].left = prev
                        prev.right = nodes[i]
                        break
                    #keep going
                    else:
                        prev = current
                        current = current.right
        
        #left 
        elif start_node.x > nodes[i].x and start_node.y + 100 > nodes[i].y and start_node.y - 100 < nodes[i].y:
            if start_node.left == "":
                nodes[i].right = start_node
                start_node.left = nodes[i]
            else:
                prev = start_node
                current = start_node.left
                while True: 
                    #left of current node
                    if current.x > nodes[i].x:
                        if current.left == "":
                            nodes[i].right = current
                            current.left = nodes[i]
                            break
                    #in between current and prev
                    elif current.x < nodes[i].x:
                        current.right = nodes[i]
                        nodes[i].left = current
                        nodes[i].right = prev
                        prev.left = nodes[i]
                        break
                    #keep going
                    else:
                        prev = current
                        current = current.left
        
        #above (y is inverted for NFA - DFA)
        elif start_node.y > nodes[i].y and start_node.x + 100 > nodes[i].x and start_node.x - 100 < nodes[i].x:
            if start_node.above == "":
                nodes[i].below = start_node
                start_node.above = nodes[i]
            else:
                prev = start_node
                current = start_node.above
                while True: 
                    #above of current node
                    if current.y > nodes[i].y:
                        if current.above == "":
                            nodes[i].below = current
                            current.above = nodes[i]
                            break
                    #in between current and prev
                    elif current.y < nodes[i].y:
                        current.below = nodes[i]
                        nodes[i].above = current
                        nodes[i].below = prev
                        prev.above = nodes[i]
                        break
                    #keep going
                    else:
                        prev = current
                        current = current.above
        #below
        elif start_node.y < nodes[i].y and start_node.x + 100 > nodes[i].x and start_node.x - 100 < nodes[i].x:
            if start_node.below == "":
                nodes[i].above = start_node
                start_node.below = nodes[i]
            else:
                prev = start_node
                current = start_node.below
                while True: 
                    #left of current node
                    if current.y > nodes[i].y:
                        if current.below == "":
                            nodes[i].above = current
                            current.below = nodes[i]
                            break
                    #in between current and prev
                    elif current.y < nodes[i].y:
                        current.above = nodes[i]
                        nodes[i].below = current
                        nodes[i].above = prev
                        prev.below = nodes[i]
                        break
                    #keep going
                    else:
                        prev = current
                        current = current.below
        #above right
        elif start_node.x < nodes[i].x and start_node.y > nodes[i].y:
            # no nodes to the above or to the right 
            if start_node.right == "" and start_node.above == "" and start_node.above_right == "":
                start_node.above_right = nodes[i]
                nodes[i].below_left = start_node
            #nodes to the right but not above
            elif start_node.right != "":
                prev = start_node
                current = start_node.right
                while True: 
                    #right of current node
                    if current.x < nodes[i].x:
                        #cant go anymore right and cant go up
                        if current.right == "" and current.above == "":
                            current.above = nodes[i]
                            nodes[i].below = current
                            break
                        #cant go anymore right but can go up
                        elif current.right == "" and current.above != "":
                            prev = current
                            current = current.above
                            while True: 
                                #above of current node
                                if current.y > nodes[i].y:
                                    if current.above == "":
                                        nodes[i].below = current
                                        current.above = nodes[i]
                                        break
                                #in between current and prev
                                elif current.y < nodes[i].y:
                                    current.below = nodes[i]
                                    nodes[i].above = current
                                    nodes[i].below = prev
                                    prev.above = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.above
                                break

                    #doesnt need to go anymore right
                    elif current.x > nodes[i].x:
                        #cant go up
                        if current.above == "":
                            current.above = nodes[i]
                            nodes[i].below = current
                            break
                        #node needs to go up
                        elif current.above != "":
                            prev = current
                            current = current.above
                            while True: 
                                #above of current node
                                if current.y > nodes[i].y:
                                    if current.above == "":
                                        nodes[i].below = current
                                        current.above = nodes[i]
                                        break
                                #in between current and prev
                                elif current.y < nodes[i].y:
                                    current.below = nodes[i]
                                    nodes[i].above = current
                                    nodes[i].below = prev
                                    prev.above = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.above
                            break
                    #keep going
                    else:
                        prev = current
                        current = current.right
            #cant go right but can go up
            elif start_node.right == "" and start_node.above != "":
                prev = start_node
                current = start_node.above
                while True: 
                    #above of current node
                    if current.y > nodes[i].y:
                        #cant go up and cant go right
                        if current.above == "" and current.right == "":
                            nodes[i].left = current
                            current.right = nodes[i]
                            break
                        #cant go up but can go right
                        elif current.above == "" and current.right != "":
                            prev = current
                            current = current.right
                            while True: 
                                #right of current node
                                if current.x < nodes[i].x:
                                    if current.right == "":
                                        nodes[i].left = current
                                        current.right = nodes[i]
                                        break
                                #inbetween current and prev
                                elif current.x > nodes[i].x:
                                    current.left = nodes[i]
                                    nodes[i].right = current
                                    nodes[i].left = prev
                                    prev.right = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.right
                            
                    #doesnt need to go up any more
                    elif current.y < nodes[i].y:
                        #cant go right
                        if current.right == "":
                            current.right = nodes[i]
                            nodes[i].left = current
                            break
                        # needs to go right
                        elif current.right != "":
                            prev = current
                            current = current.right
                            while True: 
                                #right of current node
                                if current.x < nodes[i].x:
                                    if current.right == "":
                                        nodes[i].left = current
                                        current.right = nodes[i]
                                        break
                                #inbetween current and prev
                                elif current.x > nodes[i].x:
                                    current.left = nodes[i]
                                    nodes[i].right = current
                                    nodes[i].left = prev
                                    prev.right = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.right
                            break
                    #keep going
                    else:
                        prev = current
                        current = current.above
                break
                
        #above left
        elif start_node.x > nodes[i].x and start_node.y > nodes[i].y:
            # no nodes to the above or to the left 
            if start_node.left == "" and start_node.above == "" and start_node.above_left == "":
                start_node.above_left = nodes[i]
                nodes[i].below_right = start_node
            #nodes to the left but not above
            elif start_node.left != "" :
                prev = start_node
                current = start_node.left
                while True: 
                    #left of current node
                    if current.x > nodes[i].x:
                        #cant go anymore left and cant go up
                        if current.left == "" and current.above == "":
                            current.above = nodes[i]
                            nodes[i].below = current
                            break
                        #cant go anymore left but can go up
                        elif current.left == "" and current.above != "":
                            prev = current
                            current = current.above
                            while True: 
                                #above of current node
                                if current.y > nodes[i].y:
                                    if current.above == "":
                                        nodes[i].below = current
                                        current.above = nodes[i]
                                        break
                                #in between current and prev
                                elif current.y < nodes[i].y:
                                    current.below = nodes[i]
                                    nodes[i].above = current
                                    nodes[i].below = prev
                                    prev.above = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.above
                            break
                        else:
                            prev = current
                            current = current.left
                    #doesnt need to go anymore left
                    elif current.x < nodes[i].x:
                        #cant go up
                        if current.above == "":
                            current.above = nodes[i]
                            nodes[i].below = current
                            break
                        #node needs to go up
                        elif current.above != "":
                            prev = current
                            current = current.above
                            while True: 
                                #above of current node
                                if current.y > nodes[i].y:
                                    if current.above == "":
                                        nodes[i].below = current
                                        current.above = nodes[i]
                                        break
                                #in between current and prev
                                elif current.y < nodes[i].y:
                                    current.below = nodes[i]
                                    nodes[i].above = current
                                    nodes[i].below = prev
                                    prev.above = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.above
                            break

                    #keep going
                    else:
                        prev = current
                        current = current.left
            #cant go left but can go up
            elif start_node.left == "" and start_node.above != "":
                prev = start_node
                current = start_node.above
                while True: 
                    #above of current node
                    if current.y > nodes[i].y:
                        #cant go up and cant go left
                        if current.above == "" and current.right == "":
                            nodes[i].right = current
                            current.left = nodes[i]
                            break
                        #cant go up but can go left
                        elif current.above == "" and current.right != "":
                            prev = current
                            current = current.left
                            while True: 
                                #right of current node
                                if current.x < nodes[i].x:
                                    if current.right == "":
                                        nodes[i].right = current
                                        current.left = nodes[i]
                                        break
                                #inbetween current and prev
                                elif current.x > nodes[i].x:
                                    current.right = nodes[i]
                                    nodes[i].left = current
                                    nodes[i].right = prev
                                    prev.left = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.left
                            
                    #doesnt need to go up any more
                    elif current.y < nodes[i].y:
                        #cant go left
                        if current.left == "":
                            current.left = nodes[i]
                            nodes[i].right = current
                        # needs to go left
                        elif current.right != "":
                            prev = current
                            current = current.left
                            while True: 
                                #lfet of current node
                                if current.x < nodes[i].x:
                                    if current.left == "":
                                        nodes[i].left = current
                                        current.right = nodes[i]
                                        break
                                #inbetween current and prev
                                elif current.x > nodes[i].x:
                                    current.right = nodes[i]
                                    nodes[i].left = current
                                    nodes[i].right = prev
                                    prev.left = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.left
                        break
                    #keep going
                    else:
                        prev = current
                        current = current.above
                break

        #below right
        elif start_node.x < nodes[i].x and start_node.y < nodes[i].y:
            # no nodes to the below or to the right 
            if start_node.right == "" and start_node.below == "" and start_node.below_right == "":
                start_node.below_right = nodes[i]
                nodes[i].above_left = current
            #nodes to the right
            elif start_node.right != "":
                prev = start_node
                current = start_node.right
                while True:
                    #right of current node
                    if current.x <= nodes[i].x:
                        #cant go anymore right and cant go up
                        if current.right == "" and current.below == "":
                            current.below = nodes[i]
                            nodes[i].above = current
                            break
                        #cant go right but can go down
                        elif current.right == "" and current.below != "":
                            prev = start_node
                            current = start_node.below
                            while True: 
                                #left of current node
                                if current.y > nodes[i].y:
                                    if current.below == "":
                                        nodes[i].above = current
                                        current.below = nodes[i]
                                        break
                                #in between current and prev
                                elif current.y < nodes[i].y:
                                    current.above = nodes[i]
                                    nodes[i].below = current
                                    nodes[i].above = prev
                                    prev.below = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.below
                            break
                        #doesnt need to go anymore right
                    elif current.x >= nodes[i].x:
                        #cant go down
                        if current.below == "":
                            current.below = nodes[i]
                            nodes[i].above = current
                            break
                        #needs to go down
                        if current.below != "":
                            prev = start_node
                            current = start_node.below
                            while True: 
                                #left of current node
                                if current.y > nodes[i].y:
                                    if current.below == "":
                                        nodes[i].above = current
                                        current.below = nodes[i]
                                        break
                                #in between current and prev
                                elif current.y < nodes[i].y:
                                    current.above = nodes[i]
                                    nodes[i].below = current
                                    nodes[i].above = prev
                                    prev.below = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.below
                            break
                    else:
                        prev = current
                        current = current.right
            #cant go right but can go down
            elif start_node.right == "" and start_node.below != "":
                prev = start_node
                current = start_node.below
                while True:
                    #below of current node
                    if current.y > nodes[i].y:
                        #cant go down and cant go to the right
                        if current.down == "" and current.right == "":
                            nodes[i].left = current
                            current.right = nodes[i]
                            break
                        #cant go down but can go right
                        elif current.below == "" and current.right != "":
                            prev = current
                            current = current.right
                            while True: 
                                #right of current node
                                if current.x < nodes[i].x:
                                    if current.right == "":
                                        nodes[i].left = current
                                        current.right = nodes[i]
                                        break
                                #inbetween current and prev
                                elif current.x > nodes[i].x:
                                    current.left = nodes[i]
                                    nodes[i].right = current
                                    nodes[i].left = prev
                                    prev.right = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.right
                    
                    #doesnt need to go down anymore
                    elif current.y > nodes[i].y:
                        #cant go right
                        if current.right == "":
                            current.right = nodes[i]
                            nodes[i].left = current
                            break
                        #needs to go right
                        elif current.x < nodes[i].y:
                            prev = current
                            current = current.right
                            while True: 
                                #right of current node
                                if current.x < nodes[i].x:
                                    if current.right == "":
                                        nodes[i].left = current
                                        current.right = nodes[i]
                                        break
                                #inbetween current and prev
                                elif current.x > nodes[i].x:
                                    current.left = nodes[i]
                                    nodes[i].right = current
                                    nodes[i].left = prev
                                    prev.right = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.right
                            break
                    #keep going
                    else:
                        prev = current
                        current = current.below
                break
          
        #below left
        elif start_node.x > nodes[i].x and start_node.y < nodes[i].y:
            #no nodes to below or to the left
            if start_node.left == "" and start_node.below == "" and start_node.below_right == "":
                start_node.below_right = nodes[i]
                nodes[i].above_left = start_node
            #nodes to the left
            elif start_node.left != "":
                prev = start_node
                current = start_node.left
                while True:
                    #left of the current node
                    if current.x >= nodes[i].x:
                        #cant fo anymore right and cant go up
                        if current.left == "" and current.below == "":
                            current.below = nodes[i]
                            nodes[i].above = current
                            break
                        #cant go right but can go down
                        elif current.left == "" and current.below != "":
                            prev = current
                            current = current.below
                            while True: 
                                #left of current node
                                if current.y > nodes[i].y:
                                    if current.below == "":
                                        nodes[i].above = current
                                        current.below = nodes[i]
                                        break
                                #in between current and prev
                                elif current.y < nodes[i].y:
                                    current.above = nodes[i]
                                    nodes[i].below = current
                                    nodes[i].above = prev
                                    prev.below = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.below
                            break
                    #doesnt need to go anymore left
                    elif current.x <= nodes[i].x:
                        #cant go down
                        if current.below == "":
                            current.below = nodes[i]
                            nodes[i].above = current
                            break
                        #needs to go down
                        if current.below != "":
                            prev = start_node
                            current = start_node.below
                            while True: 
                                #left of current node
                                if current.y > nodes[i].y:
                                    if current.below == "":
                                        nodes[i].above = current
                                        current.below = nodes[i]
                                        break
                                #in between current and prev
                                elif current.y < nodes[i].y:
                                    current.above = nodes[i]
                                    nodes[i].below = current
                                    nodes[i].above = prev
                                    prev.below = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.below
                            break
                    else:
                        prev = current
                        current = current.left
            #cant fo left but can go down
            elif start_node.left == "" and start_node.below != "":
                prev = start_node
                current = start_node.below
                while True:
                    #below of current node
                    if current.y > nodes[i].y:
                        #cant fo down and cant go right
                        if current.down == "" and current.left == "":
                            nodes[i].left = current
                            current.right = nodes[i]
                            break
                        #cant fo down but can go left
                        elif current.below == "" and current.left != "":
                            prev = current
                            current = current.left
                            while True: 
                                #left of current node
                                if current.x > nodes[i].x:
                                    if current.left == "":
                                        nodes[i].right = current
                                        current.left = nodes[i]
                                        break
                                #in between current and prev
                                elif current.x < nodes[i].x:
                                    current.right = nodes[i]
                                    nodes[i].left = current
                                    nodes[i].right = prev
                                    prev.left = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.left
                    #doesnt need to go down anymore
                    elif current.y < nodes[i].y:
                        #cant go left
                        if current.left == "":
                            current.left = nodes[i]
                            nodes[i].rigth = current
                            break
                        #needs to go left
                        elif current.x < nodes[i].x:
                            prev = current
                            current = current.left
                            while True: 
                                #left of current node
                                if current.x > nodes[i].x:
                                    if current.left == "":
                                        nodes[i].right = current
                                        current.left = nodes[i]
                                        break
                                #in between current and prev
                                elif current.x < nodes[i].x:
                                    current.right = nodes[i]
                                    nodes[i].left = current
                                    nodes[i].right = prev
                                    prev.left = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.left
                            break
                    #keep goiong
                    else:
                        prev = current
                        current = current.below
                break

    nodes[start].print_node()
    #print out nodes
    for i in nodes:
        if nodes[i] == start_node or nodes[i] == nodes[i].printed:
            continue
        nodes[i].print_node()

    return 0


#function to parse the json file from NFA to DFA converter
def parse_json(data):

    node_data = data["nodes"]
    nodes = {}

    #create nodes
    for i in node_data:
        initial = False
        accepting = False
        if(i['label'] == data['fsa']['startState']):
            initial = True
    
        try:
            if i["acceptState"] == True:
                accepting = True
        except:
            accepting = False

        n = Node(i['label'],i['transitionText'],accepting,initial,i['loc']['x'],i['loc']['y'])
        nodes[i['label']] = n
    
    layout_nodes(nodes,data['fsa']['startState'])

    #print the paths
    for i in node_data:
        for j in i['transitionText']:
            label = i['transitionText'][j]
            for k in range(len(label)):
                if label[k] == 'Îµ':
                    label[k] = "\\epsilon"
            
            str_label = ""
            for k in range(len(label)):
                str_label += label[k]
                if len(label) > 1 and k != len(label)-1:
                    str_label += ","

            if(i['label'] == j ):
                print("\\path (" + i['label'] + ") edge [loop below] node {$" , str_label , "$} (" + j +");")
            else:
                print("\\path (" + i['label'] + ") edge [bend right] node {$" , str_label , "$} (" + j +");")

#function to parse the text file fromt he STEM program
def parse_stem(file):
    nodes = {}
    lines = file.readlines()
    start_node = 0

    for i in range(5,len(lines)):
        if(lines[i] == "\n"):
            break
        
        words = lines[i].split()

        initial = False
        accepting = False

        if words[3] == "true":
            initial = True
        if words[4] == "true":
            accepting = True

        n = Node(words[0],"",accepting,initial,float(words[1]),float(words[2]) * -1)
        if initial == True:
            start_node = words[0]

        nodes[words[0]] = n

    layout_nodes(nodes,start_node)

    for i in range(16,len(lines)):
        if(lines[i] == "\n"):
            break

        words = lines[i].split()

        from_node = words[0]
        to_node = words[1]
        move = ""

        if words[len(words)-1] == "RIGHT":
            move = "R"
        if words[len(words)-1] == "LEFT":
            move = "L"


        if len(words) < 5:
            if(from_node == to_node):
                print("\\path (" + from_node + ") edge [loop above]   node {$ ||" + move+ "$} (" + to_node + ");")
            else:
                print("\\path (" + from_node + ") edge [bend right]   node {$ ||" + move+ "$} (" + to_node + ");")
        else:
            if(from_node == to_node):
                print("\\path (" + from_node + ") edge [loop above]   node {$ " + words[1] + "|" + words[2] + "|"+ move+ "$} (" + to_node + ");")
            else:
                print("\\path (" + from_node + ") edge [bend right]   node {$ " + words[1] + "|" + words[2] + "|"+ move+ "$} (" + to_node + ");")
                    
def main(argv):
    inputfile = ''
    outputfile = ''
    opts, args = getopt.getopt(argv,"hi:",["ifile="])
    for opt, arg in opts:
        if opt == '-h':
            print ('latexgen.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    try:
        file = open(inputfile)
        data = json.load(file)
        parse_json(data)
    except:
        file = open(inputfile)
        parse_stem(file)
    

if __name__ == "__main__":
   main(sys.argv[1:])

