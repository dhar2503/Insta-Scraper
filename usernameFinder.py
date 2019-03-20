import pandas as pd
from instabot import Bot
from generateReport import profile_id_look_up
from definePath import path
import os.path
import argparse

path_defined = path.path

user_id_file = '%s'%path_defined+'profile_id_look_up_temp.csv'

if os.path.isfile(user_id_file):
    os.remove(user_id_file)
else:
    None
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p)

uname = input("Enter the User Name:")

user_id = bot.get_user_id_from_username(uname)

profile_id_look_up.getProfileIDLookUP(bot, user_id)

user_name_df = pd.read_csv('%s'%path_defined+'profile_id_look_up_temp.csv',
                             error_bad_lines=False)

user_name_df.columns = ['profile_id', 'username','full_name', 'profile_image_url', 'is_private', 'is_verified']

user_name_df = user_name_df.drop_duplicates()

with open('%s'%path_defined+'profile_id_look_up.csv', 'w', encoding='utf-8') as f:
    user_name_df.to_csv(f, index=False)
