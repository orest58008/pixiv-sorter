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
picfiles = list(filter(
    lambda s: re.search(r"^\d+_p\d\..+$", s),
    os.listdir(picpath)
))

illusts = map(
    lambda x: (x, api.illust_detail(x)),
    set(map(lambda x: re.sub(r"_p\d\..+", "", x), picfiles))
)

for (picname, illust) in illusts:
    if illust.illust == None:
        if illust.error and not illust.error.user_message == "Page not found":
            raise BaseException(illust.error)
        category = "NULL"
    else:
        tags = list(map(
            lambda x: aliases[x] if x in aliases.keys() else x,
            map(
                lambda x: "" if x.translated_name is None else
                x.translated_name,
                illust.illust.tags
            )
        ))

        category_tags = [t for t in categories if t in tags]
        if len(category_tags) != 0:
            category = category_tags[0]
        else:
            category = tags[0] if tags else "NULL"
        
    category_path = os.path.join(picpath, category.replace('/', '_'))
    if not os.path.exists(category_path):
        os.mkdir(category_path)
        print(category_path)

    illust_files = filter(lambda x: x.find(picname) != -1, picfiles)
    for f in illust_files:
        os.rename(
            os.path.join(picpath, f),
            os.path.join(category_path, f)
        )
