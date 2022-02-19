from discord import Embed, Colour
from discord_slash import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
from prettytable import PrettyTable
from discord_slash.utils.manage_components import wait_for_component
from apis.polygonscan import get_previous_sales


def convert_address(address, owner):
    """Returns formatted address if the user is the owner"""
    if address == owner:
        return "YOU"
    elif address == "0x0000000000000000000000000000000000000000":
        return "MINTED"
    return address[:7]


class Transactions:
    def __init__(self, react, bot, address):
        self.bot = bot
        self.react = react
        self.message = react.origin_message
        # self.address = "0x9254f7f72bc6294ad6569d1ab78139121db880f6"
        self.address = address

        self.url_sales_page = f"https://opensea.io/{self.address}/chicken-derby?tab=activity&search[isSingleCollection]=true&search[chains][0]=MATIC&search[eventTypes][0]=ASSET_TRANSFER"

    async def run(self):
        await self.react.defer(edit_origin=True)
        self.data = await get_previous_sales(self.address)
        embeds, comps = self._create()
        await self.react.edit_origin(embed=embeds[0], components=[comps])
        react = await wait_for_component(self.bot, self.message, timeout=180, check=self.check_author)
        if react.custom_id == "more_token_sales":
            react = await self.sales_pagination_cycle(react, embeds)
        return react

    def check_author(self, ctx):
        return self.react.author_id == ctx.author_id

    async def sales_pagination_cycle(self, ctx, embeds):
        cycle = 0
        embeds[0].set_footer(text=Embed.Empty)
        comps = self.paginating_components()
        await ctx.edit_origin(embed=embeds[cycle], components=[comps])
        while True:
            react = await wait_for_component(self.bot, ctx.origin_message_id, timeout=180, check=self.check_author)
            if react.custom_id == "next_pag":
                cycle += 1
                if cycle >= len(embeds):
                    cycle = 0
            elif react.custom_id == "prev_pag":
                cycle -= 1
                if cycle < 0:
                    cycle = len(embeds) - 1
            elif react.custom_id == "go_back_token_sales":
                return react

            await react.edit_origin(embed=embeds[cycle])

    def paginating_components(self):
        buttons = [create_button(style=ButtonStyle.green, label="<", custom_id="prev_pag"),
                   create_button(style=ButtonStyle.green, label=">", custom_id="next_pag"),
                   create_button(style=ButtonStyle.blue, label="Go Back", custom_id="go_back_token_sales"),
                   create_button(style=ButtonStyle.URL, label="View on Opensea", url=self.url_sales_page)
                   ]
        comps = create_actionrow(*buttons)
        return comps

    def _create(self):
        embeds = self._create_embeds()
        buttons = []
        if len(embeds) > 1:
            buttons.append(create_button(style=ButtonStyle.red, label="More", custom_id="more_token_sales"))
            embeds[0].set_footer(text="More: For more transactions\n")
        buttons.append(create_button(style=ButtonStyle.blue, label="Go Back", custom_id="go_back_token_sales"))
        buttons.append(create_button(style=ButtonStyle.URL, label="View on Opensea", url=self.url_sales_page))
        comps = create_actionrow(*buttons)
        return embeds, comps

    def _create_embeds(self):
        """Paginations (list) --> list"""
        if len(self.data) == 0:
            embed = Embed(title="Token Sales", description="You have not done any transactions of Chicken Derby NFT.",
                          colour=Colour.red())
            embed.set_author(name="Chicken Derby", url=self.url_sales_page)
            return [embed]

        one_page_count = 15

        pag_data = [self.data[i * one_page_count:(i + 1) * one_page_count] for i in
                    range((len(self.data) + one_page_count - 1) // one_page_count)]
        embeds = []
        for pag in pag_data:
            tab = PrettyTable(["Sr.", "Token", "From", "To"])
            for no, tr in enumerate(pag):
                tab.add_row([f"{tr['srno']}",
                             f" {tr['tokenID']} ",
                             convert_address(tr["from"], self.address),
                             convert_address(tr["to"], self.address)
                             ])
            desc = f"Your Previous Chicken Derby NFT Transfers and sales.\n"
            embed = Embed(title="Token Sales", description=desc + "```\n" + tab.get_string() + "```",
                          colour=Colour.blue())
            embed.set_author(name="Chicken Derby", url=self.url_sales_page)
            embeds.append(embed)
        return embeds
