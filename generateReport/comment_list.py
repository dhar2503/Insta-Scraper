import pandas as pd
from definePath import path

path_defined = path.path

# Function to scrape the comments from all the posts of the given user name
def getCommentList(bot, post, uName):

    details = bot.get_media_info(post)[0]

    comments = bot.get_media_comments(post)

    for j in comments:

        temp = {}

        try:
            temp['postID'] = details['caption']['pk']
        except:
            temp['postID'] = "None"
        try:
            temp['shortcode'] = details['code']
        except:
            temp['shortcode'] = ''
        try:
            temp['comment_id'] = j['pk']
        except:
            temp['comment_id'] = ''
        try:
            temp['profileID'] = j['user']['pk']
        except:
            temp['profileID'] = ''
        try:
            temp['username'] = j['user']['username']
        except:
            temp['username'] = ''
        try:
            temp['posted_timestamp'] = details['caption']['created_at']
        except:
            temp['posted_timestamp'] = ''
        try:
            temp['comment_text'] = j['text']
        except:
            temp['comment_text'] = ''
        try:
            temp['comment_like'] = j['comment_like_count']
        except:
            temp['comment_like'] = ''
        try:
            temp['post_owner_profile_id'] = details['user']['pk']
        except:
            temp['post_owner_profile_id'] = ''
        try:
            temp['post_owner_username'] = uName
        except:
            temp['post_owner_username'] = ''


        data = pd.DataFrame(list(temp.items()), columns=['Data', 'Value']).set_index('Data').T

        try:

            if data['postID'].values[0] == 'None':
                None
            else:
                with open('%s'%path_defined+'comment_list_temp.csv', 'a', encoding='utf-8') as f:
                    data.to_csv(f, index=False, header=False)
        except:
            None