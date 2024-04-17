import csv
import pytumblr2
import jsonpickle
import requests
import json
from os.path import dirname, join


def add_headers(writer, max_num_results):
    headers = ["Poll Question"]
    for i in range(max_num_results):
        headers.append("Choice " + str(i + 1))
        headers.append("Results for Choice " + str(i + 1))
    writer.writerow(headers)


current_dir = dirname(__file__)
file_path = join(current_dir, "./client_info.json")
with open(file_path, 'r') as f:
    client_info = json.load(f)

BLOG_NAME = client_info["blog_name"]

# Authorize through Pytumblr2 using OAuth credentials
client = pytumblr2.TumblrRestClient(
    client_info["consumer_key"],
    client_info["consumer_secret"],
    client_info["oauth_token"],
    client_info["oauth_token_secret"],
)

# make a request for the blog's posts
response = client.posts(BLOG_NAME, limit=999)

# go through each post
max_num_results = 0
all_poll_data = []
for post in response.get("posts"):
    post_id = post["id"]
    for content in post["content"]:
        # grab each poll and extract data
        if content["type"] == "poll":
            poll_client_id = content["client_id"]
            poll_question = content["question"]
            poll_answers_map = {}
            num_results = len(content["answers"])
            if num_results > max_num_results:
                max_num_results = num_results
            for answer in content["answers"]:
                poll_answers_map[answer["client_id"]] = answer["answer_text"]
            votes_response = requests.get(
                f"https://www.tumblr.com/api/v2/polls/{BLOG_NAME}/{post_id}/{poll_client_id}/results"
            ).content
            vote_results = jsonpickle.decode(votes_response)["response"]["results"]
            vote_results_mapped = {}
            for key in vote_results:
                vote_results_mapped[poll_answers_map[key]] = vote_results[key]
            formatted_data = [poll_question]
            for poll_choice in vote_results_mapped:
                formatted_data.append(poll_choice)
                formatted_data.append(vote_results_mapped[poll_choice])
            all_poll_data.append(formatted_data)

# Open and write to the CSV file
data_file_path = join(current_dir, "./data.csv")
with open(data_file_path, "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    add_headers(writer, max_num_results)
    writer.writerows(all_poll_data)
    file.close()
