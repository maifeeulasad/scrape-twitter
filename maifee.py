from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep

# import re

base_url = "https://twitter.com/"

driver = webdriver.Chrome()
driver.get(base_url + "bbcbangla")
sleep(3)
count = 0


"""
css-1dbjc4n r-18u37iz r-1q142lx       <<----- Post URL, Post Time
css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0  <<------ Post Text
css-901oao r-1awozwy r-1bwzh9t r-6koalj r-37j5jr r-a023e6 r-16dba41 r-1h0z5md r-rjixqe r-bcqeeo r-o7ynqc r-clp7b1 r-3s2u2q r-qvutc0 <<----- option, No. of Comments, No. of Retweets, No. of Likes
"""

"""
Fields to Scrape: Posts, Post URL, Post Time, Post Text, No. of Comments, No. of Retweets, No. of Likes, Commenter Name, Commenter profile URL, Comment time, Comment, Who Retweets, Retweet Text, Retweeter URL
"""

while True:
    if count >= 20:  # at least 20
        break
    sleep(2)
    tweets_in_page = driver.find_elements(
        By.XPATH, "//div[@class='css-1dbjc4n r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l']"
    )
    for scope in tweets_in_page:
        tweets = scope.find_elements(
            By.XPATH,
            "//div[@class='css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']",
        )
        times_n_urls = scope.find_elements(
            By.XPATH, "//div[@class='css-1dbjc4n r-18u37iz r-1q142lx']"
        )
        for tweet, time_n_url in zip(tweets, times_n_urls):
            print("serial : ", count)
            # print(re.sub('<[^<]+?>', '', tweets.get_attribute("innerHTML")))
            post_text = tweet.get_attribute("innerHTML")
            print(post_text)
            print("")

            post_time = time_n_url.find_element(By.TAG_NAME, "time").get_attribute(
                "datetime"
            )
            print(post_time)
            print("")

            post_url = time_n_url.find_element(By.TAG_NAME, "a").get_attribute("href")
            print(post_url)
            print("")

            count += 1
            if count >= 20:  # at least 20
                break

        print("------------")
        break
    break
    count += 1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
driver.quit()
