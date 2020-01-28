import turtle
import winsound

wn = turtle.Screen()
wn.title("Pong by Abhai")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

#score
score_a = 0

#turn
turn = 1

#Paddle A
paddle_a = turtle.Turtle()
paddle_a.shape("square")
paddle_a.speed(0)
paddle_a.color("blue")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350,0)

#Paddle B
paddle_b = turtle.Turtle()
paddle_b.shape("square")
paddle_b.speed(0)
paddle_b.color("green")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350,0)

#Ball
ball = turtle.Turtle()
ball.shape("circle")
ball.speed(0)
ball.color("white")
ball.penup()
ball.goto(0,0)
ball.dx = 0.4
ball.dy = 0.4

#Pen
pen1 = turtle.Turtle()
pen1.speed(0)
pen1.shape("square")
pen1.color("white")
pen1.penup()
pen1.hideturtle()
pen1.goto(0,260)
pen1.write("Survival Mode",align="center",font=("Courier",24,"normal"))

#Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,230)
pen.write("Player A turns: 0",align="center",font=("Courier",16,"normal"))

def paddle_a_up():
    y = paddle_a.ycor()
    y = y+20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y = y+30
    paddle_b.sety(y)
    
def paddle_a_down():
    y = paddle_a.ycor()
    y = y-20
    paddle_a.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y = y-30
    paddle_b.sety(y)

wn.listen()
wn.onkeypress(paddle_a_up,"w")
wn.onkeypress(paddle_a_down,"s")


#Main game loop
calculatedForTurn = False
while True:
    wn.update()
    #Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    

    #Border checking
    if ball.ycor() > 290:
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 350:
        pen.clear()
        #pen.write("Player A: {}  Player B: {}".format(score_a, score_b),align="center",font=("Courier",24,"normal"))
        ball.goto(0,0)
        ball.dx *= -1
        calculatedForTurn = False
        turn += 1

    if ball.xcor() < -350:
        pen.clear()
        score_a = 0
        pen.write("Player A turns: 0",align="center",font=("Courier",16,"normal"))
        ball.goto(0,0)
        ball.dx *= -1
        calculatedForTurn = False
        turn += 1
    
    if turn % 2 != 0 and calculatedForTurn == False:
        #Calculate target position
        init_dx = 40
        init_dy = 40

        initX = ball.xcor()
        initY = ball.ycor()
        print("Starting calculation turn {} ball x {} ball y{}".format(turn,initX,initY))
        simulation_exit = False
        move_exit = False

        while simulation_exit == False:
            print("Calculating x {} and y{}".format(initX,initY))

            if initY > 290:
                initY = 290
                init_dy *= -1
                print("reversing y {}".format(initY))

            if initY < -290:
                initY = -290
                init_dy *= -1
                print("reversing y {}".format(initY))

            if initX == 0 and ball.dy > 0 and init_dy < 0:
                init_dy *= -1
            
            if initX == 0 and ball.dy < 0 and init_dy > 0:
                init_dy *= -1
            
            if initX <= -339 and ball.dy > 0 and init_dy < 0:
                print("Correcting simulation direction when -")
                init_dy *= -1
            
            if initX <= -339 and ball.dy < 0 and init_dy > 0:
                print("Correcting simulation direction when +")
                init_dy *= -1
            
            #if initX <= -339.8 and initY < 0:
                #if init_dy < 0:
                 #   init_dy *= -1

            if initX >= 340:
                print("y coordinate found {}".format(initY))
                simulation_exit = True

            initX = initX + init_dx
            initY = initY + init_dy

        #Move paddle_b to init_dy
        while(move_exit == False):
            print("Paddle y {} target y {}".format(paddle_b.ycor(),initY))
            if(initY > paddle_b.ycor() -20 and initY < paddle_b.ycor() + 20 ):
                print("paddle moved x {} y {}".format(paddle_b.xcor(),paddle_b.ycor()))
                calculatedForTurn = True
                move_exit = True
            elif paddle_b.ycor() > initY:
                paddle_b_down()
                print("Moving paddle down x {} y {} and ball y {}".format(paddle_b.xcor(),paddle_b.ycor(), initY))
            elif paddle_b.ycor() < initY:
                paddle_b_up()
                print("Moving paddle up x {} y {} and ball y {}".format(paddle_b.xcor(),paddle_b.ycor(),initY))


    #Paddle bouncing
    if ball.xcor() < -340 and ball.xcor() > -350 and (ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() -50 ):
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.setx(-340)
        ball.dx *= -1
        calculatedForTurn = False
        turn += 1
        score_a +=1
        pen.clear()
        pen.write("Player A turns: {}".format(score_a),align="center",font=("Courier",16,"normal"))
        print("Paddle bounced ball x{} y{} dx{} dy{} simulation x{} y{} paddle x{} y{}".format(ball.xcor(),ball.ycor(),ball.dx,ball.dy,init_dx,init_dy,paddle_a.xcor(),paddle_a.ycor()))

    if ball.xcor() > 340 and ball.xcor() < 350 and (ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() -50 ):
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.setx(340)
        ball.dx *= -1
        calculatedForTurn = False
        turn += 1    
    