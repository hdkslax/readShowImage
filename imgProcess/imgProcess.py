import imgUtils


imgOriginal = imgUtils.getImage("week9-photo.jpg")
width = 600
height = 400

flag = True
while(flag):
    userInput = int(input("Please input a number(0/1/2/3/4): "))
    if userInput == 0:
        flag = False
    elif userInput == 1:
        imgUtils.showImage(imgOriginal)
    elif userInput == 2:
        rmvRImg = list()
        # 2 - remove all R
        for x in range(width):
            row = list()
            for y in range(height):
                row.append([0, imgOriginal[x][y][1],imgOriginal[x][y][2]])
            rmvRImg.append(row)
        imgUtils.saveImage(rmvRImg, "removeR.jpg")
    elif userInput == 3:
        geryImg = list()
        # 3 - grey image
        for x in range(width):
            row = list()
            for y in range(height):
                pixelAvg = (imgOriginal[x][y][0] + imgOriginal[x][y][1] + imgOriginal[x][y][2]) / 3
                pixel = [pixelAvg, pixelAvg, pixelAvg]
                row.append(pixel)
            geryImg.append(row)

        imgUtils.saveImage(geryImg, "grey.jpg")
    elif userInput == 4:
        # 4 - reverse image
        imgRev = list()
        for x in range(width):
            row = list()
            for y in range(height):
                row.append(imgOriginal[x][height - 1 - y])
            imgRev.append(row)
        imgUtils.saveImage(imgRev, "reverse.jpg")
    else:
        print("Sorry, I don’t understand", userInput)




