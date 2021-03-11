import turtle

# s = turtle.getscreen()
# t = turtle.Turtle()

# value1 = 200
# value2 = 40

# def add(a,b):
#     c = a + b
#     return c

# # Set the initial position of the Turtle
# turtle.setpos((0,0))
# turtle.penup()

# t.speed(1)
# t.pen(pencolor="black", fillcolor="black", pensize=10, speed=1)
# t.goto(0,-100)
# turtle.pendown()
# t.goto(100,-100)
# t.forward(value1)
# t.right(90)
# t.forward(add(100,20))

# t.clear()
# turtle.done()

# #
# #
# #


# Set Turtle screen = image size
s = turtle.getscreen()

# Set turtle
t = turtle.Turtle()

# Unchanged turtle commands
t.speed(1)
t.pen(pencolor="black", fillcolor="black", pensize=5, speed=1)

# Set the initial position of the Turtle
t.dot(50)
t.penup()
t.goto(-200,70)
t.pendown()
t.fd(300)


t.clear()
turtle.done()