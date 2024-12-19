class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6977793872"
    sudo_users = "7053677913", "1732582235"
    GROUP_ID = -1002437903458
    TOKEN = "7308335879:AAHTi3IjB6OcOtxsutJfAEdnfCuMnis5X6Y"
    mongo_url = "mongodb+srv://HaremDBBot:ThisIsPasswordForHaremDB@haremdb.swzjngj.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "https://t.me/GetCricketPlayers"
    UPDATE_CHAT = "https://t.me/GetCricketPlayers"
    BOT_USERNAME = "Get_Cricket_Players_Bot"
    CHARA_CHANNEL_ID = "-1002437903458"
    api_id = 28735016
    api_hash = "395761ed41e18de91ee4e18ff99afc81"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
