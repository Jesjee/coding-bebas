import turtle
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Red Heart")
screen.setup(width=800, height=800)
screen.tracer(0)

love = turtle.Turtle()
love.hideturtle()
love.speed(0)
love.color("red")
love.width(3)
love.penup()

fill_turtle = turtle.Turtle()
fill_turtle.hideturtle()
fill_turtle.speed(0)
fill_turtle.color("red")

sparkle = turtle.Turtle()
sparkle.hideturtle()
sparkle.speed(0)
sparkle.color("white")
sparkle.penup()

def heart_points(steps=200):
    from math import sin, cos, pi
    points = []
    for i in range(steps + 1):
        t = (i / steps) * 2 * pi
        x = 16 * (sin(t) ** 3)
        y = 13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)
        points.append((x * 20, y * 20))
    return points

points = heart_points(steps=300)

index = 0
filled = False

def sparkle_effect(t, width, height, count=80):
    t.clear()
    for _ in range(count):
        x = random.randint(-width//2, width//2)
        y = random.randint(-height//2, height//2)
        size = random.randint(2, 6)
        t.goto(x, y)
        t.dot(size, "white")

def fill_heart():
    fill_turtle.penup()
    fill_turtle.goto(points[0])
    fill_turtle.pendown()
    fill_turtle.begin_fill()
    for pt in points:
        fill_turtle.goto(pt)
    fill_turtle.end_fill()

def draw_heart_step():
    global index, filled
    sparkle_effect(sparkle, 800, 800, count=100)

    if not filled:
        if index == 0:
            love.penup()
            love.goto(points[0])
            love.pendown()
        if index < len(points):
            love.goto(points[index])
            index += 1
            screen.update()
            screen.ontimer(draw_heart_step, 20)
        else:
            # isi warna dalam hati
            filled = True
            fill_heart()
            screen.update()
            # lanjut sparkle tanpa gambar ulang hati
            screen.ontimer(draw_heart_step, 100)
    else:
        # sparkle terus berjalan
        screen.update()
        screen.ontimer(draw_heart_step, 100)

draw_heart_step()

screen.mainloop()
