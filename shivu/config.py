class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6977793872"
    sudo_users = "6845325416", "6765826972"
    GROUP_ID = -1002133191051
    TOKEN = "7714215608:AAHGp9x86-wvlTityW8k6vfa1sLE_-6PIhI"
    mongo_url = "mongodb+srv://HaremDBBot:ThisIsPasswordForHaremDB@haremdb.swzjngj.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "Collect_em_support"
    UPDATE_CHAT = "Collect_em_support"
    BOT_USERNAME = "CricketGrabberBot"
    CHARA_CHANNEL_ID = "-1002133191051"
    api_id = 28735016
    api_hash = "395761ed41e18de91ee4e18ff99afc81"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
