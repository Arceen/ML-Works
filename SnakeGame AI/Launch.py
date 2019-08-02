import sys, pygame
import time
import random
from snakebody import SnakeBody


#init
pygame.init()
#start
begin = False
#score mechanics
score = 0
incscore = 100
#number of blocks in a row or column
sblocks = 20
gridsize= sblocks+2
GridBlocks = [[0 for i in range(gridsize)] for j in range(gridsize)]
#initialize borders
for i in range(gridsize):
    GridBlocks[0][i] = 1
    GridBlocks[i][0] = 1
    GridBlocks[i][gridsize-1] = 1
    GridBlocks[gridsize-1][i] = 1

filename = "data.csv"
dfile = open(filename, 'w')
iter = 0
for i in range(gridsize):
    for j in range(gridsize):
        dfile.write(str(iter)+",")
        iter += 1

dfile.write("\n")
dfile.close()

#Game Window
windowsize = width, height = 1280, 768
screen = pygame.display.set_mode(windowsize)
pygame.display.set_caption('Snake Game')

#iterator variables for easy creation
bwidth = 32
bheight = 32

#Speed of Snake
# Speed should mean the amount of displacement in one move of the snake
speed = bwidth

#Color Const
BLACK = 10, 10, 10
WHITE = 230, 230, 230
RED = 222, 155, 55
GREEN = 0, 255, 0
BLUE = 0, 0, 255
BCOLOR = 80, 173, 125
HCOLOR = (112, 80, 180)
GRIDCOLOR = (190, 190, 190)
BEANCOLOR = 20, 180, 60
BC = [(190, 100, 80), (80, 173, 125), (135, 206, 250)]
BALLCOLOR = BCOLOR

#magic bean
magicbeanalive = False
mbx = 0
mby = 0

#go big condition
getbig = False

# Now the only problem I can think of is how inferring from random variable(0, 3) into directionx and directiony
#lets use dictionary
directionary = {
    "LEFT" : [-1, 0],
    "UP" : [0, -1],
    "RIGHT" : [1, 0],
    "BOTTOM" : [0, 1],
}

# ------------------Init Snake-----------------
snakehead = None
#snake initialization of 2 part snake from the middle of the gamebox
midx1 = int(sblocks/2)*int(bwidth) - int(bwidth/2)
midx2 = int(sblocks/2)*int(bwidth) + int(bwidth/2)
midy1 = midx1
midy2 = midx1

# headdirection
headdirection = "RIGHT"
# create snake head
snakehead = SnakeBody(midx1, midy1, True)
# The tail creation
snakehead.next = SnakeBody(midx2, midy2, False)
# -----------------End init Snake ----------------------

#did some minor modification on structure

#Game Theory
# I want to divide the entire window into sblock x sblock size of blocks where the snake can run
# Now to make the snake I want to use a linked list where each data body part is going to be a
# circle class object and all of them will be chained to each other



#Now that the positions and directions are fixed
#Lets draw



# --------- Draw Functions ----------
def gamebasegrid(screen):

    #draw the base game graphics
    for i in range(sblocks):
        for j in range(sblocks):
            pygame.draw.rect(screen, GRIDCOLOR, pygame.Rect((j*bwidth, i*bheight), (bwidth, bheight)),1)
    

def drawscore():
    myfont = pygame.font.SysFont('Comis Sans MS', 25)
    textsurface1 = myfont.render('Your Score: ', False, WHITE)
    screen.blit(textsurface1, (930, 200))

    myfont = pygame.font.SysFont('Comis Sans MS', 30)
    textsurface2 = myfont.render(str(score), False, GREEN)
    screen.blit(textsurface2, (1100, 200))


def drawdirection():
    global headdirection
    myfont = pygame.font.SysFont('Comis Sans MS', 25)
    textsurface1 = myfont.render('Current Direction: ', False, WHITE)
    screen.blit(textsurface1, (930, 500))

    myfont = pygame.font.SysFont('Comis Sans MS', 30)
    textsurface2 = myfont.render(headdirection, False, (255,255,255))
    screen.blit(textsurface2, (1100, 500))



def drawSnake(snake):
    #draw the current snake part
    if snake:
        if snake.head:
            BALLCOLOR = HCOLOR
        else:
            BALLCOLOR = BCOLOR
        pygame.draw.circle(screen, BALLCOLOR, (snake.x, snake.y), int(bwidth/2)-1, 0)
    else:
        return
    if snake.next:
        drawSnake(snake.next)

