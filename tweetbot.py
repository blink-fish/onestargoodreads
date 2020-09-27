
import tweepy
import requests
import xml.etree.ElementTree as ET
import re
from os import environ

consumer_key = environ['TWITTER_CONSUMER_KEY']
consumer_secret = environ['TWITTER_CONSUMER_SECRET']
access_token = environ['TWITTER_ACCESS_TOKEN']
access_token_secret = environ['TWITTER_ACCESS_TOKEN_SECRET']
goodreadsKey = environ['GOODREADS_KEY']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# This script grabs the 20 most recent reviews on Goodreads and sorts them by worst rated. It places a payload of data
# about the worst review in a payload variable called worstBook.


tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

# Goodreads stuff


params = {'key': goodreadsKey}
r = requests.get(
    'https://www.goodreads.com/review/recent_reviews', params=params)
root = ET.fromstring(r.content)
reviews = root[1]
review_list = []
for review in reviews:
    id = review.find('id').text
    title = review.find('book/title').text
    image_url = review.find('book/image_url').text
    avg_rating = review.find('book/average_rating').text
    ratings_count = review.find('book/ratings_count').text
    author = review.find('book/authors/author/name').text
    rating = review.find('rating').text
    review_body = review.find('body').text
    review_link = review.find('link').text
    print(rating)
    if int(rating) == 1:
        review_list.append(
            {
                'title': title,
                'url': image_url,
                'id': id,
                'avg_rating': avg_rating,
                'ratings_count': ratings_count,
                'author': author,
                'rating': rating,
                'review_body': review_body,
                'review_link': review_link
            }
        )
if review_list != []:
    sortedList = sorted(
        review_list, key=lambda book:  book['rating'])

    worstBook = sortedList[0]

    # handling various contingencies for worstReview; striping it to two sentences
    worstReview = tag_re.sub('', worstBook['review_body']).strip()
    if '.' in worstReview:
        worstSentences = worstReview.rsplit('. ')
        if len(worstSentences) > 1:
            twoWorstSentences = (f'{worstSentences[0]}. {worstSentences[1]}.')
        else:
            twoWorstSentences = (f'{worstSentences[0]}')

    else:
        twoWorstSentences = worstReview.strip()

    worstLink = worstBook['review_link'].strip()
    worstTitle = worstBook['title'].strip()
    worstAuthor = worstBook['author'].strip()

    tweet = (
        f'{twoWorstSentences} {worstLink}')

    cleanTweet = " ".join(tweet.split())

    # # Twitter stuff

    def tweet():
        tweettopublish = cleanTweet
        api.update_status(tweettopublish)

    tweet()
else:
    exit("No one-star reviews this time.")
