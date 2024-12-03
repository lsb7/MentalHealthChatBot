# -*- coding: utf-8 -*-
"""web_scraper.py

This code parses through a list of given subreddits, takes the first 5 comments that go over a 500 character threshold, and outputs it into a text file

"""

import requests
import re

def parse(subreddit, after=''):
    url_template = 'https://old.reddit.com/r/{}/top.json?t=all{}'
    headers = {'User-Agent': 'XDD'}
    params = f'&after={after}' if after else ''
    url = url_template.format(subreddit, params)
    response = requests.get(url, headers=headers)
    post_ids_list = []

    if response.ok:
        data = response.json()['data']
        # print(f"len of number of posts is {len(data)}")
        for post in data['children']:
            pdata = post['data']
            post_id = pdata['id']
            post = re.sub(r'\s+', ' ', pdata['selftext'])
            author = pdata['author']
            
            post_ids_list.append((post_id, post, author))           
        return post_ids_list
    else:
        print(f'Error {response.status_code}')
        return None

def fetch_comments(url, headers, depth=1, author=None, num_comments=5):
    url += f'?depth={depth}'
    response = requests.get(url, headers=headers)

    if response.ok:
        data = response.json()[1]['data']
        comments = []


        for i in range(len(data['children'])):
            post = data['children'][i]
            pdata = post['data']
            if pdata.get('body') and pdata['body'] not in ['[removed]', '[deleted]'] and author != pdata["author"] and len(pdata['body']) > 500:
                comment = re.sub(r'\s+', ' ', pdata['body'])
                comments.append(comment)
            if i == len(data['children']) or len(comments) == num_comments:
                return comments
    
    else:
        print(f'Error {response.status_code}')
        return []
    
def save_to_file(text, file1, file2, file3):
    instruction = '<s> [INST] <<SYS>> You are a helpful and joyous mental therapy assistant. Always answer as helpfully and cheerfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don\'t know the answer to a question, please don\'t share false information. <</SYS>> '
    for post, comment in text:
        with open(file1, "a") as file:
            file.write(instruction + post + ' [/INST] ' + comment + ' </s>\n')
        with open(file2, "a") as file:
            file.write(post + "\n")
        with open(file3, "a") as file:
            file.write(comment + "\n")

def main():
    subreddits = ['offmychest','advice','mentalhealth','confessions', 'self', 'AITAH', 'AmItheAsshole', 'depression', 'anxiety', 'relationships', 'family']

    text = []
    num_comments = 15
    for subreddit in subreddits:

        post_ids = parse(subreddit)
        ##### Post_ids in format (post_id, post, author)
        print(f"There are {len(post_ids)} posts for subreddit r/{subreddit}, each will have {num_comments} comments")

        url = 'https://www.reddit.com/'

        for i in range(len(post_ids)):
            url_mod = url + post_ids[i][0] + '/.json'
            headers = {'User-Agent': 'test'}
            all_comments = fetch_comments(url=url_mod, headers=headers, depth=1, author=post_ids[i][2], num_comments=num_comments)
            # print(f"len of all coments is {len(all_comments)}")
            if all_comments:
                for comment in all_comments:
                    text.append((post_ids[i][1], comment))

    print(len(text))

    save_to_file(text, "Llama2_reddit_post.txt", "BlenderBot_posts.txt", "BlenderBot_comments.txt")

if __name__ == '__main__':
    main()
