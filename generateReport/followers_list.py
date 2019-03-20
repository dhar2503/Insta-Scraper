import pandas as pd
import datetime
from definePath import path

path_defined = path.path

followersList = {}

# Function to get the followers of the given user name
def getFollowersList(bot, uName):

    followers_list = bot.get_user_followers(bot.get_user_id_from_username(uName))

    followerCount = len(followers_list)

    followers_list = ",".join(followers_list)

    profile_ID = bot.get_user_id_from_username(uName)

    followersList['username'] = uName

    followersList['profile_ID'] = profile_ID

    followersList['captured_timestamp'] = datetime.datetime.now().timestamp()

    followersList['followers_count'] = followerCount

    followersList['follower_list'] = followers_list

    followerListDF = pd.DataFrame(list(followersList.items()), columns=['Data', 'Value']).set_index('Data').T

    with open('%s'%path_defined+'follower_list.csv', 'w', encoding='utf-8') as f:
        followerListDF.to_csv(f, index=False, header=True)

    return followerCount