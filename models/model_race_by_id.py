from datetime import datetime


class RaceByIdModel:
    def __init__(self, json):
        self.id = json.get("id")
        self.name = json.get("name")
        self.peckingOrder = json.get("peckingOrder")
        self.terrainId = json.get("terrainId")
        self.distance = json.get("distance")
        self.fee = json.get("fee")
        self.maxCapacity = json.get("maxCapacity")
        self.currentCapacity = json.get("currentCapacity")
        self.location = json.get("location")
        self.minimumStartDelay = json.get("minimumStartDelay")
        self.status = json.get("status")
        self.startTime = json.get("startTime")
        self.prizePool = json.get("prizePool")
        self.paidStatus = json.get("paidStatus")
        self.unlimitPO = json.get("unlimitPO")
        self.startsAt = datetime.strptime(json.get("startsAt"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d %b %H:%M UTC")
        self.endsAt = json.get("endsAt")
        self.payoutAttempts = json.get("payoutAttempts")
        self.type = json.get("type")
        self.group = json.get("group")
        self.feeUSD = json.get("feeUSD")
        self.prizePoolUSD = json.get("prizePoolUSD")
        self.createdAt = json.get("createdAt")
        self.updatedAt = json.get("updatedAt")
        self.terrain = Terrain(json.get("terrain")) if json.get("terrain") else None
        self.lanes = []
        for lane in json.get("lanes"):
            self.lanes.append(Lane(lane))


class Terrain:
    def __init__(self, json):
        self.name = json.get("name")
        self.image = json.get("image")


class Lane:
    def __init__(self, json):
        self.laneNumber = json.get("laneNumber")
        self.assignedAt = json.get("assignedAt")
        self.chickenId = json.get("chickenId")
        self.userWalletId = json.get("userWalletId")
        self.userWallet = UserWallet(json.get("userWallet")) if json.get("userWallet") else None
        self.chicken = Chicken(json.get("chicken")) if json.get("chicken") else None

    def __lt__(self, other):
        return self.chicken < other.chicken

    def __le__(self, other):
        return self.chicken <= other.chicken

    def __eq__(self, other):
        return self.chicken == other.chicken

    def __ne__(self, other):
        return self.chicken != other.chicken

    def __gt__(self, other):
        return self.chicken > other.chicken

    def __ge__(self, other):
        return self.chicken >= other.chicken


class UserWallet:
    def __init__(self, json):
        self.username = json.get("username")


class Chicken:

    def __init__(self, json):
        self.id = json.get("id")
        self.chknId = json.get("chknId")
        self.heritage = json.get("heritage")
        self.perfection = json.get("perfection")
        self.stock = json.get("stock")
        self.talent = json.get("talent")
        self.image = json.get("image")
        self.gender = json.get("gender")
        self.animal = json.get("animal")
        self.baseBody = json.get("baseBody")
        self.stripes = json.get("stripes")
        self.eyesType = json.get("eyesType")
        self.beakColor = json.get("beakColor")
        self.beakAccessory = json.get("beakAccessory")
        self.combColor = json.get("combColor")
        self.wattleColor = json.get("wattleColor")
        self.legs = json.get("legs")
        self.background = json.get("background")
        self.races = json.get("races")
        self.firsts = json.get("firsts")
        self.seconds = json.get("seconds")
        self.thirds = json.get("thirds")
        self.earnings = json.get("earnings")
        self.situation = json.get("situation")
        self.poPoints = json.get("poPoints")
        self.hair = json.get("hair")
        self.necklace = json.get("necklace")
        self.glasses = json.get("glasses")
        self.jacket = json.get("jacket")
        self.shoes = json.get("shoes")
        self.fatherID = json.get("fatherID")
        self.motherID = json.get("motherID")
        self.name = json.get("name")[:18] if json.get("name") else json.get("id")
        self.chickRaces = json.get("chickRaces")
        self.createdAt = json.get("createdAt")
        self.updatedAt = json.get("updatedAt")
        self.position = json.get("position")
        self.owner = json.get("owner")[:18]
        self.cumulativeSegmentSize = "{0:.2f}".format(json.get("cumulativeSegmentSize"))
        self.raceEarnings = json.get("raceEarnings")
        self.performance = f"{json.get('firsts')}/{json.get('seconds')}/{json.get('thirds')}"

    def __lt__(self, other):
        return self.position < other.position

    def __gt__(self, other):
        return self.position > other.position

    def __eq__(self, other):
        return self.position == other.position

    def __le__(self, other):
        return self.position <= other.position

    def __ge__(self, other):
        return self.position >= other.position

    def __ne__(self, other):
        return self.position != other.position

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
