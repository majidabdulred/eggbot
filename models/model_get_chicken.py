def get_chickens_model(json) -> dict:
    data = {}
    for chick in json.get("body"):
        data[chick.get("id")] = Chicken(chick)
    return data


class Chicken:

    def __init__(self, json) -> None:
        self.id = json.get("id")
        self.name = json.get("name") if json.get("name") else json.get("id")
        self.tokenId = json.get("tokenId")
        self.image = json.get("image")
        info = json.get("info")
        self.heritage = info.get("heritage")
        self.perfection = info.get("perfection")
        self.stock = info.get("stock")
        self.talent = info.get("talent")
        self.gender = info.get("gender")
        self.baseBody = info.get("baseBody")
        self.stripes = info.get("stripes")
        self.eyesType = info.get("eyesType")
        self.beakColor = info.get("beakColor")
        self.combColor = info.get("combColor")
        self.wattleColor = info.get("wattleColor")
        self.beakAccessory = info.get("beakAccessory")
        self.background = info.get("background")
        self.legs = info.get("legs")
        self.races = info.get("races")
        self.firsts = info.get("firsts")
        self.seconds = info.get("seconds")
        self.thirds = info.get("thirds")
        self.performance = f"{info.get('firsts')}/{info.get('seconds')}/{info.get('thirds')}"
        self.earnings = info.get("earnings") if info.get("earnings") else 0
        self.situation = info.get("situation")
        self.poPoints = info.get("poPoints")
