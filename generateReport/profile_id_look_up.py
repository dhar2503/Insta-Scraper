import threading
import pandas as pd
from definePath import path
import re

path_defined = path.path

def getCommentList(bot, post):
    commenters = bot.get_media_commenters_details(post)

    for j in commenters:
        temp = {}
        profile_id = re.findall(r"'pk': (.+?),", str(j))
        username = re.findall(r"'username': '(.+?)',", str(j))
        fullname = re.findall(r"'full_name': '(.+?)',", str(j))
        profilepicurl = re.findall(r"'profile_pic_url': '(.+?)',", str(j))
        isprivate = re.findall(r"'is_private': (.+?),", str(j))
        isverified = re.findall(r"'is_verified': (.+?),", str(j))
        try:
            temp['profileID'] = profile_id[0]
            temp['username'] = username[0]
            temp['fullname'] = fullname[0]
            temp['profilepicurl'] = profilepicurl[0]
            temp['isprivate'] = isprivate[0]
            temp['isverified'] = isverified[0]
        except:
            None
        data = pd.DataFrame(list(temp.items()), columns=['Data', 'Value']).set_index('Data').T

        with open('%s' % path_defined + 'profile_id_look_up_temp.csv', 'a', encoding='utf-8') as f:
            data.to_csv(f, index=False, header=False)


def getLikersList(bot, post):
    likers = bot.get_media_likers(post)

    for j in likers:
        temp = {}
        profile_id = re.findall(r"'pk': (.+?),", str(j))
        username = re.findall(r"'username': '(.+?)',", str(j))
        fullname = re.findall(r"'full_name': '(.+?)',", str(j))
        profilepicurl = re.findall(r"'profile_pic_url': '(.+?)',", str(j))
        isprivate = re.findall(r"'is_private': (.+?),", str(j))
        isverified = re.findall(r"'is_verified': (.+?),", str(j))
        try:
            temp['profileID'] = profile_id[0]
            temp['username'] = username[0]
            temp['fullname'] = fullname[0]
            temp['profilepicurl'] = profilepicurl[0]
            temp['isprivate'] = isprivate[0]
            temp['isverified'] = isverified[0]
        except:
            None
        data = pd.DataFrame(list(temp.items()), columns=['Data', 'Value']).set_index('Data').T

        with open('%s' % path_defined + 'profile_id_look_up_temp.csv', 'a', encoding='utf-8') as f:
            data.to_csv(f, index=False, header=False)

def getProfileIDLookUP(bot, user_id):

    followers = bot.get_user_followers_details(user_id)

    for j in followers:
        temp = {}
        profile_id = re.findall(r"'pk': (.+?),",str(j))
        username = re.findall(r"'username': '(.+?)',", str(j))
        fullname = re.findall(r"'full_name': '(.+?)',", str(j))
        profilepicurl = re.findall(r"'profile_pic_url': '(.+?)',", str(j))
        isprivate = re.findall(r"'is_private': (.+?),", str(j))
        isverified = re.findall(r"'is_verified': (.+?),", str(j))
        try:
            temp['profileID'] = profile_id[0]
            temp['username'] = username[0]
            temp['fullname'] = fullname[0]
            temp['profilepicurl'] = profilepicurl[0]
            temp['isprivate'] = isprivate[0]
            temp['isverified'] = isverified[0]
        except:
            None
        data = pd.DataFrame(list(temp.items()), columns=['Data', 'Value']).set_index('Data').T

        with open('%s'%path_defined+'profile_id_look_up_temp.csv', 'a', encoding='utf-8') as f:
            data.to_csv(f, index=False, header=False)

    following = bot.get_user_following_details(user_id)

    for j in following:
        temp = {}
        profile_id = re.findall(r"'pk': (.+?),",str(j))
        username = re.findall(r"'username': '(.+?)',", str(j))
        fullname = re.findall(r"'full_name': '(.+?)',", str(j))
        profilepicurl = re.findall(r"'profile_pic_url': '(.+?)',", str(j))
        isprivate = re.findall(r"'is_private': (.+?),", str(j))
        isverified = re.findall(r"'is_verified': (.+?),", str(j))
        try:
            temp['profileID'] = profile_id[0]
            temp['username'] = username[0]
            temp['fullname'] = fullname[0]
            temp['profilepicurl'] = profilepicurl[0]
            temp['isprivate'] = isprivate[0]
            temp['isverified'] = isverified[0]
        except:
            None
        data = pd.DataFrame(list(temp.items()), columns=['Data', 'Value']).set_index('Data').T

        with open('%s'%path_defined+'profile_id_look_up_temp.csv', 'a', encoding='utf-8') as f:
            data.to_csv(f, index=False, header=False)

    posts = bot.get_total_user_medias('wanderasinc')

    threads_comments = [threading.Thread(target=getCommentList, args=(bot, post, )) for post in
                     posts]

    for thread in threads_comments:
        thread.start()
    for thread in threads_comments:
        thread.join()

    threads_likers = [threading.Thread(target=getLikersList, args=(bot, post, )) for post in
                     posts]

    for thread in threads_likers:
        thread.start()
    for thread in threads_likers:
        thread.join()