def drawmagicbeans(mbx, mby):
    tx = defercord(mbx)
    ty = defercord(mby)
    
    pygame.draw.circle(screen, BEANCOLOR, (tx,ty), int(bwidth/4), 0)



# --------- End Draw Functions ----------

# --------- Logic Functions ----------

# We have to infer grid pos from the x, y coordinates and vice versa

def updatescore():
    global score
    global incscore
    score += incscore

def infercord(x):
    return int((x + int(bwidth/2))/int(bwidth))

def defercord(x):
    return int(x)*int(bwidth) - int(bwidth/2)

# Lets update the directions of the snake parts
def updateSnakeAuto(snake, pos, grow):
    global magicbeanalive
    global BCOLOR
    global BEANCOLOR
    #update snake positions after controlled by user or AI
    if snake.head: 
        if GridBlocks[infercord(pos[1])][infercord(pos[0])] == 2:
            print("BeanTime")
            grow = True
        elif GridBlocks[infercord(pos[1])][infercord(pos[0])] == 1:
            print("Played yourself ")
    if snake.next:
        updateSnakeAuto(snake.next, (snake.x, snake.y), grow)
    else:
        #Just Delete the tail cord from the collision grid
        if not grow:
            GridBlocks[infercord(snake.y)][infercord(snake.x)] = 0
            
        else:
            #create another snakepart
            print("snake should grow")
            snake.next = SnakeBody(snake.x, snake.y, False)
            GridBlocks[infercord(snake.y)][infercord(snake.x)] = 1
            magicbeanalive = False
            BCOLOR = BEANCOLOR
            updatescore()
            
    snake.x=pos[0]
    snake.y=pos[1]
    if snake.head:
        if GridBlocks[infercord(snake.y)][infercord(snake.x)] == 1:
            print("Congrats! You played yourself!")
            exit()

        else:
            GridBlocks[infercord(snake.y)][infercord(snake.x)] = 1
            print(infercord(snake.x))
            print(infercord(snake.y))
        
    return snake

def calculateheadpos(dir):
    posx = snakehead.x + speed * dir[0]
    posy = snakehead.y + speed * dir[1]
    return posx, posy

def magicbeans():
    # find a place where nothing is Blocking and place a magic bean on it
    # lets just use two rand vars and find a place with no 1
    global mbx
    global mby
    global BEANCOLOR
    while GridBlocks[mby][mbx] == 1:
        print("magic")
        mbx = random.randint(1, sblocks)
        mby = random.randint(1, sblocks)
    
    GridBlocks[mby][mbx] = 2
    BEANCOLOR =  BC[random.randint(0, 2)]

    return mbx, mby


# --------- End Logic Functions ----------



# --------- Info and other help Functions ----------

def checkbeanalive():
    global magicbeanalive
    if not magicbeanalive:
        mbx, mby = magicbeans()
        magicbeanalive = True

def printgrid():
    for i in range(gridsize):
        print(GridBlocks[i])    


def pressspacetostart():

    screen.fill(WHITE)
    myfont = pygame.font.SysFont('Comis Sans MS', 50)
    textsurface = myfont.render('Press SPACE to Start', False, (0, 0, 0))
    screen.blit(textsurface, (480, 300))
    myfont = pygame.font.SysFont('Comis Sans MS', 30)
    textsurface = myfont.render('Use Arrow keys for control', False, (0, 0, 0))
    screen.blit(textsurface, (520, 500))
    pygame.display.flip()


    

def waitforstart():
    pressspacetostart()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


#----------------------AI Helper function--------------------
# #Send the current game state to a csv file
# #so that the ai can make the predictions



# def statetocsv():
#     global GridBlocks
#     global gridsize
#     filename = "data.csv"
#     dfile = open(filename, 'a')
#     for i in range(gridsize):
#         for j in range(gridsize):
#             dfile.write(str(GridBlocks[i][j])+",")

    
#     dfile.write("\n")
#     dfile.close()

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.position[0] < other.position[0] | ((self.position[0]==other.position[0]) & (self.position[1] < other.position[1]))
        
