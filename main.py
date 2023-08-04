import string
from pprint import pprint

import pytumblr
import sys

print(sys.argv)

if (sys.argv.len >= 3):
    blogName = sys.argv.at(1)
    optionName = sys.argv.at(2);

client = pytumblr.TumblrRestClient(
    '<consumer_key>',
    '<consumer_secret>',
    '<oauth_token>',
    '<oauth_secret>',
)

client.posts(blogName, tags=[optionName]) # get posts for a blog

# do some analytics with the data I fetch (e.g. count up
# cumulative votes for a specific option)
