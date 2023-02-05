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

    def print_node(self):
        if(self.initial == True):
            print("\\node[" + "state,initial" + "] (" + self.label + ") [""] {$" + self.label + "$};")
        else:
            if(self.right != ""):
                loc = "left of = " + self.right.label
            elif(self.left != ""):
                loc = "right of =" + self.left.label
            elif(self.above != ""):
                loc = "below of =" + self.above.label
            elif(self.below != ""):
                loc = "above of = "+ self.below.label

            print("\\node[" + "state" + "] (" + self.label + ") [" + loc + "] {$" + self.label + "$};")
        



#function that will organize the nodes and print the latex code
def layout_nodes(nodes,start):
    start_node = nodes[start]
    for i in nodes:
        if nodes[i] == start_node:
            continue
        #right
        if start_node.x < nodes[i].x and start_node.y + 10 > nodes[i].y and start_node.y - 10 < nodes[i].y:
            print(start_node.right == "")
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
        elif start_node.x > nodes[i].x and start_node.y + 10 > nodes[i].y and start_node.y - 10 < nodes[i].y:
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
        elif start_node.y > nodes[i].y and start_node.x + 10 > nodes[i].x and start_node.x - 10 < nodes[i].x:
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
        elif start_node.y < nodes[i].y and start_node.x + 10 > nodes[i].x and start_node.x - 10 < nodes[i].x:
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
            #nodes to the right but not above
            elif start_node.right != "" and start_node.above == "":
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
                            nodes[i].left = nodes[i]
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
            #nodes to the left but not above
            elif start_node.left != "" and start_node.above == "":
                prev = start_node
                current = start_node.left
                while True: 
                    #left of current node
                    if current.x < nodes[i].x:
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
            #nodes to the right but not below
            elif start_node.right != "" and start_node.below == "":
                prev = start_node
                current = start_node.right
                while True: 
                    #right of current node
                    if current.x < nodes[i].x:
                        #cant go anymore right and cant go up
                        if current.right == "" and current.below == "":
                            current.below = nodes[i]
                            nodes[i].above = current
                            break
                        #cant go anymore right but can go up
                        elif current.right == "" and current.below != "":
                            prev = current
                            current = current.below
                            while True: 
                                #below of current node
                                if current.y < nodes[i].y:
                                    if current.below == "":
                                        nodes[i].above = current
                                        current.below = nodes[i]
                                        break
                                #in between current and prev
                                elif current.y > nodes[i].y:
                                    current.below = nodes[i]
                                    nodes[i].above = current
                                    nodes[i].below = prev
                                    prev.above = nodes[i]
                                    break
                                #keep going
                                else:
                                    prev = current
                                    current = current.below
                            break

                    #doesnt need to go anymore right
                    elif current.x > nodes[i].x:
                        #cant go up
                        if current.below == "":
                            current.above = nodes[i]
                            nodes[i].below = current
                            break
                        #node needs to go up
                        elif current.below != "":
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
                            nodes[i].left = nodes[i]
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
        #below left
        elif start_node.x < nodes[i].x and start_node.y < nodes[i].y:
            # no nodes to the above or to the left 
            if start_node.left == "" and start_node.below == "" and start_node.below_left == "":
                start_node.below_left = nodes[i]
            #nodes to the left but not above
            elif start_node.left != "" and start_node.below == "":
                prev = start_node
                current = start_node.left
                while True: 
                    #left of current node
                    if current.x < nodes[i].x:
                        #cant go anymore left and cant go up
                        if current.left == "" and current.below == "":
                            current.below = nodes[i]
                            nodes[i].above = current
                            break
                        #cant go anymore left but can go up
                        elif current.left == "" and current.below != "":
                            prev = current
                            current = current.below
                            while True: 
                                #left of current node
                                if current.y < nodes[i].y:
                                    if current.below == "":
                                        nodes[i].above = current
                                        current.below = nodes[i]
                                        break
                                #in between current and prev
                                elif current.y > nodes[i].y:
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
                        current = current.left
            #cant go left but can go up
            elif start_node.left == "" and start_node.above != "":
                prev = start_node
                current = start_node.above
                while True: 
                    #above of current node
                    if current.y > nodes[i].y:
                        #cant go up and cant go left
                        if current.above == "" and current.left == "":
                            nodes[i].left = current
                            current.left = nodes[i]
                            break
                        #cant go up but can go left
                        elif current.above == "" and current.left != "":
                            prev = current
                            current = current.left
                            while True: 
                                #left of current node
                                if current.x < nodes[i].x:
                                    if current.left == "":
                                        nodes[i].right = current
                                        current.left = nodes[i]
                                        break
                                #inbetween current and prev
                                elif current.x > nodes[i].x:
                                    current.left = nodes[i]
                                    nodes[i].right = current
                                    nodes[i].left = prev
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
                            nodes[i].right = nodes[i]
                            break
                        # needs to go elft
                        elif current.rileftght != "":
                            prev = current
                            current = current.left
                            while True: 
                                #left of current node
                                if current.x < nodes[i].x:
                                    if current.left == "":
                                        nodes[i].right = current
                                        current.left = nodes[i]
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
        
    #print out nodes
    for i in nodes:
        nodes[i].print_node()

    #print out paths


    return 0


#function to parse the json file from NFA to DFA converter
def parse_json(data):

    node_data = data["nodes"]
    nodes = {}

    #create nodes
    for i in node_data:
        initial = False
        if(i['label'] == data['fsa']['startState']):
            initial = True

        n = Node(i['label'],i['transitionText'],False,initial,i['loc']['x'],i['loc']['y'])
       
        nodes[i['label']] = n
    
    layout_nodes(nodes,data['fsa']['startState'])

#function to parse the text file fromt he STEM program
def parse_stem(file):
    return 0

def main(argv):
    inputfile = ''
    outputfile = ''
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    for opt, arg in opts:
        if opt == '-h':
            print ('latexgen.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    file = open(inputfile)

    try:
        data = json.load(file)
        parse_json(data)
    except:
        parse_stem(file)
    

if __name__ == "__main__":
   main(sys.argv[1:])

