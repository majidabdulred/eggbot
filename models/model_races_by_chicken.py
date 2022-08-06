class RacesByChicken:
    def __init__(self, json) -> None:
        self.count = json.get("count")

        self.rows = []
        for row in json.get("rows"):
            self.rows.append(Row(row))


class Row:

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
        self.startsAt = json.get("startsAt")
        self.endsAt = json.get("endsAt")
        self.payoutAttempts = json.get("payoutAttempts")
        self.type = json.get("type")
        self.group = json.get("group")
        self.feeUSD = json.get("feeUSD")
        self.prizePoolUSD = json.get("prizePoolUSD")
        self.createdAt = json.get("createdAt")
        self.updatedAt = json.get("updatedAt")
        self.result = Result(json.get("result")) if json.get("result") else None
        self.terrain = Terrain(json.get("terrain")) if json.get("terrain") else None

class Terrain:
    def __init__(self, json):
        self.name = json.get("name")
        self.image = json.get("image")

class Result:

    def __init__(self, json):
        self.id = json.get("id")
        self.raceId = json.get("raceId")
        self.chickens = []
        for chick in json.get("chickens"):
            self.chickens.append(Chicken(chick))


class Chicken:
    def __init__(self, json) -> None:
        self.id = json.get("id")
        self.raceEarnings = json.get("raceEarnings") if json.get("raceEarnings") else 0
