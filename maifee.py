from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from time import sleep
import json
from typing import List, Dict

# import re


"""
Fields to Scrape: 
 [ ]Posts, 
 [x] Post URL, 
 [x] Post Time, 
 [x] Post Te[x]t, 
 [x] No. of Comments, 
 [x] No. of Retweets, 
 [x] No. of Likes, 
 [ ]Commenter Name, 
 [ ]Commenter profile URL, 
 [ ]Comment time, 
 [ ]Comment, 
 [ ]Who Retweets, 
 [ ]Retweet Te[x]t, 
 [ ]Retweeter URL
"""

base_url = "https://twitter.com/"

driver = webdriver.Chrome()
driver.get(base_url + "bbcbangla")
sleep(3)
count = 0

__PAGE = "//div[@class='css-1dbjc4n r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l']"
__TEXTS = "//div[@class='css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']"
__TIMES_N_URLS = "//div[@class='css-1dbjc4n r-18u37iz r-1q142lx']"
__OPTIONS_REPLIES_RETWEETS_LIKES_SHARES = "//div[@class='css-901oao r-1awozwy r-1bwzh9t r-6koalj r-37j5jr r-a023e6 r-16dba41 r-1h0z5md r-rjixqe r-bcqeeo r-o7ynqc r-clp7b1 r-3s2u2q r-qvutc0']"


class Comment(object):
    def __init__(self) -> None:
        self.commenter_name = ""
        self.commenter_url = ""
        self.comment_time = ""
        self.comment = ""
        self.__COMMENTS = (
            "//div[@class='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu']"
        )

    def parse_time_from_comment__element(self, time__n__url_element: WebElement) -> str:
        return time__n__url_element.find_element(By.TAG_NAME, "time").get_attribute(
            "datetime"
        )

    def parse_comment(self, comment_element: WebElement) -> Comment:
        self.comment_time = self.parse_time_from_comment__element(comment_element)
        return self

    def parse_all_comments(self) -> List[Comment]:
        global __COMMENTS
        comment_elements = driver.find_elements(By.XPATH, self.__COMMENTS)
        comments = []
        for comment_element in comment_elements:
            comment = self.parse_comment(comment_element)
            comments.append(comment)
            print(comment)
            break

        return comments

    def to_dict(self) -> Dict:
        return {
            "commenter_name": self.commenter_name,
            "commenter_url": self.commenter_url,
            "comment_time": self.comment_time,
            "comment": self.comment,
        }

    def __str__(self) -> str:
        return json.dumps(
            self.to_dict(),
            indent=4,
        )


class Tweet(object):
    def __init__(self):
        self.post_text = ""
        self.post_time = ""
        self.post_url = ""
        self.count_reply = 0
        self.count_retweet = 0
        self.count_like = 0
        self.comments = []

    def parse_text_from_text__element(self, text_element: WebElement) -> str:
        return text_element.get_attribute(
            "innerHTML"
        )  # print(re.sub('<[^<]+?>', '', tweets.get_attribute("innerHTML")))

    def parse_time_from_time__n__url_element(
        self, time__n__url_element: WebElement
    ) -> str:
        return time__n__url_element.find_element(By.TAG_NAME, "time").get_attribute(
            "datetime"
        )

    def parse_count__reply_from_reply__element(self, reply_element: WebElement) -> int:
        return reply_element.find_elements(By.TAG_NAME, "span")[2].get_attribute(
            "innerHTML"
        )

    def parse_count__retweet_from_retweet__element(
        self, retweet_element: WebElement
    ) -> int:
        return retweet_element.find_elements(By.TAG_NAME, "span")[2].get_attribute(
            "innerHTML"
        )

    def parse_count__like_from_like__element(self, like_element: WebElement) -> int:
        return like_element.find_elements(By.TAG_NAME, "span")[2].get_attribute(
            "innerHTML"
        )

    def parse_url_from_time__n__url_element(
        self, time__n__url_element: WebElement
    ) -> str:
        return time__n__url_element.find_element(By.TAG_NAME, "a").get_attribute("href")

    def parse_from_elements(self, tweet_elements: List[WebElement]) -> Tweet:
        text_element, time_n_url, option_reply_retweet_like_share = (
            tweet_elements[0],
            tweet_elements[1],
            tweet_elements[2],
        )
        self.post_text = self.parse_text_from_text__element(text_element)

        self.post_time = self.parse_time_from_time__n__url_element(time_n_url)

        self.post_url = self.parse_url_from_time__n__url_element(time_n_url)

        reply_element, retweet_element, like_element = (
            option_reply_retweet_like_share[1],
            option_reply_retweet_like_share[2],
            option_reply_retweet_like_share[3],
        )

        self.count_reply = self.parse_count__reply_from_reply__element(reply_element)
        self.count_retweet = self.parse_count__retweet_from_retweet__element(
            retweet_element
        )
        self.count_like = self.parse_count__like_from_like__element(like_element)
        self.get_comments()
        return self

    def to_dict(self) -> Dict:
        return {
            "post_text": self.post_text,
            "post_time": self.post_time,
            "post_url": self.post_url,
            "count_reply": self.count_reply,
            "count_retweet": self.count_retweet,
            "count_like": self.count_like,
            # "comments": self.comments,
        }

    def __str__(self) -> str:
        return json.dumps(
            self.to_dict(),
            indent=4,
        )

    def _return_to_old_path(self) -> None:
        driver.back()

    def _open_tweet_page(self) -> None:
        driver.get(self.post_url)

    def get_comments(self) -> Tweet:
        self._open_tweet_page()
        sleep(2)
        self.comments = Comment().parse_all_comments()
        self._return_to_old_path()
        return self


tweets = []

while True:
    if count >= 20:  # at least 20
        break
    sleep(2)
    tweets_in_page = driver.find_elements(By.XPATH, __PAGE)
    for scope in tweets_in_page:
        texts = scope.find_elements(
            By.XPATH,
            __TEXTS,
        )
        times_n_urls = scope.find_elements(By.XPATH, __TIMES_N_URLS)
        options_replies_retweets_likes_shares = scope.find_elements(
            By.XPATH, __OPTIONS_REPLIES_RETWEETS_LIKES_SHARES
        )
        magic_number_count = 5
        options_replies_retweets_likes_shares = [
            options_replies_retweets_likes_shares[
                magic_number_count * x : magic_number_count * x + magic_number_count
            ]
            for x in range(
                0, int(len(options_replies_retweets_likes_shares) / magic_number_count)
            )
        ]

        for text, time_n_url, option_reply_retweet_like_share in zip(
            texts, times_n_urls, options_replies_retweets_likes_shares
        ):
            tweet_instance = Tweet().parse_from_elements(
                [text, time_n_url, option_reply_retweet_like_share]
            )
            tweets.append(tweet_instance)
            # print(tweet_instance)
            break

            count += 1
            if count >= 20:  # at least 20
                break

        print("------------")
        break
    break
    count += 1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


# print(tweets)

driver.quit()
