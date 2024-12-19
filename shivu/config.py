class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6977793872"
    sudo_users = "7053677913", "6977793872"
    GROUP_ID = -1002143253592
    TOKEN = "7714215608:AAG3f6YdhsM3NTzskUhoPDy3xu4LFCw7EuE"
    mongo_url = "mongodb+srv://HaremDBBot:ThisIsPasswordForHaremDB@haremdb.swzjngj.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "The2B2T"
    UPDATE_CHAT = "The2B2T"
    BOT_USERNAME = "CricketGrabberBot"
    CHARA_CHANNEL_ID = "-1002384039597"
    api_id = 28735016
    api_hash = "395761ed41e18de91ee4e18ff99afc81"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
