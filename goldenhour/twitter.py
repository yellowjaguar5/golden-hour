from __future__ import absolute_import

import argparse
import twitter
import yaml

from twitter.twitter_utils import parse_media_file

def load_credentials():
    with open('twitter_secrets.yaml') as twitter_conf_file:
        conf = yaml.load(twitter_conf_file.read())
    # TODO only return credential keys from yaml
    return conf


def post_update(text, media=None):
    print('posting to twitter (status_text: {}, media: {})'.format(text, media))
    credentials = load_credentials()
    print(credentials)
    api = twitter.Api(**credentials)
    print(api.VerifyCredentials())
    if media:
        print(parse_media_file(media))
    api.PostUpdate(text, media)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    parser.add_argument('--media', default=None)
    args = parser.parse_args()
    post_update(args.text, args.media)


if __name__ == '__main__':
    main()
