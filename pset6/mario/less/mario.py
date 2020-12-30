import cs50

# print ("x", end="")

while True:
    height = cs50.get_int("Height: ")
    if (height >= 1 and height <= 8):
        break

# height = height + 1

for i in range(height):
    for k in range(height - i, 1, -1):
        print(" ", end="")
    for j in range(0, i + 1, 1):
        print("#", end="")
    print()
