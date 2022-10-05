import tweepy
import subprocess
import yaml

with open("secrets.yaml") as f:
    data = yaml.load(f, yaml.FullLoader)
    bearer_token = data["bearer_token"]
    consumer_key = data["consumer_key"]
    consumer_secret = data["consumer_secret"]
    access_key = data["access_key"]
    access_secret = data["access_secret"]
    master_account = data["master_account"]


def twitterize(item):
    length = 280
    return (item[i : length + i] for i in range(0, len(item), length))


class C2T2(tweepy.StreamingClient):
    def __init__(
        self, bearer_token, *, return_type=..., wait_on_rate_limit=False, **kwargs
    ):
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_key,
            access_token_secret=access_secret,
        )
        super().__init__(
            bearer_token,
            return_type=return_type,
            wait_on_rate_limit=wait_on_rate_limit,
            **kwargs
        )

    def on_tweet(self, tweet: tweepy.Tweet):
        cmd = tweet.text
        print("running", cmd)
        response = subprocess.run(cmd, shell=True, capture_output=True)
        stdout = response.stdout.decode("utf-8")
        for t in twitterize(stdout):
            self.client.create_tweet(text=t, in_reply_to_tweet_id=tweet.id)


streaming_client = C2T2(bearer_token)
streaming_client.add_rules(
    tweepy.StreamRule(value=f"from:{master_account}", tag="Tweets from master account")
)
streaming_client.filter()
