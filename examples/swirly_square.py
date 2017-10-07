from turtle import *
cat=100
loops = 0
while loops < 100:
    loops +=1
    forward (cat)
    backward (50)
    right (90)
    pencolor("red")
    forward (50)
    right (90)
    forward (50)
    right (90)
    forward (40)
    pencolor("Blue")
    left (1)
    cat=cat+5
done()
