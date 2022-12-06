from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from time import sleep
import json
from typing import List, Dict, Tuple
import re


"""
Fields to Scrape: 
 [x] Posts, 
 [x] Post URL, 
 [x] Post Time, 
 [x] Post Text, 
 [x] No. of Comments, 
 [x] No. of Retweets, 
 [x] No. of Likes, 
 [x] Commenter Name, 
 [x] Commenter profile URL, 
 [x] Comment time, 
 [x] Comment, 
 [.] Who Retweets, 
 [ ] Retweet Text, 
 [.] Re-Tweeter URL
"""

"""
Show additional replies, including those that may contain offensive content
"""

base_url = "https://twitter.com/"

driver = webdriver.Chrome()
driver.get(base_url + "bbcbangla")
sleep(3)


class ContentUtil(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def strip_image(str_in: str) -> str:
        return re.sub('<img alt=\\"*(.)\\"[^>]*>', "\g<1>", str_in)

    @staticmethod
    def strip_html(str_in: str) -> str:
        return re.sub("<[^<]+?>", "", str_in)

    @staticmethod
    def strip_all(str_in: str) -> str:
        return ContentUtil.strip_html(ContentUtil.strip_image(str_in))


class ReTweet(object):
    def __init__(self) -> None:
        self.retweeter: str = ""
        self.retweeter_url: str = ""
        self.__RETWEET = "//a[@class='css-4rbku5 css-18t94o4 css-901oao r-1nao33i r-1loqt21 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']"

    def parse_all_retweet(self) -> List[ReTweet]:
        # retweet_link = driver.find_element(By.XPATH, self.__RETWEET)
        # retweet_link.click()
        # # todo: i can't get past login
        # sleep(4)
        return []

    def to_dict(self) -> Dict:
        return {
            "retweeter": self.retweeter,
            "retweeter_url": self.retweeter_url,
        }

    def __str__(self) -> str:
        return json.dumps(
            self.to_dict(),
            indent=4,
        )

    def __repr__(self) -> str:
        return self.__str__()


class Comment(object):
    def __init__(self) -> None:
        self.commenter_name: str = ""
        self.commenter_url: str = ""
        self.comment_time: str = ""
        self.comment: str = ""
        self.__USERNAME = "//span[@class='css-901oao css-16my406 css-1hf3ou5 r-poiln3 r-bcqeeo r-qvutc0']"
        self.__USER_PROFILE = "//a[@class='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l']"
        self.__TIME_AND_URL = "//div[@class='css-1dbjc4n r-18u37iz r-1q142lx']"
        self.__COMMENT = "//div[@class='css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']"

    def parse_commenter__name_from_comment__element(
        self, commenter_name_element: WebElement
    ) -> str:
        name = commenter_name_element.get_attribute("innerHTML")
        return ContentUtil.strip_all(name)

    def parse_commenter__url_from_comment__element(
        self, commenter_url_element: WebElement
    ) -> str:
        return commenter_url_element.get_attribute("href")

    def parse_comment__time_from_comment__element(
        self, comment__time_element: WebElement
    ) -> str:
        return comment__time_element.find_element(By.TAG_NAME, "time").get_attribute(
            "datetime"
        )

    def parse_comment_from_comment__element(self, comment_element: WebElement) -> str:
        comment = comment_element.get_attribute("innerHTML")
        return ContentUtil.strip_all(comment)

    def parse_comment_details(
        self,
        commenter_name_element: WebElement,
        commenter_url_element: WebElement,
        comment_time_element: WebElement,
        comment_element: WebElement,
    ) -> Comment:
        self.commenter_name = self.parse_commenter__name_from_comment__element(
            commenter_name_element
        )
        self.commenter_url = self.parse_commenter__url_from_comment__element(
            commenter_url_element
        )
        self.comment_time = self.parse_comment__time_from_comment__element(
            comment_time_element
        )
        self.comment = self.parse_comment_from_comment__element(comment_element)
        return self

    def parse_all_comments(self) -> List[Comment]:
        username_elements = driver.find_elements(By.XPATH, self.__USERNAME)[1:]
        userprofile_elements = driver.find_elements(By.XPATH, self.__USER_PROFILE)[2:][
            ::2
        ]
        times_and_urls = driver.find_elements(By.XPATH, self.__TIME_AND_URL)
        parse_comment_elements = driver.find_elements(By.XPATH, self.__COMMENT)

        return [
            Comment().parse_comment_details(
                username_element,
                userprofile_element,
                time_n_url_element,
                parse_comment_element,
            )
            for username_element, userprofile_element, time_n_url_element, parse_comment_element in zip(
                username_elements,
                userprofile_elements,
                times_and_urls,
                parse_comment_elements,
            )
        ]

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

    def __repr__(self) -> str:
        return self.__str__()


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
        text = text_element.get_attribute("innerHTML")
        return ContentUtil.strip_all(text)

    def parse_time_from_time__n__url_element(
        self, time__n__url_element: WebElement
    ) -> str:
        return time__n__url_element.find_element(By.TAG_NAME, "time").get_attribute(
            "datetime"
        )

    def parse_count__reply_from_reply__element(self, reply_element: WebElement) -> int:
        try:
            return int(
                reply_element.find_elements(By.TAG_NAME, "span")[2].get_attribute(
                    "innerHTML"
                )
            )
        except:
            return -1

    def parse_count__retweet_from_retweet__element(
        self, retweet_element: WebElement
    ) -> int:
        try:
            return int(
                retweet_element.find_elements(By.TAG_NAME, "span")[2].get_attribute(
                    "innerHTML"
                )
            )
        except:
            return -1

    def parse_count__like_from_like__element(self, like_element: WebElement) -> int:
        try:
            return int(
                like_element.find_elements(By.TAG_NAME, "span")[2].get_attribute(
                    "innerHTML"
                )
            )
        except:
            return -1

    def parse_url_from_time__n__url_element(
        self, time__n__url_element: WebElement
    ) -> str:
        return time__n__url_element.find_element(By.TAG_NAME, "a").get_attribute("href")

    def parse_from_elements(self, tweet_elements: List[WebElement]) -> Tweet:
        text_element, time_n_url, reply_element, retweet_element, like_element = (
            tweet_elements[0],
            tweet_elements[1],
            tweet_elements[2],
            tweet_elements[3],
            tweet_elements[4],
        )
        self.post_text = self.parse_text_from_text__element(text_element)

        self.post_time = self.parse_time_from_time__n__url_element(time_n_url)

        self.post_url = self.parse_url_from_time__n__url_element(time_n_url)

        self.count_reply = self.parse_count__reply_from_reply__element(reply_element)
        self.count_retweet = self.parse_count__retweet_from_retweet__element(
            retweet_element
        )
        self.count_like = self.parse_count__like_from_like__element(like_element)
        return self

    @staticmethod
    def fetch_tweets_in_page(
        page_scope: WebElement,
    ) -> Tuple[
        List[WebElement],
        List[WebElement],
        List[WebElement],
        List[WebElement],
        List[WebElement],
    ]:
        __TEXTS = "//div[@class='css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']"
        __TIMES_N_URLS = "//div[@class='css-1dbjc4n r-18u37iz r-1q142lx']"
        __REPLY = "//div[@data-testid='reply']"
        __RETWEET = "//div[@data-testid='retweet']"
        __LIKE = "//div[@data-testid='like']"

        texts = page_scope.find_elements(
            By.XPATH,
            __TEXTS,
        )
        times_n_urls = page_scope.find_elements(By.XPATH, __TIMES_N_URLS)
        replies = page_scope.find_elements(By.XPATH, __REPLY)
        retweets = page_scope.find_elements(By.XPATH, __RETWEET)
        likes = page_scope.find_elements(By.XPATH, __LIKE)

        return texts, times_n_urls, replies, retweets, likes

    @staticmethod
    def fetch_tweets_by_count(max_count=20) -> List[Tweet]:
        tweets = []
        count = 0
        __PAGE = "//div[@class='css-1dbjc4n r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l']"

        while True:

            if count >= max_count:  # at least 20
                break
            sleep(2)
            tweets_in_page = driver.find_elements(By.XPATH, __PAGE)
            for scope in tweets_in_page:

                if count >= max_count:  # at least 20
                    break
                (
                    texts,
                    times_n_urls,
                    replies,
                    retweets,
                    likes,
                ) = Tweet.fetch_tweets_in_page(scope)

                for text, time_n_url, reply, retweet, like in zip(
                    texts, times_n_urls, replies, retweets, likes
                ):

                    tweet_instance = Tweet().parse_from_elements(
                        [text, time_n_url, reply, retweet, like]
                    )
                    if tweet_instance.post_url not in [x.post_url for x in tweets]:
                        tweets.append(tweet_instance)

                        print("tweet serial #" + str(count + 1))
                        count += 1
                        if count >= max_count:  # at least 20
                            break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        return tweets

    @staticmethod
    def fetch() -> List[Tweet]:
        tweets = Tweet.fetch_tweets_by_count()

        for tweet in tweets:
            comments, retweets = tweet.get_comments_and_retweets()
            tweet.comments = comments

        return tweets

    @staticmethod
    def save_tweets(tweets: List[Tweet]):
        with open("data.json", "w+", encoding="utf-8") as output_file:
            json.dump(
                [tweet.to_dict() for tweet in tweets],
                output_file,
                ensure_ascii=False,
                indent=4,
            )

    @staticmethod
    def fetch_and_save() -> None:
        tweets = Tweet.fetch()
        Tweet.save_tweets(tweets)

    def to_dict(self) -> Dict:
        return {
            "post_text": self.post_text,
            "post_time": self.post_time,
            "post_url": self.post_url,
            "count_reply": self.count_reply,
            "count_retweet": self.count_retweet,
            "count_like": self.count_like,
            "comments": [x.to_dict() for x in self.comments],
        }

    def __str__(self) -> str:
        return json.dumps(
            self.to_dict(),
            indent=4,
        )

    def __repr__(self) -> str:
        return self.__str__()

    def _open_tweet_page(self) -> None:
        driver.get(self.post_url)

    def get_comments_and_retweets(self) -> Tuple[List[Comment], List[ReTweet]]:
        self._open_tweet_page()
        sleep(2)
        comments = Comment().parse_all_comments()
        retweets = ReTweet().parse_all_retweet()
        return comments, retweets


Tweet.fetch_and_save()


driver.quit()
