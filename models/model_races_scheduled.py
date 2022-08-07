class UserWallet:
    def __init__(self, json) -> None:
        self.username = json.get("username")


class Lane:

    def __init__(self, json):
        self.laneNumber = json.get("laneNumber")
        self.assignedAt = json.get("assignedAt")
        self.chickenId = json.get("chickenId")
        self.userWalletId = json.get("userWalletId")
        self.userWallet = UserWallet(json.get("userWallet")) if json.get("userWallet") else None


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
        self.fee = float(json.get("fee"))
        self.maxCapacity = json.get("maxCapacity")
        self.currentCapacity = json.get("currentCapacity")
        self.location = json.get("location")
        self.minimumStartDelay = json.get("minimumStartDelay")
        self.status = json.get("status")
        self.startTime = json.get("startTime")
        self.prizePool = float(json.get("prizePool"))
        self.paidStatus = json.get("paidStatus")
        self.unlimitPO = json.get("unlimitPO")
        self.startsAt = json.get("startsAt")
        # datetime.strptime(json.get("createdAt"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d %b %H:%M UTC")
        self.endsAt = json.get("endsAt")
        self.payoutAttempts = json.get("payoutAttempts")
        self.type = json.get("type")
        self.group = json.get("group")
        self.feeUSD = json.get("feeUSD")
        self.prizePoolUSD = json.get("prizePoolUSD")
        self.createdAt = json.get("createdAt")
        self.updatedAt = json.get("updatedAt")
        self.lanes = []
        for lane in json["lanes"]:
            self.lanes.append(Lane(lane))
        self.terrain = Terrain(json.get("terrain"))


class ScheduledRaces:
    def __init__(self, json):
        self.count = json.get("count")
        self.rows = []
        for row in json["rows"]:
            self.rows.append(RaceModel(row))
