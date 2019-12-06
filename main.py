import turtle

class TileEntity(object):

    def __init__(self,position,gravity=False):
        self.turt = turtle.Turtle()
        self.position = position
        self.turt.hideturtle()

        self.Gravity = gravity
        self.GravitySteps = 60 #Delay between gravity simulations
        self.NextGravityGametime = GameTime+self.GravitySteps

        self.turt.color("Green","Lime Green")
        self.turt.speed("fastest")

    def GravitySimulation(self):
        if self.Gravity and self.NextGravityGametime <= GameTime:
            self.Down()
            self.NextGravityGametime = GameTime+self.GravitySteps

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
        self.position = (self.position[0],self.position[1] + 32)
    def Down(self):
        self.position = (self.position[0],self.position[1] - 32)
    def Left(self):
        self.position = (self.position[0] - 32,self.position[1])
    def Right(self):
        self.position = (self.position[0] + 32,self.position[1])

        

class Player(TileEntity):

    def __init__(self,position):
        super().__init__(position,True)

        Screen.onkey(self.Up,"w")
        Screen.onkey(self.Down,"s")
        Screen.onkey(self.Left,"a")
        Screen.onkey(self.Right,"d")

        self.turt.color("Red","Pink")



global Screen
Screen = turtle.Screen()
Screen.delay(0)
Screen.bgcolor("Black")

global GameTime #Turtle doesn't have the luxury of built-in time knowledge.
GameTime = 0

player = Player((0,64))
print(player)

renderlist = []

for i in range(10):
    renderlist.append(TileEntity((32*i,0)))

Screen.listen()

#You can comment out "turtle.tracer" and "turtle.update" if you want some screen flicker.

while True:
    turtle.tracer(0,0) #Hide Changes
    for i in renderlist: i.render()
    player.render()
    turtle.update() #Push Changes
    GameTime+=1
    Screen.title(GameTime)
