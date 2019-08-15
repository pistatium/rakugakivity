import argparse

from typing import NamedTuple, List
from datetime import datetime

from twitter_scraper import get_tweets


class Tweet(NamedTuple):
    id: int
    text: str
    created_at: datetime
    images: str
    retweets: int
    likes: int

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            id=d['tweetId'],
            text=d['text'],
            created_at=d['time'],
            images=d['entries']['photos'],
            retweets=d['retweets'],
            likes=d['likes']
        )


class UserTweets():

    def __init__(self, username):
        self.username = username

    def fetch_all(self) -> List[Tweet]:
        page = 1

        while True:
            try:
                tweets = get_tweets(self.username, pages=page)
                for tweet in tweets:
                    if tweet['isRetweet']:
                        continue
                    tw = Tweet.from_dict(tweet)
                    if tw.images:
                        yield tw
                page += 1
            except Exception as e:
                print(e)
                break


def format_as_csv(tweets: List[Tweet]) -> str:
    return f'{tw.created_at.isoformat()}, {tw.likes}, {tw.retweets}, {tw.images[0]}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze your rakugaki tweet.')
    parser.add_argument('username', help='twitter user name(without @)')
    args = parser.parse_args()

    print('created_at, like, rt, image')

    for tw in UserTweets(args.username).fetch_all():
        print(format_as_csv(tw))
