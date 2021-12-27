import json
import random
import re

###############################################################
## CONSTANTS
###############################################################

# try out with a dummy file or with the actual thing
FILENAME = 'dummy.txt'
FILENAME = 'twi860.txt'

# Constant values for avatars
USER_AVATAR = {
    "Anonymous Spellcaster A": "https://twifanart.shelter.moe/_images/84c3ac29328c127cb77aa815de5cef27/",
    "Belavierr": "https://twifanart.shelter.moe/_images/d036889c6c7d7822f4f504e8f8d71fc7/",
    "Eldavin": "https://twifanart.shelter.moe/_images/32c32fe557c5a58b7ce6ec5a8dca6c4e/",
    "Fetohep": "https://twifanart.shelter.moe/_images/64f8c1f4fce11c8efbbfb3dbbf5c17db/",
    "Geneva": "https://twifanart.shelter.moe/_images/77a32074005ab64aba533ca79eab690a/",
    "Ice Squirrel": "https://twifanart.shelter.moe/_images/9bb5a9cbef2100aac45403f8a65aa9da/",
    "Joseph Ortega": "https://twifanart.shelter.moe/_images/9745e6d3127bdf747e4c9b8cbc0a3967/",
    "Lionette": "https://twifanart.shelter.moe/_images/dca74c85b5ff66905b181e8a36ae64ca/",
    "Magus G": "https://twifanart.shelter.moe/_images/9ab8bd7751f02f3da4b75a8b50416045/",
    "Mons": "https://twifanart.shelter.moe/_images/9ed343644ea0e255214dd265ba5f464a/",
    "Mri": "https://twifanart.shelter.moe/_images/e2d726c90cd9908bcf6d042c728df49b/",
    "RainyEarl": "https://twifanart.shelter.moe/_images/a6c0ced0b75f6e871e24f4e4c9b02199/",
    "Rhis": "https://twifanart.shelter.moe/_images/4c88bda9af1c955707538488e8a91b48/",
    "Saliss": "https://twifanart.shelter.moe/_images/3c69e220ee2609efd5bd3b4c81126a10/",
    "Tallman": "https://twifanart.shelter.moe/_images/1594286f701d2086b80fff83c63e753c/",
    "True Grit": "https://twifanart.shelter.moe/_images/0d8169da2c0d8d6d8848bb972706a0ea/",
    "Viscount V": "https://twifanart.shelter.moe/_images/9b64e45389429a09892111951ab55658/",
    "Wall Lord Ilvriss": "https://twifanart.shelter.moe/_images/57876dab4e8864df970e0fca5ea1cc17/",
    "Windy Girl": "https://twifanart.shelter.moe/_images/fc0d1224d4967909ecf2d043190d6c53/",
    "Witch A": "https://twifanart.shelter.moe/_images/dfa0686baf6f5e78f449fe217713c454/",
    "YlawesB": "https://twifanart.shelter.moe/_images/9c97116d758d356b18395d96b0b32aec/",
    "Yvlon": "https://twifanart.shelter.moe/_images/4355d45ca829b9e0cf994a62c6944690/",
}

ROLES = {
    11: {"id": 11, "name": "pirateaba", "color": "rgb(141, 53, 41)", "isSeparated": True},
    12: {"id": 12, "name": "Moderators", "color": "rgb(250, 215, 73)", "isSeparated": True},
}

USER_ROLES = {
    "pirateaba": [11],
    "Grand Magus Eldavin": [12],
    "Eldavin": [12],
}

# I'm too lazy to fix the actual code
IGNORED_USERNAME = [
    "The Necromancer barely paid attention to the undead after his harrowing battle with magic that threatened even him. He was also checking in on Pisces, so he did what he had done for a century in life",
    "“Here’s a tip from the Titan of Baleros",
]

###############################################################
## PREPROCESSING STUFF
###############################################################

