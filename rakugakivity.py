from typing import NamedTuple
from datetime import datetime

from twitter_scraper import get_tweets


class Tweet(NamedTuple):
    id: int
    created_at: datetime
    images: str
    retweets: int
    likes: int

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            id=d['tweetId'],
            created_at=d['time'],
            images=d['entries']['photos'],
            retweets=d['retweets'],
            likes=d['likes']
        )


class UserTweets():

    def __init__(self, username):
        self.username = username

    def fetch_all(self):
        page = 1
        ret = []
        try:
            tweets = get_tweets(self.username, pages=page)
            ret.extend([Tweet.from_dict(t) for t in tweets])
        finally:
            return ret
