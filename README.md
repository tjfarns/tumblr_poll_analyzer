# Tumblr Poll Analyzer
Fetches the results from polls and outputs them into a .csv data file. 

## Requirements
This script requires OAuth credentials for tumblr's API, as provided through [tumblr's API Console](https://www.tumblr.com/oauth/apps). You will then need to store these in a file named "client_info.json" (template provided in repo). You will also need to add the blog_name for the blog you're trying to analyze.

This repo uses the following libraries: 
```
pip install pytumblr2
pip install jsonpickle
```

