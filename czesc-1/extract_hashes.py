with open("dane.csv", "r") as f:
    f.readline() # omijanie nagłówka nagłówek
    for line in f.readlines():
        print(f"{line.split(',')[2]}:{line.split(',')[3]}",end='') # format przyjazny dla hashcata