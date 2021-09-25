"""
解析数据的Model结构体
"""


class AircraftRelation(object):
    def __init__(self):
        self.chineseName = ""
        self.englishName = ""
        self.followed = ""
        self.developmentTime = ""
        self.attendedTime = ""
        self.developedCountries = ""
        self.equipmentState = ""
        self.theAircraftType = ""
        self.researchDevelopmentUnit = ""
        self.country = ""


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
        self.maximumMachNumber = ""
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
        self.relation = AircraftRelation()
        self.attribute = AircraftAttribute()

    def __doc__(self):
        __doc__ = {
            "relation": AircraftRelation,
            "attribute": AircraftAttribute
        }
