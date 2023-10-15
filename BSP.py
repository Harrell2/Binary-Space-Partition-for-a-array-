import numpy as np
import random
import tcod

def start(y, x):
    map = np.zeros((y,x), order = "F")
    return map

Tree = []
class node:
    """
    a class that holds the array of a sub map and its top right corners xy
    each node will be added to the Tree list so it will be easier to navigate and find its parent node
    """
    def __init__(self, map,y,x):
        self.map = map
        self.y = y
        self.x = x

class final_node:
    """
    the same as the node class but is used in the final splitting function
    """
    def __init__(self, map, y , x, type):
        self.map = map
        self.y = y
        self.x = x
        self.type = type

def split(map, min_deviation, max_deviation):    
    """
    a funtion that takes an array and splits it into two arrays
    min_deviation and max is to control how far from the center the split will be
    this function will return a list of two sub maps
    """

    #0 is y or horizontal slice while 1 is x or vertical slice
    direction = 0
    
    #checks if the width of the map is smaller than its length, used to avoid skinny rooms
    if map.shape[0] < map.shape[1]:
        direction = 1
    #finds the dimensions of the side we chose(x or y)
    size = map.shape[direction]
    #finds where we are going to cut the map
    slice_part = random.randrange(int(size/2)- min_deviation, int(size/2) + max_deviation)
    
    #splits the map into two sub maps
    if direction == 0: # horizontal
        first_half = map[:slice_part]
        second_half = map[slice_part:]
    else: # vertical
        first_half = map[0:, :slice_part]
        second_half = map[0:, slice_part:]
    
    return first_half, second_half, direction, slice_part

        
def partitions(nodes,pointer):
    """
    a funtion that handles all of the logic of going through the submaps and finding what to do with its children
    Also used to find the xy cords of each sub map
    Takes a list of arrays(or sub maps) as nodes
    Pointer is a variable that used to find the parent nodes xy
    Returns the children of all the sub maps iterated through
    
    """
    
    #creates a empty list which will hold all of the children maps
    sub_map = []
    #checks if the input is a list or not (helps with the iteration logic)
    if type(nodes) != list:
        refrence = [nodes]
    else:
        refrence = nodes
    #iterates through all maps inputted
    for i in refrence:
        
        pointer += 1
        #sets the xy to the parents xy
        x = Tree[pointer].x
        y = Tree[pointer].y
        
        #gets the children maps by splitting the current map(refer to split function for more info)
        splot = split(i,10,10)
        first_half = splot[0]
        second_half = splot[1]
        #gets the splits angle and position
        direction = splot[2]
        slice_part = splot[3]
        
        #checks if the split was horizontal or vertical
        #this is used to find the second_halfs xy as the first_half has the same as its parent
        if direction == 0: #horizontal
            x2 = x
            y2 = y + slice_part
        elif direction == 1: #vertical
            x2 = x + slice_part
            y2 = y
       
        #adds the children nodes to the Tree so the program can find its own childrens xy
        Tree.append(node(first_half,y,x))
        Tree.append(node(second_half,y2,x2))
        
        #adds the children maps to sub maps to so it can be iterated up
        sub_map.append(first_half)
        sub_map.append(second_half)
    return sub_map, pointer
    
def recursive_partitions(depth, main_map):
    """
    recursivly calls on the partitions function to split the map multiple times
    depth is how many times you want to split the map
    """
    #adds the main map as the root of Tree
    Tree.append(node(main_map,0,0))
    #first partition that takes the original map as its loop
    #this is to make iterations simple and to initiate the pointer 
    popping = partitions(main_map,-1)
    new_maps = popping[0]
    pointer = popping[1]
    #loops through all partitions execpt the first
    for i in range(depth - 1):
        #gets the sub maps and pointer from previous partions
        popping = partitions(new_maps, pointer)
        new_maps = popping[0]
        pointer = popping[1]
    #finds the final maps created and puts them in a List with their xy    
    end_map = Tree[len(new_maps)-1:]
    end_maps = []
    for count, z in enumerate(end_map):
        if count > 8:
            count -= 9
        end_maps.append(final_node(z.map,z.y,z.x,type = count))
        
    return end_maps
        



def main():
    final_BSP = recursive_partitions(4, start(60,100))
    screen_width = 100
    screen_height = 60
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset = tileset,
        title = "BSP",
        vsync = True,
    ) as context:
        console = tcod.Console(screen_width, screen_height, order = "F")
        
        while True:
            
            for i in final_BSP:
                x = i.x
                y = i.y
                map = i.map
                type = i.type + 1
                
                for pos, value in np.ndenumerate(map):
                         
                    pos_y, *rest, pos_x = pos
                    pos_x = pos_x + x
                    pos_y = pos_y + y
                    
                    match type:
                        case 1:
                            color = (255,255,255)
                        case 2:
                            color = (255,255,0)
                        case 3:
                            color = (255,0,255)
                        case 4:
                            color = (255,0,255)
                        case 5:
                            color = (0,255,255)
                        case 6:
                            color = (100,255,100)
                        case 7:
                            color = (255,100,255)
                        case 8:
                            color = (50,50,50)
                        
                    console.print(x = pos_x, y = pos_y, string = " ", bg = color)
                
                    
            context.present(console)
            console.clear()
            
            
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()
                    
if __name__ == "__main__":
    main()
