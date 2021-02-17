import turtle

s = turtle.getscreen()
t = turtle.Turtle()

# Set the initial position of the Turtle
turtle.setpos((0,0))
turtle.penup()

t.speed(1)
t.pen(pencolor="black", fillcolor="black", pensize=10, speed=1)
t.goto(0,-100)
turtle.pendown()
t.goto(100,-100)

t.clear()
turtle.done()