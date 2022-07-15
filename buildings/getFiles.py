import buildings.getData as getData
from collections import defaultdict
from buildings import buildingclass
import pickle


buildingObjects = defaultdict(object)
def createFiles():

    buildingArgs, economicalBuldingArgs = getData.buildings()

    for building in buildingArgs:
        buildingObjects[building[0]] = buildingclass.Building(*building)
    for eco in economicalBuldingArgs:
        buildingObjects[eco[0]] = buildingclass.economicalBuilding(*eco)

    with open('S1914_buildings.txt', 'w') as file:
        for k,v in buildingObjects.items():
            file.write(str(v))

    with open('S1914_buildings.pickle', 'wb') as handle:
        pickle.dump(buildingObjects, handle)


if __name__ == "__main__":
    createFiles()
    with open('S1914_buildings.pickle', 'rb') as file:
        for k,v in pickle.load(file).items():
            print(v)