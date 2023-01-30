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

#function to parse the json file from NFA to DFA converter
def parse_json(data):

    node_data = data["nodes"]
    nodes = {}

    #create nodes
    for i in node_data:
        initial = False
        if(i['label'] == data['fsa']['startState']):
            initial == True

        n = Node(i['label'],i['transitionText'],False,initial,i['loc']['x'],i['loc']['y'])
       
        nodes[i['label']] = n
    
    #layout nodes
    
    start_node = nodes[data['fsa']['startState']]
    for i in nodes:
        if nodes[i] == start_node:
            continue
        #right
        if start_node.x < nodes[i].x and start_node.y + 10 > nodes[i].y and start_node.y - 10 < nodes[i].y:
            print(start_node.right == "")
            if start_node.right == "":
                nodes[i].left = start_node
                start_node.right = nodes[i]
                print("test" + i)
            else:
                print("test" + i)
                prev = start_node
                current = start_node.right
                while True: 
                    if current.x < nodes[i].x:
                        if current.right == "":
                            nodes[i].left = current
                            current.right = nodes[i]
                            break
                    elif current.x > nodes[i].x:
                        current.left = nodes[i]
                        nodes[i].right = current
                        nodes[i].left = prev
                        prev.right = nodes[i]
                        break
                    else:
                        prev = current
                        current = current.right
        
        #left 
        if start_node.x > nodes[i].x and start_node.y + 10 > nodes[i].y and start_node.y - 10 < nodes[i].y:
            if start_node.left == "":
                nodes[i].right = start_node
                start_node.left = nodes[i]
            else:
                prev = start_node
                current = start_node.left
                while True: 
                    if current.x < nodes[i].x:
                        if current.left == "":
                            nodes[i].right = current
                            current.left = nodes[i]
                            break
                    elif current.x < nodes[i].x:
                        current.right = nodes[i]
                        nodes[i].left = current
                        nodes[i].right = prev
                        prev.left = nodes[i]
                        break
                    else:
                        prev = current
                        current = current.right
        
    #print out nodes
    for i in nodes:
        print(i,"right", nodes[i].right, "left" ,nodes[i].left)

    #print out paths


    return 0

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

