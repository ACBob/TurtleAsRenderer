import turtle
import time

class TileEntity(object):

    def __init__(self,position,gravity=False,collisions=True):
        self.turt = turtle.Turtle()
        self.position = position
        self.turt.hideturtle()

        self.Gravity = gravity
        self.GravitySteps = 120 #Delay between gravity simulations
        self.NextGravityGametime = GameTime.value+self.GravitySteps

        self.Collision = collisions
        self.CollisionBounds = (0,32) #Var 1 = Top left on both axis, Var 2 = Bottom Right on both Axis.
        #In this case, it's 0,0 to the shape, and 32,32 from origin (0,0)

        self.turt.color("Green","Lime Green")
        self.turt.speed("fastest")

    def GravitySimulation(self):
        if self.Gravity and self.NextGravityGametime <= GameTime.value:
            self.Down()
            self.NextGravityGametime = GameTime.value+self.GravitySteps

    def GetCollide(self):
        return ((self.position[0]+self.CollisionBounds[0],self.position[1]+self.CollisionBounds[0]),(self.position[0]+self.CollisionBounds[1],self.position[1]+self.CollisionBounds[1])) #For testing collisions!

    def render(self):
        self.GravitySimulation()
        self.turt.goto(self.position[0],self.position[1])
        self.turt.clear()

        self.turt.begin_fill()
        
        for i in range(4):
            self.turt.forward(32)
            self.turt.right(90)

        self.turt.end_fill()

    def Up(self):
        #self.position = (self.position[0],self.position[1] + 32)
        self.Movement(0)
    def Down(self):
        #self.position = (self.position[0],self.position[1] - 32)
        self.Movement(1)
    def Left(self):
        #self.position = (self.position[0] - 32,self.position[1])
        self.Movement(2)
    def Right(self):
        #self.position = (self.position[0] + 32,self.position[1])
        self.Movement(3)

    def TestCollision(self):
        if self.Collision:
            for i in RenderList:
                if not i.Collision:
                    continue #If it doesn't have collision, what are we doing?!
                TestCollideBounds = i.GetCollide()
                CollideBounds = self.GetCollide()
                #print(CollideBounds,TestCollideBounds)
                if CollideBounds[0][0] >= TestCollideBounds[0][0] and CollideBounds[0][1] >= TestCollideBounds[0][1] and CollideBounds[1][0] <= TestCollideBounds[1][0] and CollideBounds[1][1] <= TestCollideBounds[1][1]:
                    #print("Collide")
                    return True
        return False

    def Movement(self,direction): #Direction is an integer, 0 = "UP" 1 + "DOWN" 2 = "LEFT" 3 = "RIGHT"
        #print(direction)
        if direction < 2:
            self.position = (self.position[0],self.position[1]+((32,-32)[direction]))
            if self.TestCollision():
                self.position = (self.position[0],self.position[1]+((-32,32)[direction]))
        else:
            self.position = (self.position[0]+((-32,32)[direction-2]),self.position[1])
            if self.TestCollision():
                self.position = (self.position[0],self.position[1]+((32,-32)[direction-2]))
        

class Player(TileEntity):

    def __init__(self,position):
        super().__init__(position,True)

        Screen.onkey(self.Up,"w")
        Screen.onkey(self.Down,"s")
        Screen.onkey(self.Left,"a")
        Screen.onkey(self.Right,"d")

        self.turt.color("Red","Pink")

class Clock(object):

    def __init__(self,startnum=0):
        print("Clock {} initialised.".format(self))
        self.value = 0
        self.LastCall = time.time()
        self.Calls = [0]

    def tick(self,amount=1):
        self.Calls = self.Calls[-10:]
        self.Calls.append(time.time()-self.LastCall)
        #print(self.Calls)
        self.value += 1

    def GetAverageCalls(self,indice=10):
        avg = 0
        for i in self.Calls[indice:]:
            avg+=i
        if avg > 0 and len(self.Calls) > 0:
            avg = avg/indice
        return avg

global Screen
Screen = turtle.Screen()
Screen.delay(0)
Screen.bgcolor("Black")

global GameTime #Turtle doesn't have the luxury of built-in time knowledge.
GameTime = Clock()

global RenderList
RenderList = []

player = Player((0,64))
print(player)

for i in range(10):
    RenderList.append(TileEntity((32*i,0)))

Screen.listen()

#You can comment out "turtle.tracer" and "turtle.update" if you want some screen flicker.

#9223372036854775807

while True:
    turtle.tracer(0,0) #Hide Changes
    for i in RenderList: i.render()
    player.render()
    turtle.update() #Push Changes
    GameTime.tick()
    
    Screen.title(GameTime.GetAverageCalls(10))