#Method should return Right, left, top, bottom
def Astarsearch(maze, startpos, endpos):
    maze = list(zip(*maze))
    start = Node(None, startpos)
    end_node = Node(None, endpos)
    print(startpos)
    print(endpos)
    open_list = []
    closed_list = []
    open_list.append(start)
    while len(open_list) > 0:
        # print("inside while loop")
        #find the minimum f=g+h value
        current_node = open_list[0]
        current_index = 0
        # for i in open_list:
        #     print([i.position[0], i.position[1]], end='--->')
        #     print(i.f)
            

        for index, item in enumerate(open_list):
            
            if item.position == end_node.position:
                current_node = item
                current_index = index
                break
            elif item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # print(current_node.position)
        # print(end_node.position)
        # Found the goal
        if current_node.position == end_node.position:
            # print("inside this shitt\n\n\n\n\n")
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            dirpath = []
            px = startpos[0]
            py = startpos[1]
            for x in path[::-1][1:]: 
            # Return reversed path
            # print(x)
            # print("New Location: ", end=' ')
            # print([x])
            # print("Value of new location: ", end=' ')
            # print(maze[x[1]] [x[0]])
            
                tx = x[0] - px
                ty = x[1] - py
                # print(tx)
                # print(ty)
                if tx == 0 and ty == -1:
                    dirpath.append("UP")
                elif tx == 0 and ty == 1:
                    dirpath.append("BOTTOM")
                elif tx == -1 and ty == 0:
                    dirpath.append("LEFT")
                elif tx== 1 and ty == 0:
                    dirpath.append("RIGHT")
                px = x[0]
                py = x[1]
            return dirpath
            sys.exit()

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = [current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]
            # print(node_position)
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze)-1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 1:
                print("not adding it")
                tl  = []
                for d in open_list:
                    if d not in tl:
                        tl.append(d)
                open_list = tl
                print([x.position for x in open_list])
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
        # print("Children:")
        # print([x.position for x in children])
        # Loop through children
        for child in children:
            f = False
            # open_list.sort()
            # print("1current child:")
            # print([child.position])
            # print("1Closed List:")
            # print([x.position for x in closed_list])
            # print("1Open List:")
            # print([x.position for x in open_list])

            for closed_child in closed_list:
                if child == closed_child:
                    f = True
                    # print(startpos)
                    # print(endpos)
                    # print(child.position)
                    # print(child.f)
                    # print("Child already in closed list")
                    
                    
            if f:
                continue


            # for i in range(1, len(open_list)):
            #     if open_list[i] == open_list[i-1]:
            #         print("THIS POS:")
            #         print(open_list[i].position)
            #         print("Open List:")
            #         print([x.position for x in open_list])
            #         print("END POS:")
            #         print(end_node.position)
            #         printgrid()
            #         sys.exit()
            
            # print("2current child:")
            # print([child.position])
            # print("2Closed List:")
            # print([x.position for x in closed_list])
            # print("2Open List:")
            # print([x.position for x in open_list])
            f = False
            # Child is on the closed list

            

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            # print(child.f)
            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    f = True
                    # print("Child already in oprn list")
            
            if f:
                continue

            # Add the child to the open list
            open_list.append(child)


path = []
# -------------------- GAME --------------------------------
# Game loop
while True:
    #Check if game has begun yet 
    if not begin:
        waitforstart()
        begin = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    # key = pygame.key.get_pressed()
    
    # if key[pygame.K_UP] and headdirection != "BOTTOM":
    #     headdirection = "UP"
    # if key[pygame.K_DOWN] and headdirection != "UP":
    #     headdirection = "BOTTOM"
    # if key[pygame.K_LEFT] and headdirection != "RIGHT":
    #     headdirection = "LEFT"
    # if key[pygame.K_RIGHT] and headdirection != "LEFT":
    #     headdirection = "RIGHT"

    #calculate where to go. i.e. find headdirection. "LEFT", "RIGHT", "TOP", "BOTTOM"
    
    if not (mbx == 0 & mby == 0) and not path:
        path = Astarsearch(GridBlocks, [infercord(snakehead.x), infercord(snakehead.y)], [mbx, mby])
        print(headdirection)
        print([infercord(snakehead.x), infercord(snakehead.y)])
        
    else:
        headdirection = "RIGHT"
    if path:
        headdirection = path.pop(0)
    screen.fill(BLACK)
    gamebasegrid(screen)
    #update positions
    snakehead = updateSnakeAuto(snakehead, calculateheadpos(directionary[headdirection]), False)
    #Drawing the snake
    drawSnake(snakehead)
    checkbeanalive()
    drawmagicbeans(mbx, mby)
    drawscore()
    drawdirection()
    printgrid()
    #statetocsv()
    pygame.display.flip()

    wtime = 100
    # Our fps will be 1/wtime
    # pygame.time.wait(wtime)


# we will have to create a 26 x 26 matrix to store all the occupied stuff as well as
# the boundaries so that we can keep track of collision

