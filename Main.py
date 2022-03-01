from datetime import datetime
from random import uniform as randromValue
import math
import Variables
import csv

Autos = []

def Start():
    Debug("[Started]")

    # Сколько вместится машин по горизонтали
    maxCarCountHorizontal = math.floor ((Variables.ParkHorizontalSize - Variables.VerticalRoadCount * Variables.VerticalRoadSize) / (Variables.CarHorizontalSize + Variables.Car_range))
    Debug("maxCarCountHorizontal: " + str(maxCarCountHorizontal))

    # кол-во горизонтальных проездов
    horizontalRoadCount = math.floor ((Variables.ParkVerticalSize / (Variables.CarVerticalSize + Variables.Car_range)) / 3 - 1/3)  
    Debug("horizontalRoadCount: " + str(horizontalRoadCount))

    # сколько вместится машин по вертикали
    maxCarCountVertical = math.floor ((Variables.ParkVerticalSize - horizontalRoadCount * Variables.HorizontalRoadSize) / (Variables.CarVerticalSize + Variables.Car_range))
    Debug("maxCarCountVertical: " + str(maxCarCountVertical))

    maxCarCount = math.floor (maxCarCountHorizontal * maxCarCountVertical * Variables.Dencity)
    Debug("maxCarCount: " + str(maxCarCount))

    # вероятность создания машины
    spawnProb = 10 / maxCarCount
    Debug("spawnProb: " + str(spawnProb))

    trueCarCount = 0
    parking_count_x = maxCarCountHorizontal; # Длина парковки от проезда до проезда (вертикальных)
    if (Variables.VerticalRoadCount > 0):
        parking_count_x = math.floor (maxCarCountHorizontal / (Variables.VerticalRoadCount))
    Debug("parking_count_x: " + str(parking_count_x))
    
    matrix = [0] * maxCarCountHorizontal
    for i in range(maxCarCountHorizontal):
        matrix[i] = [0] * maxCarCountVertical

    i = 0
    while (trueCarCount < maxCarCount):
        for y in range(0, maxCarCountVertical):
            realHorozontalRoadCount = math.floor ((y + 1) / 2)
            if (horizontalRoadCount == 0):
                realHorozontalRoadCount -= 1
            realVerticalRoadCount = -1
            
            for x in range(0, maxCarCountHorizontal):
                if (trueCarCount > maxCarCount):
                    break
                if (x % parking_count_x == 0):
                    realVerticalRoadCount += 1
                if (matrix[x][y] == 1):
                    continue

                if (randromValue(0, 1) > spawnProb):
                    continue

                xcoord = x * (Variables.CarHorizontalSize + Variables.Car_range) + realVerticalRoadCount * Variables.VerticalRoadSize
                ycoord = y * (Variables.CarVerticalSize + Variables.Car_range / 2) + realHorozontalRoadCount * Variables.HorizontalRoadSize
                SetCar(xcoord, ycoord)
                matrix[x][y] = 1
                trueCarCount += 1
        i += 1
        if (i > maxCarCount * 1000):
            break
    
    WriteCSV()

def Debug(msg):
    print(datetime.now().strftime("%H:%M:%S:%M: ") + str(msg))

def SetCar(xcoord, ycoord):
    Autos.append([Variables.AutoType, xcoord, ycoord])
    Debug("Car placed: " + str(xcoord) + ", " + str(ycoord))

def WriteCSV():
    Debug("Writing data...")
    try:
        file = open('output.csv', 'w')
        data = [] * Variables.ParkingsCount
        for auto in range(Variables.ParkingsCount):
            data.append(auto)
        with file:
            writer = csv.writer(file)
            writer.writerows(data)
        Debug("Data writing complete!")
    except Exception as ex:
        Debug("Error with writing data!\n" + str(ex))

Start()