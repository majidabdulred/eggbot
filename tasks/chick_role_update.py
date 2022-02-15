"""
Updates users chicks and role in discord
"""
import asyncio
from discord.utils import get
from db.users import col, update_chick_sum
from db.chickens import get_many_chickens
from tasks.updatedb import main_updater
from random import randrange
from util import mylogs

DB_CALLS = 10


class UpdateClass:

    def __init__(self, bot):
        self.bot = bot
        self.cluck200_ = get(bot.server.roles, name="Cluck Norris")
        self.attia100_199 = get(bot.server.roles, name="Attila The Hen")
        self.chook50_99 = get(bot.server.roles, name="The Big Chook")
        self.coop15_49 = get(bot.server.roles, name="Coop Commander")
        self.rancher1_14 = get(bot.server.roles, name="Rancher")
        self.all_roles = [self.cluck200_, self.chook50_99, self.coop15_49, self.attia100_199, self.rancher1_14]
        self.stop = False
        self.data_to_add_roles = []
        self.errored_tasks = []
        self.data_to_remove_roles = []
        self.errored = []
        if None in self.all_roles:
            mylogs.error(f"A ROLE NOT FOUND, {self.all_roles}")
            self.stop = True

    async def all_update_chicks(self, hours):
        await main_updater(hours)

    async def refresh_all_users(self):

        if self.stop:
            return
        update_tasks = []
        async for user in col.find():
            update_tasks.append(self._update_member_role(user))
            if len(update_tasks) >= DB_CALLS:
                await asyncio.gather(*update_tasks)
                update_tasks = []

        mylogs.info(
            f"ADD REMOVE TASKS CREATED\nADD = {len(self.data_to_add_roles)} : REMOVE {len(self.data_to_remove_roles)}")
        await asyncio.sleep(5)
        loop = asyncio.get_event_loop()

        self.count_add = 0
        self.count_remove = 0

        for task in self.data_to_remove_roles:
            loop.create_task(self._remove_role(task))
            await asyncio.sleep(.1)
        for task in self.data_to_add_roles:
            loop.create_task(self._add_role(task))
            await asyncio.sleep(.1)

        print("__DONE__")

    async def _add_role(self, data):
        user, role, userdb = data
        await user.add_roles(*[role])
        await update_chick_sum(user.id, self._count_chick_sum(userdb))
        self.count_add += 1
        mylogs.info(f"ADDED : {user.name} : {role.name} : ({self.count_add}/{len(self.data_to_add_roles)})")

    async def _remove_role(self, data):
        user, otherroles, userdb = data
        await user.remove_roles(*otherroles)
        await update_chick_sum(user.id, self._count_chick_sum(userdb))
        self.count_remove += 1
        mylogs.info(
            f"REMOVED : {user.name} : {[oa.name for oa in otherroles]}: ({self.count_remove}/{len(self.data_to_remove_roles)})")

    def _count_chick_sum(self, userdb):
        csum = 0
        for acc in userdb["accounts"]:
            csum += sum(acc["chicks"])
        return csum

    async def _update_member_role(self, userdb, refresh=False

                                  ):
        if not refresh and "chick_sum" in userdb.keys() and userdb["chick_sum"] == self._count_chick_sum(userdb):
            mylogs.debug(f"ROLE_ALREADY_SET : {userdb['_id']}")
            return
        total_score = await self._get_total_score(userdb)
        mylogs.debug(f"{userdb['_id']} : SCORE : {total_score}")

        user = self.bot.server.get_member(userdb["_id"])
        if user is None:
            self.errored.append(("DISCORD_USER_NOT_FOUND", userdb['accounts'][0]["chicks"]))
            mylogs.debug(f"USER NOT FOUND : {userdb['_id']} : {total_score}")
            return
        if total_score <= 0 and any([ro for ro in user.roles if ro in self.all_roles]):
            roles_to_remove = [ro for ro in user.roles if ro in self.all_roles]
            if len(roles_to_remove) > 0:
                self.data_to_remove_roles.append((user, roles_to_remove, userdb))
        elif 1 <= total_score < 15:
            self._data_add_to_list(user, userdb, self.rancher1_14)
        elif 15 <= total_score < 50:
            self._data_add_to_list(user, userdb, self.coop15_49)
        elif 50 <= total_score < 100:
            self._data_add_to_list(user, userdb, self.chook50_99)
        elif 100 <= total_score < 200:
            self._data_add_to_list(user, userdb, self.attia100_199)
        elif total_score >= 200:
            self._data_add_to_list(user, userdb, self.cluck200_)
        return total_score

    def _data_add_to_list(self, user, userdb, role):
        # update_chic_sum = col.update_one({"_id": user.id}, {"$set": {"chick_sum": self._count_chick_sum(userdb)}})
        pre_roles = [kl.name + "  " for kl in user.roles if kl in self.all_roles]
        mylogs.debug(f"{user.id} :  {pre_roles} : {len(pre_roles)}")

        if role not in user.roles:
            self.data_to_add_roles.append((user, role, userdb))
        other_roles = [self.cluck200_, self.chook50_99, self.coop15_49, self.attia100_199, self.rancher1_14]
        other_roles.remove(role)
        roles_to_remove = [ro for ro in user.roles if ro in other_roles]
        if len(roles_to_remove) > 0:
            self.data_to_remove_roles.append((user, roles_to_remove, userdb))

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
            return 7
        elif chick["Heritage"] == "Sultan":
            return 5
        elif chick["Heritage"] == "Lakenvelder":
            return 3
        elif chick["Heritage"] == "Dorking":
            return 1
        else:
            self.errored.append(("HERITAGE_NOT_IDENTIFIED", chick))
