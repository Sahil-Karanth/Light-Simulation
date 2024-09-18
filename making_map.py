from values import Values

WIDTH = Values.SCREEN_WIDTH // Values.CELL_SIZE
HEIGHT = Values.SCREEN_HEIGHT // Values.CELL_SIZE

with open("map.txt", "w") as file:
    
    file.write("1"*WIDTH + "\n")
    for i in range(HEIGHT-2):
        file.write(f"1{'0'*(WIDTH-2)}1\n")
    file.write("1"*WIDTH + "\n")