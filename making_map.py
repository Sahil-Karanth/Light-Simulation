from values import Values

WIDTH = Values.SCREEN_WIDTH // Values.CELL_SIZE
HEIGHT = Values.SCREEN_HEIGHT // Values.CELL_SIZE

with open("map.txt", "w") as file:
    
    file.write("2"*WIDTH + "\n")
    for i in range(HEIGHT-2):
        file.write(f"2{'0'*(WIDTH-2)}2\n")
    file.write("2"*WIDTH + "\n")