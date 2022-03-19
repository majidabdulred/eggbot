class Server:
    def __init__(self):
        pass


class RacedChicken:
    def __init__(self, data):
        info = data.get("info")
        self.id = data.get("tokenId") if data.get("tokenId") else info.get("tokenId")
        self.id = int(self.id) if self.id else 0
        self.name = info.get("name") if info.get("name") else info.get("id")
        self.image = info.get("image")
        self.owner = self._parse_name(info.get("owner")) if info.get("owner") else None
        self.owner_full_name = info.get("owner")
        self.races = info.get("races")
        self.performance = f"{info.get('firsts')}/{info.get('seconds')}/{info.get('thirds')}"
        self.total_earnings = info.get("earnings") if info.get("earnings") else 0
        self.POP = info.get("poPoints")
        self.perfection = info.get("perfection")
        self.this_race_earnings = info.get("race_earnings") if info.get("race_earnings") else 0
        self.race_timing = round(data["race_profile"][-1]["cumulativeSegmentSize"], 2) if data.get(
            "race_profile") else None
        self.heritage = data.get("attributes").get("heritage") if data.get("attributes") else None

    def _parse_name(self, name):
        length = len(name)
        if length <= 15:
            return name
        words = name.split()
        if len(words) >= 3 and len(na := f"{words[0]} {words[1]} {words[2]}") <= 15:
            return na
        elif len(words) >= 2 and len(na := f"{words[0]} {words[1]}") <= 15:
            return na
        elif len(words) >= 1 and len(na := f"{words[0]}") <= 15:
            return na
        else:
            return name[:15]
