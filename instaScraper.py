import argparse
import threading
import pandas as pd
import numpy as np
from instabot import Bot
import os.path
from generateReport import followers_list
from generateReport import following_list
from generateReport import post_list
from generateReport import comment_list
from definePath import path
from generateReport import getUserID
from time import sleep

# To get the username and password from the user
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('--u', type=str, help="username")
parser.add_argument('--p', type=str, help="password")
args = parser.parse_args()

# Initialize the Instagram bot
bot = Bot()
bot.login(username=args.u, password=args.p)

# Get the user name to scrape the data
uname = input("Enter the User Name:")
users = ['%s'%uname]
path_defined = path.path

# Function to clean the scraped post data and create report with necessary attributes of the post details for the given username
def create_post_report():

    insta_df = pd.read_csv('%s'%path_defined+'media_info.csv', error_bad_lines=False)

    post_id = insta_df.iloc[:, 0]

    for i in range(len(post_id)):
        if post_id[i].isdigit():
            None
        else:
            insta_df = insta_df[insta_df.iloc[:, 0] != post_id[i]]

    insta_df.columns = ['post_id', 'profile_id', 'username', 'shortcode', 'display_url',
                        'caption', 'comment_count', 'like_count', 'engagement', 'hashtags', 'is_video', 'is_carousel',
                        'posted_timestamp',
                        'view_count', 'mentions', 'tagged_users', 'location_name', 'location_id', 'likers_list',
                        'captured_timestamp']

    post_list_df = insta_df[['post_id', 'profile_id', 'username', 'shortcode', 'posted_timestamp', 'display_url',
                             'caption', 'like_count', 'comment_count', 'engagement', 'hashtags', 'mentions',
                             'tagged_users', 'is_video', 'is_carousel',
                             'view_count', 'location_name', 'location_id']]

    with open('%s'%path_defined+'post_list.csv', 'w', encoding='utf-8') as f:
        post_list_df.to_csv(f, index=False)

# Function to create report about the likers list for the given user name
def create_likers_report():

    insta_df = pd.read_csv('%s'%path_defined+'media_info.csv', error_bad_lines=False)

    post_id = insta_df.iloc[:, 0]

    for i in range(len(post_id)):
        if post_id[i].isdigit():
            None
        else:
            insta_df = insta_df[insta_df.iloc[:, 0] != post_id[i]]

    insta_df.columns = ['post_id', 'profile_id', 'username', 'shortcode', 'display_url',
                        'caption', 'comment_count', 'like_count', 'engagement', 'hashtags', 'is_video', 'is_carousel',
                        'posted_timestamp',
                        'view_count', 'mentions', 'tagged_users', 'location_name', 'location_id', 'likers_list',
                        'captured_timestamp']

    likers_list_df = insta_df[['post_id', 'shortcode','profile_id', 'username', 'captured_timestamp', 'like_count', 'likers_list']]

    with open('%s'%path_defined+'likers_list.csv', 'w', encoding='utf-8') as f:
        likers_list_df.to_csv(f, index=False)

# Function to create report about the commenters for the given user name
def create_comment_report():

    comment_df = pd.read_csv('%s'%path_defined+'comment_list_temp.csv',
                             error_bad_lines=False)

    post_id = comment_df.iloc[:, 0]

    for i in range(len(post_id)):
        if isinstance(post_id[i], float):
            None
        else:
            if post_id[i].isdigit() or post_id[i] == '':
                None
            else:
                comment_df = comment_df[comment_df.iloc[:, 0] != post_id[i]]

    comment_df.columns = ['post_id', 'shortcode', 'comment_id', 'profile_id', 'username',
                          'posted_timestamp', 'comment_text', 'comment_like_count', 'post_owner_profile_id',
                          'post_owner_username']

    comment_df['post_id'].replace('', np.nan, inplace=True)

    comment_df.dropna(subset=['post_id'], inplace=True)

    with open('%s'%path_defined+'comment_list.csv', 'w', encoding='utf-8') as f:
        comment_df.to_csv(f, index=False)

# Function to remove the temp files, If any present
def removeFiles():

    media_file = '%s'%path_defined+'media_info.csv'

    comment_file = '%s'%path_defined+'comment_list_temp.csv'

    if os.path.isfile(media_file):
        os.remove(media_file)
    else:
        None

    if os.path.isfile(comment_file):
        os.remove(comment_file)
    else:
        None

removeFiles()

for username in users:

    # Function to get the follower list report of the given user name
    try:
        follower_count = followers_list.getFollowersList(bot, username)
    except:
        None
    sleep(5)

    # Function to get the following list report of the given user name
    try:
        following_list.getFollowingList(bot, username)
    except:
        None
    sleep(5)
    posts = bot.get_total_user_medias(username)

    # Function to get the post data of the given user name
    threads_posts = [threading.Thread(target=post_list.getPostList, args=(bot, post, follower_count,)) for post in posts]
    for thread in threads_posts:
        thread.start()
    for thread in threads_posts:
        thread.join()

    # Function to get the comments data of the given user name
    threads_comments = [threading.Thread(target=comment_list.getCommentList, args=(bot, post, username,)) for post in posts]
    for thread in threads_comments:
        thread.start()
    for thread in threads_comments:
        thread.join()

try:
    create_post_report()
except:
    None
sleep(5)
try:
    create_likers_report()
except:
    None
sleep(5)
try:
    create_comment_report()
except:
    None
sleep(5)
try:
    getUserID.saveUserList()
except:
    None
sleep(5)