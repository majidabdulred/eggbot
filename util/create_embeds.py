from discord import Embed
from discord_slash import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow

opensea_link = "https://opensea.io/assets/matic/0x8634666ba15ada4bbc83b9dbf285f73d9e46e4c2/"
from .slash_options import percent

from db.local_db import verify_messages


def chicken(data):
    embed = Embed(description=f"Token {data['_id']}",
                  url=f"{opensea_link}{data['_id']}?ref=0xc96b13e952e77d2f9accb33597c216d96ed91395")
    for key, value in data.items():
        if key in ("_id", "image_url"):
            continue
        if value not in percent.keys():
            suffix = ""
        elif percent[value] == "":
            suffix = ""
        else:
            suffix = f" ({percent[value]}%)"
        embed.add_field(name=key.capitalize(), value=f'{value}{suffix}')
    embed.set_image(url=data["image_url"])
    return embed


def verification_messsage():
    """Wallet verification message"""
    embed = Embed(
        description="We need to know who you are in order to give you access to some amazing perks in this "
                    "discord server. Like beta access and ranks. So click on Verify to Connect your wallet.",
        title="Verify Your wallet")
    buttons2 = [create_button(style=ButtonStyle.blue, label="Verify", custom_id="verify")]
    linkbuttons = create_actionrow(*buttons2)
    return embed, linkbuttons


def access_beta():
    """Access Beta Message"""
    embed = Embed(
        description="Click on Enroll so we can add you wallet address to our Beta list",
        title="Get Beta Access")
    buttons2 = [create_button(style=ButtonStyle.blue, label="Enroll", custom_id="enroll")]
    linkbuttons = create_actionrow(*buttons2)
    return embed, linkbuttons


def wallet_connect_message(userid):
    """Wallet verification message"""
    embed = Embed(
        description="We don't know your wallet address. Click on Connect to connect you wallet. It will take you to a "
                    "link statring with  `https://chickenderby.github.io` . \n"
                    "Click on *Connect Metamask* on the website to connect your wallet.\n\n",
        title="Connect Your Wallet")
    buttons2 = [
        create_button(style=ButtonStyle.URL, label="Connect", url=f"https://chickenderby.github.io/verify/?{userid}")]
    verify_messages[userid]["beta"] = True
    verify_messages[userid]["mode"] = "new"

    linkbuttons = create_actionrow(*buttons2)

    return embed, linkbuttons


def wallet_connect_message_2(userid):
    """Wallet verification message after changing wallet address"""
    embed = Embed(
        description="Click on **Connect** to connect your new wallet. It will take you to a "
                    "website starting with  `https://chickenderby.github.io` . \n"
                    "Click on **Connect Metamask** on the website to connect your wallet.\n\n",
        title="Connect Your Wallet")
    buttons2 = [
        create_button(style=ButtonStyle.URL, label="Connect", url=f"https://chickenderby.github.io/verify/?{userid}")]
    linkbuttons = create_actionrow(*buttons2)

    return embed, linkbuttons


def already_have_your_wallet(address):
    embed = Embed(
        description=f"Our record says your wallet address is \n`{address}`\n"
                    f"**Add** : Add this wallet to beta.\n"
                    f"**Change** : Change your wallet address.",
        title="Found an address")
    buttons2 = [create_button(style=ButtonStyle.blue, label="Add", custom_id="add_to_beta"),
                create_button(style=ButtonStyle.green, label="Change", custom_id="change_wallet")]
    linkbuttons = create_actionrow(*buttons2)

    return embed, linkbuttons


def create_change_wallet_button(msg):
    change_wallet_msg = "\n\n**Change** : To change your wallet address if you have moved your chickens."

    embed = Embed(title="Refresh", description=msg + change_wallet_msg)

    button = [create_button(style=ButtonStyle.green, label="Change Wallet", custom_id="change_wallet"),
              create_button(style=ButtonStyle.blue, label="Go Back", custom_id="go_back_refresh")]
    comps = create_actionrow(*button)
    return embed, comps


def wallet_connect_message_refresh(ctx):
    embed = Embed(
        description="Your wallet is not verified . You will need to verify your wallet in order to get roles and see your points.\n"
                    "Click on **Connect** to verify your wallet. It will take you to a "
                    "website starting with  `https://chickenderby.github.io` . \n"
                    "Click on **Connect Metamask** on the website to connect your wallet.\n\n",
        title="Connect Your Wallet")
    buttons2 = [
        create_button(style=ButtonStyle.URL, label="Connect",
                      url=f"https://chickenderby.github.io/verify/?{ctx.author_id}"),
        create_button(style=ButtonStyle.red, label="No Thanks!", custom_id="no_thanks")]
    linkbuttons = create_actionrow(*buttons2)
    verify_messages[ctx.author_id] = {}
    verify_messages[ctx.author_id]["mode"] = "new"
    verify_messages[ctx.author_id]["ctx_submitdata"] = ctx
    return embed, linkbuttons


def already_have_your_wallet_and_in_beta(address):
    embed = Embed(
        description=f"You are already in Beta list with this wallet address \n`{address}`.\n"
                    f"**Remove** : Remove yourself from beta list.\n"
                    f"**Change** : Change your wallet address.",
        title="Already Enrolled")
    buttons2 = [create_button(style=ButtonStyle.red, label="Remove", custom_id="remove_from_beta"),
                create_button(style=ButtonStyle.green, label="Change", custom_id="change_wallet")]
    linkbuttons = create_actionrow(*buttons2)

    return embed, linkbuttons
