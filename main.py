import turtle
import time

class SquareCollisionObject(object):

    def __init__(self,origin=0,size=32):
        self.Bounds = (origin,size)

    def GetCollide(self,position):
        return ((position[0]+self.Bounds[0],position[1]+self.Bounds[0]),(position[0]+self.Bounds[1],position[1]+self.Bounds[1]))

    def TestCollideWith(self,CollisionObject,OurPosition,CollisionPosition):
        OurCollide = self.GetCollide(OurPosition)
        TheirCollide = CollisionObject.GetCollide(CollisionPosition)

        if OurCollide[0][0] >= TheirCollide[0][0] and OurCollide[0][1] >= TheirCollide[0][1] and OurCollide[1][0] <= TheirCollide[1][0] and OurCollide[1][1] <= TheirCollide[1][1]:
            return True
        return False        

class TileEntity(object):

    def __init__(self,position,gravity=False,pusher=False,collisions=True,tooltext=""):
        self.turt = turtle.Turtle()
        self.position = position
        self.turt.hideturtle()

        self.Gravity = gravity
        self.GravitySteps = 120 #Delay between gravity simulations
        self.NextGravityGametime = GameTime.value+self.GravitySteps

        self.CanPush = pusher

        self.Collision = SquareCollisionObject()

        self.turt.color("#FFFFFF","#222222")
        self.turt.speed("fastest")

        self.ToolText = tooltext

    def GravitySimulation(self):
        if self.Gravity and self.NextGravityGametime <= GameTime.value:
            self.Down()
            self.ResetFall()

    def render(self):
        self.GravitySimulation()
        self.turt.goto(self.position[0],self.position[1])
        self.turt.clear()

        self.turt.begin_fill()
        
        for i in range(4):
            self.turt.forward(32)
            self.turt.right(90)

        self.turt.end_fill()
        if self.ToolText: self.turt.write(self.ToolText)

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
                if not i.Collision or i == self: #If it's not got collision, or it is us, ignore.
                    continue
                if self.Collision.TestCollideWith(i.Collision,self.position,i.position):
                    return i
        return False

    def ResetFall(self):
        self.NextGravityGametime = GameTime.value+self.GravitySteps

    def Movement(self,direction): #Direction is an integer, 0 = "UP" 1 + "DOWN" 2 = "LEFT" 3 = "RIGHT"
        #print(direction)
        if direction < 2:
            self.position = (self.position[0],self.position[1]+((32,-32)[direction]))
            collider = self.TestCollision()
            if collider:
                if collider.Gravity and self.CanPush:
                    collider.Movement(direction)
                    collider.ResetFall()
                    self.ResetFall()
                else:
                    self.position = (self.position[0],self.position[1]+((-32,32)[direction]))
                    self.ResetFall()
        else:
            self.position = (self.position[0]+((-32,32)[direction-2]),self.position[1])
            collider = self.TestCollision()
            if collider:
                if collider.Gravity and self.CanPush:
                    collider.Movement(direction)
                    collider.ResetFall()
                    self.ResetFall()
                else:
                    self.position = (self.position[0],self.position[1]+((32,-32)[direction-2]))
                    self.ResetFall()
        

class Player(TileEntity):

    def __init__(self,position):
        super().__init__(position,True,True)

        Screen.onkey(self.Up,"w")
        Screen.onkey(self.Down,"s")
        Screen.onkey(self.Left,"a")
        Screen.onkey(self.Right,"d")

        self.turt.color("#FFEEEE","#442222")

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
    RenderList.append(TileEntity((32*i,0),False,True))

RenderList.append(TileEntity((64,32),True,False))

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
