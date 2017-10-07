import turtle

def draw_tree(length, depth):
    jonney.forward(length)
    if depth > 1:
        jonney.left(45)
        draw_tree(length/2, depth-1)
        jonney.left(90)
        draw_tree(length/2, depth-1)
        jonney.right(135)
    jonney.right(180)
    jonney.forward(length)

def draw_snowflake(length, depth):
    draw_fractal(length, depth-1)
    jonney.left(120)
    draw_fractal(length, depth-1)
    jonney.left(120)
    draw_fractal(length, depth-1)


def draw_fractal(length, depth):
    if depth == 1:
        jonney.forward(length)
    else:
        draw_fractal(length, depth-1)
    jonney.right(60)
    if depth == 1:
        jonney.forward(length)
    else:
        draw_fractal(length, depth-1)
    jonney.left(120)
    if depth == 1:
        jonney.forward(length)
    else:
        draw_fractal(length, depth-1)
    jonney.right(60)
    if depth == 1:
        jonney.forward(length)
    else:
        draw_fractal(length, depth-1)


jonney = turtle.Turtle()
jonney.speed(0)
jonney.left(90)
jonney.width(2)
draw_tree(128,6)
jonney.width(1)
jonney.penup()
jonney.goto(210,0)
for i in range(0, 10):
    for j in range(0,10):
        jonney.pendown()
        draw_snowflake((i+j)%3+1,2)
        jonney.penup()
        jonney.setheading(90)
        jonney.forward(30)
    jonney.setheading(270)
    jonney.forward(300)
    jonney.setheading(180)
    jonney.forward(50)

turtle.exitonclick()
