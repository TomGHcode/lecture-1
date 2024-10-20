#pyhton code

import turtle

def draw_star(sides, length):
	if sides % 2 == 0:
		print("Error: n must be an odd number.")
		return

	angle = 180 - (180 / sides)
	
	for _ in range(sides):
		turtle.forward(length)
		turtle.right(angle)

print("Ēnter the number of sides and length of the star")
x=int(input("sides: " ))
y=int(input("length: "))
turtle.speed(10)
draw_star(x, y)
turtle.done()
