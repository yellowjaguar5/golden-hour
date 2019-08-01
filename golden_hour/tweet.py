from __future__ import absolute_import

import argparse
import logging
import twitter
import yaml

import schema


logger = logging.getLogger()

def verify_credentials(credentials):
    api = twitter.Api(**credentials)

    return api.VerifyCredentials() is not None

TWITTER_CONFIG_SCHEMA = schema.And(
    {
        'consumer_key': str,
        'consumer_secret': str,
        'access_token_key': str,
        'access_token_secret': str,
    },
    verify_credentials
)


def post_update(credentials, text, media=None):
    TWITTER_CONFIG_SCHEMA.validate(credentials)

    logger.info('posting to twitter (status_text: {}, media: {})'.format(text, media))
    api = twitter.Api(**credentials)

    media_id = None
    if media:
        with open(media, 'rb') as mediafile:
            media_id = api.UploadMediaChunked(mediafile)

    api.PostUpdate(text, media=media_id)


def load_credentials_from_file(filepath):
    ''' Load credentials from a YAML file.
    Supports files with twitter configuration parameters under a "twitter" key, or at the top level.
    Expects the parameters to match the format of TWITTER_CONFIG_SCHEMA.
    '''
    with open(filepath) as twitter_conf_file:
        conf = yaml.load(twitter_conf_file.read())

    return TWITTER_CONFIG_SCHEMA.validate(
        conf['twitter'] if 'twitter' in conf else conf
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    parser.add_argument('--media', default=None)
    parser.add_argument('--credentials-file', default='twitter_secrets.yaml')
    args = parser.parse_args()

    credentials = load_credentials_from_file(args.credentials_file)
    post_update(credentials, args.text, args.media)


if __name__ == '__main__':
    main()
