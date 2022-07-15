"""
 * Building and Resource classes related to the game Supremacy 1914 in Python
 * @author petrvvv, 8olwerk@gmail.com
"""

from buildings import settings


class Resources:

    def __init__(self, quantity, resourceType):
        self.quantity = quantity
        self.resourceType = resourceType

    def __str__(self):
        return f"{self.quantity:<10} {settings.resourceToName[self.resourceType]}"


class Building:

    def __init__(self, ID, name, buildtime, dayAvaible, hitpointsLevel,
                 maxHitpoints, buildCost, upkeepCost, hp=1):

        self.__ID = ID
        self.__name = name
        self.__buildtime = buildtime
        self.__dayAvailable = dayAvaible
        self.__hitpointsLevel = hitpointsLevel
        self.__maxHitpoints = maxHitpoints
        self.__buildCost = buildCost
        self.__upkeepCost = upkeepCost
        self.__moraleFactor = settings.buildingNametoMoraleFactor.get(self.__name, 0)
        self.hp = hp

    def getID(self):
        return self.__ID

    def getName(self):
        return self.__name

    def getBuildTime(self):
        return self.__buildtime

    def getMoraleFactor(self):
        return self.__moraleFactor

    def cancelBuildRefund(self):
        'the building is reset to last hitpoint finished, the unfinished remainder refunded'
        self.hp = int(self.hp * self.__maxHitpoints)
        return f"{(1-self.hp) * 100}% refunded"

    def getBuildCost(self):
        return self.__buildCost

    def getUpkeepCost(self):
        if self.__upkeepCost:
            return self.__upkeepCost
        return "No upkeep cost required."

    def getDayAvailable(self):
        return self.__dayAvailable

    def __str__(self):

        s =  f"\n\n{self.__name.upper()}\n" + \
        f"hitpoints per level: {self.__hitpointsLevel}\n" + \
        f"maximum hitpoints: {self.__maxHitpoints}" + \
        f"available at day: {self.__dayAvailable}\n" + \
        f"Build time/level: {round(self.__buildtime / 3600, 2)} hours\n" + \
        'Construction cost required:\n' + \
        "\n".join(sorted([str(Resources(q, rtype)) for rtype, q in self.__buildCost.items()], key=lambda t: t[1]))

        if self.__upkeepCost:
            s += '\nUpkeep cost required/day:\n'
            s += "\n".join(sorted([str(Resources(q,rtype)) for rtype,q in self.__upkeepCost.items()], key=lambda t: t[1]))
        return s



class economicalBuilding(Building):

    """
    custom subclass for buildings that influence resource output
    """

    def __init__(self, ID, name, buildtime, dayAvaible, hitpointsLevel,
                 maxHitpoints, buildCost, upkeepCost, productionLevel):
        super().__init__(ID, name, buildtime, dayAvaible, hitpointsLevel,
                 maxHitpoints, buildCost, upkeepCost)

        self.__baseProductionBonus = self.getBaseProductionBonus(productionLevel)

    def getActualProductionBonus(self):
        'hp-factor needs to be reduced to hitpoint segment'
        return self.__baseProductionBonus * int(self.hp * self.__maxHitpoints)/self.__maxHitpoints

    def checkUniformity(self, productionLevel):
        if len(set(v for k,v in productionLevel.items())) == 1:
            return True

    def getBaseProductionBonus(self, productionLevel):
        if self.checkUniformity(productionLevel):
            return productionLevel.popitem()[1]
        else:
            print('productionbonus is not applied to all resources uniformly anymore')

    def __str__(self):
        return super().__str__() + f"\nproductionBase: {100* self.__baseProductionBonus}%"