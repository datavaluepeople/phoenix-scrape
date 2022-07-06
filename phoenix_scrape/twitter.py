"""Twitter query connections through the Twitter API."""
import logging
import os
import sys

import prefect
import tweepy
from prefect import Flow, task


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

# Application authentication OAuth 2
ENV_BEARER_TOKEN = "TWITTER_BEARER_TOKEN"

QUERY = ""  # Default query for tweet_search(api, q)


def get_client() -> tweepy.Client:
    """Get a Tweepy client based on environment variables."""
    bearer_token = os.getenv(ENV_BEARER_TOKEN)
    if bearer_token:
        logger.info("Using App authentication for tweepy authentication.")
        return tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    raise RuntimeError("Authentication for Twitter is not correctly configured.")


def get_user_tweets(client: tweepy.Client, twitter_id: str, num_items: int) -> tweepy.tweet:
    """Yield tweets composed by a single user."""
    for tweet in tweepy.Paginator(
            client.get_users_tweets, max_results=100, id=twitter_id
    ).flatten(num_items):
        yield tweet


@task
def scrape_twitter():
    logger = prefect.context.get("logger")
    client = get_client()
    logger.info("Got a client")
    # DEBUG code to pull one tweet
    tweets = get_user_tweets(client, "3476266396", 1)
    tweets_json = [tweet._json for tweet in tweets]
    logger.info(tweets_json)


if __name__ == "__main__":
    flow = Flow("scrape_twitter", tasks=[scrape_twitter])
    flow.register(project_name="phoenix-scrape")
    logging.info("successfully registered a flow client")
    scrape_twitter.run()
