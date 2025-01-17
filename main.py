from dotenv import load_dotenv
from pixivpy3 import AppPixivAPI
from src.tags import aliases, categories

import os
import re
import sys


load_dotenv()

api = AppPixivAPI()
api.set_auth(
    access_token=os.getenv("CLIENT_ACCESS_TOKEN"),
    refresh_token=os.getenv("CLIENT_REFRESH_TOKEN")
)

picpath = sys.argv[1]
picnames = map(
    lambda x: re.sub(r"_p\d\..+", "", x),
    filter(
        lambda s: re.search(r"^\d+_p\d\..+$", s),
        os.listdir(picpath)
    )
)

illusts = map(
    lambda x: (x, api.illust_detail(x)),
    set(picnames)
)

illust_tags = {}

for (picname, illust) in illusts:
    if illust.illust == None:
        illust_tags[picname] = "NULL"
        continue
    
    tags = list(map(
        lambda x: aliases[x] if x in aliases.keys() else x,
        map(
            lambda x: x.name if x.translated_name is None else
            x.translated_name,
            illust.illust.tags
        )
    ))

    category_tags = [t for t in tags if t in categories]
    
    if len(category_tags) != 0:
        illust_tags[illust.illust.id] = category_tags[0]
    else:
        illust_tags[illust.illust.id] = tags[0] if tags else "NULL"

print(illust_tags)
