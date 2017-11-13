from turtle import *
cat=100
loops = 0
while loops < 100:
    loops +=1
    turtle.forward (cat)
    turtle.backward (50)
    turtle.right (90)
    turtle.forward (50)
    turtle.right (90)
    turtle.forward (50)
    turtle.right (90)
    turtle.forward (40)
    turtle.left (1)
    cat=cat+5

