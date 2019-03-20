import pandas as pd
import datetime
from definePath import path

path_defined = path.path

followingList = {}

# Function to get the followings of the given user name
def getFollowingList(bot, uName):

    profile_ID = bot.get_user_id_from_username(uName)

    following_list = bot.get_user_following(bot.get_user_id_from_username(uName))

    followingCount = len(following_list)

    following_list = ",".join(following_list)

    followingList['username'] = uName

    followingList['profile_ID'] = profile_ID

    followingList['captured_timestamp'] = datetime.datetime.now().timestamp()

    followingList['following_count'] = followingCount

    followingList['following_list'] = following_list

    followingListDF = pd.DataFrame(list(followingList.items()), columns=['Data', 'Value']).set_index('Data').T

    with open('%s'%path_defined+'following_list.csv', 'w', encoding='utf-8') as f:
        followingListDF.to_csv(f, index=False, header=True)