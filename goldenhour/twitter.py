from __future__ import absolute_import

import argparse
import twitter
import yaml

from twitter.twitter_utils import parse_media_file

def load_credentials():
    with open('twitter_secrets.yaml') as twitter_conf_file:
        conf = yaml.load(twitter_conf_file.read())
    return {
        'consumer_key': conf['consumer_key'],
        'consumer_secret': conf['consumer_secret'],
        'access_token_key': conf['access_token_key'],
        'access_token_secret': conf['access_token_secret'],
    }


def post_update(text, media=None):
    print('posting to twitter (status_text: {}, media: {})'.format(text, media))
    credentials = load_credentials()
    api = twitter.Api(**credentials)

    media_id = None
    if media:
        with open(media, 'rb') as mediafile:
            media_id = api.UploadMediaChunked(mediafile)

    api.PostUpdate(text, media=media_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    parser.add_argument('--media', default=None)
    args = parser.parse_args()
    post_update(args.text, args.media)


if __name__ == '__main__':
    main()
