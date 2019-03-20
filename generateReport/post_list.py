import pandas as pd
import re
import datetime
from definePath import path

path_defined = path.path

# Function to scrape the post details of the given user name
def getPostList(bot,post,followers_count):

    try:

        details = bot.get_media_info(post)[0]

        keys_there=details.keys()

        temp = {}

        if "caption" in keys_there:
            if details['caption'] is not None:
                temp['postID'] = details['caption']['pk']
            else:
                temp['postID'] = "None"
        else:
            temp['postID'] = "None"

        if details['user'] is not None:
            temp['profileID'] = details['user']['pk']
            temp['username'] = details['user']['username']
        else:
            temp['profileID'] = "None"
            temp['username'] = "None"

        if details['code'] is not None:
            temp['shortcode'] = details['code']
            temp['display_url'] = 'https://www.instagram.com/p/%s'%str(temp['shortcode'])
        else:
            temp['shortcode'] = "None"
            temp['display_url'] = "None"

        if "caption" in keys_there:
            if details['caption'] is not None:
                temp['caption']=details['caption']['text']
        else:
            temp['caption'] = "None"

        if details['comment_count'] is not None:
            temp['comment_count']=int(details['comment_count'])
        else:
            temp['comment_count']=0

        if details['like_count'] is not None:
            temp['like_count']=int(details['like_count'])
        else:
            temp['like_count']=0

        if temp['comment_count'] & temp['like_count'] != "0":
            temp['engagement'] = ((int(temp['like_count']) + int(temp['comment_count'])) / int(followers_count)) * 100
        else:
            temp['engagement'] = 0

        if "caption" in keys_there:
            if details['caption'] is not None:
                comments = bot.get_media_comments(post)
                comment_list = []
                for j in comments:
                    t = {}
                    t['comment'] = j['text']
                    comment_list.append(t)
                hashtag_comment = re.findall(r"#(\w+)", str(comment_list))
                description = details['caption']['text']
                hashtag_post = re.findall(r"#(\w+)", description)
                hashtags = hashtag_comment+hashtag_post
                temp['hashtags'] = hashtags
            else:
                temp['hashtags'] = "None"
        else:
            temp['hashtags'] = "None"

        temp['hashtags'] = ",".join(temp['hashtags'])

        if details['media_type'] is not None:
            if details['media_type']==2:
                temp['_is_Video']="true"
            else:
                temp['_is_Video']="false"
        else:
             temp['_is_Video']="None"

        temp['_is_Video'].lower()

        if "carousel_media_count" in keys_there:
            pics_count=int(details['carousel_media_count'])
            if pics_count>0:
                images=[]
                for m in range(0,pics_count):
                    images.append(details['carousel_media'][m]['image_versions2']['candidates'][0]['url'])
                temp['is_carousel']="true"
        else:
            temp['is_carousel']="false"

        temp['is_carousel'].lower()

        if details['caption'] is not None:
            temp['time_posted'] = details['caption']['created_at']
        else:
            temp['time_posted'] = "None"

        if "view_count" in keys_there:
            temp['view_count']=details['view_count']
        else:
            temp['view_count']= ''

        if "caption" in keys_there:
            if details['caption'] is not None:
                mentions = details['caption']['text']
                mentions = re.findall(r"@(\w+)", str(mentions))
                temp['mentions'] = ",".join(mentions)
            else:
                temp['mentions'] = ''
        else:
            temp['mentions'] = ''

        if "usertags" in keys_there:

            if details['usertags'] is not None:

                usertags = re.findall(r"'username': '\w+'", str(details['usertags']['in']))

                usertags = re.findall(r": '\w+'", str(usertags))

                usertags = re.findall(r"\w+", str(usertags))

                usertags = ",".join(usertags)

                temp['tagged_users'] = usertags
            else:
                temp['tagged_users'] = ''
        else:
            temp['tagged_users'] = ''

        if "location" in keys_there:
            if details['location'] is not None:
                temp['location_name'] = details['location']['name']
                temp['location_id'] = details['location']['pk']
            else:
                temp['location_name'] = ''
                temp['location_id'] = ''
        else:
            temp['location_name'] = ''
            temp['location_id'] = ''

        likers_list = bot.get_media_likers(post)

        temp['likers_list'] = re.findall(r"'pk': (.+?),", str(likers_list))

        temp['likers_list'] = ",".join(temp['likers_list'])

        temp['captured_timestamp'] = datetime.datetime.now().timestamp()

        data = pd.DataFrame(list(temp.items()), columns=['Data', 'Value']).set_index('Data').T

        if data['postID'].values[0] == 'None':
            None
        else:
            with open('%s'%path_defined+'media_info.csv', 'a', encoding='utf-8') as f:
                data.to_csv(f, index=False, header=False)

    except:
        None