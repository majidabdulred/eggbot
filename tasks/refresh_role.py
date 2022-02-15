from discord.utils import get
from db.users import col, get_user, update_chick_sum
from db.chickens import get_many_chickens
from tasks.updatedb import main_update_chicks_one

from db.local_db import server


class UpdateUser:

    def __init__(self, bot, user):
        self.bot = bot
        self.cluck200_ = get(server.guild.roles, name="Cluck Norris")
        self.attia100_199 = get(server.guild.roles, name="Attila The Hen")
        self.chook50_99 = get(server.guild.roles, name="The Big Chook")
        self.coop15_49 = get(server.guild.roles, name="Coop Commander")
        self.rancher1_14 = get(server.guild.roles, name="Rancher")
        self.all_roles = [self.cluck200_, self.chook50_99, self.coop15_49, self.attia100_199, self.rancher1_14]
        self.total_score_str = ""
        self.chickens = {"Serama": 0, "Sultan": 0, "Lakenvelder": 0, "Dorking": 0}
        self.chickens_str = ""
        self.str_to_send = ""
        self.wallet_str = ""
        self.changed = False
        self.already_have_role = ""
        self.changed_str = ""
        self.user = user
        self.stop = False
        self.userdb = None
        if None in self.all_roles:
            print("A ROLE NOT FOUND,", self.all_roles)
            self.stop = True
        print("INITIALISED")
        self.count = 0

    async def exists(self):
        self.userdb = await get_user(self.user.id)
        if self.userdb is None:
            return False
        return True

    async def refresh_single_user(self):
        if self.stop:
            print("END")
            return
        await main_update_chicks_one(self.userdb)
        self.userdb = await get_user(self.user.id)
        await self._update_member_role(self.userdb)

    def _count_chick_sum(self, userdb):
        csum = 0
        for acc in userdb["accounts"]:
            csum += sum(acc["chicks"])
        return csum

    async def _update_member_role(self, userdb):
        self.wallet_str = f"Wallet address is `{userdb['accounts'][0]['address']}`"
        total_score = await self._get_total_score(userdb)
        self.total_score_str = f"Your Total Points are **{total_score}** . "
        if total_score > 0:
            self.chickens_str = "You have "
        for name, amount in self.chickens.items():
            if amount > 0:
                self.chickens_str += f"**{amount}** {name} "

        print(f"{userdb['_id']} : SCORE : {total_score}")
        if total_score <= 0 and any([ro for ro in self.user.roles if ro in self.all_roles]):
            await self.user.remove_roles(*self.all_roles)
            self.changed = True
        elif 1 <= total_score < 15:
            await self._data_add_to_list(self.rancher1_14)
        elif 15 <= total_score < 50:
            await self._data_add_to_list(self.coop15_49)
        elif 50 <= total_score < 100:
            await self._data_add_to_list(self.chook50_99)
        elif 100 <= total_score < 200:
            await self._data_add_to_list(self.attia100_199)
        elif total_score >= 200:
            await self._data_add_to_list(self.cluck200_)
        await update_chick_sum(self.user.id, self._count_chick_sum(userdb))

    async def _data_add_to_list(self, role):
        if role not in self.user.roles:
            await self.user.add_roles(*[role])
            self.changed_str += f"You have been given role **{role.name}**."
            self.changed = True
        other_roles = [self.cluck200_, self.chook50_99, self.coop15_49, self.attia100_199, self.rancher1_14]
        other_roles.remove(role)
        user_other_roles = [ro for ro in self.user.roles if ro in other_roles]
        if len(user_other_roles) > 0:
            self.changed = True
            await self.user.remove_roles(*other_roles)
        self.already_have_role = f"You already have role **{role.name}**."

    async def _get_total_score(self, user):
        chicks = user["accounts"][0]["chicks"]
        if len(chicks) <= 0:
            return 0

        chickens = await get_many_chickens(chicks)
        score = 0
        for chick in chickens:
            score += self._get_score(chick)
        return score

    def _get_score(self, chick):
        if chick["Heritage"] == "Serama":
            self.chickens["Serama"] += 1
            return 7
        elif chick["Heritage"] == "Sultan":
            self.chickens["Sultan"] += 1

            return 5
        elif chick["Heritage"] == "Lakenvelder":
            self.chickens["Lakenvelder"] += 1

            return 3
        elif chick["Heritage"] == "Dorking":
            self.chickens["Dorking"] += 1

            return 1
        else:
            pass
