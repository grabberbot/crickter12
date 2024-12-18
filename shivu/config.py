class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6977793872"
    sudo_users = "7053677913", "6977793872"
    GROUP_ID = -1002143253592
    TOKEN = "7714215608:AAFB0VovsvLpMmMXIvE6NGUbCABJnAFQYk4"
    mongo_url = "mongodb+srv://kalawativerma80:s?QF7Yx3NUE9u!6@finepixel.afi4pra.mongodb.net/?retryWrites=true&w=majority&appName=finepixel"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "The2B2T"
    UPDATE_CHAT = "The2B2T"
    BOT_USERNAME = "CricketGrabberBot"
    CHARA_CHANNEL_ID = "-1002384039597"
    api_id = 26626068
    api_hash = "bf423698bcbe33cfd58b11c78c42caa2"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
