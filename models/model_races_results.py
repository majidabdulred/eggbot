from datetime import datetime


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
        self.name = json.get("name") if json.get("name") else json.get("id")
        self.chickRaces = json.get("chickRaces")
        self.createdAt = json.get("createdAt")
        self.updatedAt = json.get("updatedAt")
        self.owner = json.get("owner")
        self.bonusBawk = json.get("bonusBawk")
        self.raceEarnings = json.get("raceEarnings") if json.get("raceEarnings") else 0


class Terrain:
    def __init__(self, json):
        self.name = json.get("name")
        self.image = json.get("image")


class RaceModel:
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
        self.endsAt = datetime.strptime(json.get("endsAt"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d %b %H:%M UTC")
        self.payoutAttempts = json.get("payoutAttempts")
        self.type = json.get("type")
        self.group = json.get("group")
        self.feeUSD = json.get("feeUSD")
        self.prizePoolUSD = json.get("prizePoolUSD")
        self.createdAt = datetime.strptime(json.get("createdAt"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d %b %H:%M UTC")

        self.updatedAt = self.endsAt = datetime.strptime(json.get("updatedAt"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
            "%d %b %H:%M UTC")

        self.terrain = Terrain(json.get("terrain")) if json.get("terrain") else None


class RowsModel:
    def __init__(self, json):
        self.id = json.get("id")
        self.raceId = json.get("raceId")
        self.chickens = []
        for chick in json.get("chickens"):
            self.chickens.append(Chicken(chick))
        self.race = RaceModel(json.get("race")) if json.get("race") else None


class RaceResults:

    def __init__(self, json) -> None:
        self.count = json.get("count")
        self.totalRaces = json.get("totalRaces")
        self.totalEarnings = json.get("totalEarnings")
        self.rows = []
        for row in json.get("rows"):
            self.rows.append(RowsModel(row))
