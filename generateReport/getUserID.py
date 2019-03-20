import pandas as pd
from definePath import path

path_defined = path.path

# Function to get the user id of all the followers, likers, followings & commenters of the given user name
def saveUserList():

    comment_df = pd.read_csv('%s'%path_defined+'comment_list.csv', error_bad_lines=False)

    likers_df = pd.read_csv('%s'%path_defined+'likers_list.csv', error_bad_lines=False)

    followers_df = pd.read_csv('%s'%path_defined+'follower_list.csv', error_bad_lines=False)

    following_df = pd.read_csv('%s'%path_defined+'following_list.csv', error_bad_lines=False)

    commneter_user_id_list = list(comment_df['profile_id'])

    follower_user_id = followers_df['follower_list']

    follower_user_id = follower_user_id[0].split(',')

    follower_user_id_list = []

    for follwers in range(len(follower_user_id)):

        follower_user_id_list.append(follower_user_id[follwers])

    following_user_id = following_df['following_list']

    following_user_id = following_user_id[0].split(',')

    following_user_id_list = []

    for following in range(len(following_user_id)):

        following_user_id_list.append(following_user_id[following])

    likers_user_id_list = []

    for i in range(len(likers_df)):

        if isinstance(likers_df['likers_list'][i],float):
            None
        else:
            likers_user_id = likers_df['likers_list'][i].split(',')
            for liker in range(len(likers_user_id)):
                likers_user_id_list.append(likers_user_id[liker])

    user_id = likers_user_id_list+follower_user_id_list+following_user_id_list+commneter_user_id_list
    final_user_id = list(set(user_id))
    final_user_id_df = pd.DataFrame(final_user_id, columns=['user_id'])

    with open('%s' % path_defined + 'user_id_list.csv', 'w', encoding='utf-8') as f:
        final_user_id_df.to_csv(f, index=False, header=True)