class AircraftRelation(object):
    def __init__(self):
        self.chineseName = ""
        self.englishName = ""
        self.flowed = ""
        self.developmentTime = ""
        self.attendedTime = ""
        self.developedCountries = ""
        self.equipmentState = ""
        self.theAircraftType = ""
        self.theFirstFlightTime = ""


class AircraftAttribute(object):
    def __init__(self):
        self.wingspan = ""
        self.length = ""
        self.height = ""
        self.mainWheelPitch = ""
        self.frontMainPitch = ""
        self.normalTakeoff = ""
        self.maximumTakeoffWeight = ""
        self.plugInCapacity = ""
        self.fuel = ""
        self.practicalLimit = ""
        self.takeOffDistance = ""
        self.landingDistance = ""
        self.range = ""
        self.limitOverload = ""


class Aircraft(object):
    def __init__(self):
        self.name = ""
        self.img = ""
        self.content = ""
        self.relation = {}
        self.attribute = {}


class KeyMapping(object):

    def __init__(self):
        self.map = {"": "", "": "", "": ""}