def get_user_maps(splitted):
    user_set = set()
    username_map = dict()
    userid_map = dict()
    for user, val in splitted:
        user_set.add(user.strip())

    for ignore in IGNORED_USERNAME:
        user_set.remove(ignore)

    # Need something for pirateaba
    username_map["pirateaba"] = 1
    userid_map[1] = "pirateaba"

    # start at 2 because idx=1 is pirateaba
    for userid, username in enumerate(user_set, start=2):
        username_map[username] = userid
        userid_map[userid] = username

    return (username_map, userid_map)

def get_user_json(username, userid):
    # dummy account, who is viewing the discord
    PIRATEABA = {
        "id": 1,
        "username": "pirateaba",
        "tag": 1877,
        "avatar": "https://2.gravatar.com/avatar/2f8ac70cd17f11c419846c441769523b?s=136&d=identicon&r=PG",
        "activity": {
            "type": "writing",
            "name": "The Wandering Inn",
            "duration": "for 2 hours",
        },
    }

    if username == "pirateaba":
        return PIRATEABA

    return {
        "id": userid,
        "username": username,
        "tag": random.randrange(1000, 9999),
        "avatar": USER_AVATAR.get(username, "discordblue.png"),
    }

def get_all_users_json(username_map):
    return {userid: get_user_json(username, userid) for username, userid in username_map.items()}

def get_members_list(username_map):
    return [{"userId": userid, "roles": USER_ROLES.get(username, [])} for username, userid in username_map.items()]

next_msg_idx = 900
def get_single_msg(username, msg, username_map):
    global next_msg_idx
    username = username.strip()
    msg_idx = next_msg_idx
    next_msg_idx += 1
    return {
        "id": msg_idx,
        "userId": username_map[username],
        "content": msg.strip(),
        "time": 'Today at 5:17 PM'
    }

def get_all_messages(splitted, username_map):
    return [get_single_msg(username, msg, username_map) for username, msg in splitted if username not in IGNORED_USERNAME]
    

def overall_json(splitted, username_map):
    return {
        "userId": 1,
        "friendsOnlineCount": 0,
        "directMessages": [
            # because this project doesn't work with empty array
            {
              "id": 333,
              "userId": 2,
              "messages": [get_single_msg("Witch A", "Please don’t kill me :<", username_map)]
            }
        ],
        "users": get_all_users_json(username_map),
        "guilds": [
            {
                "id": 1111,
                "name": "WistramChat",
                "initials": "WNN",
                "icon": "https://twifanart.shelter.moe/_images/56c234dfd5b0f7457bf2a24edb414611/",
                "welcomeChannelId": 111124,
                "categories": [
                    {
                        "id": 11112,
                        "name": "general",
                        "channels": [
                            {
                                "id": 111124,
                                "name": "general",
                                "messages": get_all_messages(splitted, username_map)
                            },
                        ]
                    }
                ],
                "roles": ROLES,
                "members": get_members_list(username_map),
            }
        ],
    }


###############################################################
## ACTUAL SCRIPT
###############################################################

with open(FILENAME) as f:
    lines = f.readlines()
    # Remove all lines that aren't chat
    filtered = filter(lambda line: ":" in line, lines)
    # split into username, text
    splitted = map(lambda line: line.split(":", 1), filtered)
    splitted = list(splitted)
    IGNORED_USERNAME += [username for username, msg in splitted if not len(msg.strip())]
    # first pass - get user list
    username_map, userid_map = get_user_maps(splitted)
    json_content = json.dumps(overall_json(splitted, username_map), sort_keys=True, indent=4)
    final_js_file = "export default " + json.dumps(overall_json(splitted, username_map), indent=4)
    # wtf this stupid library converts int keys to str 
    # not a bug my ass https://bugs.python.org/issue34972
    final_js_file = re.sub("\"(\d+)\"", "\\1", final_js_file)
    with open('./data.js', 'w') as filetowrite:
        filetowrite.write(final_js_file)


