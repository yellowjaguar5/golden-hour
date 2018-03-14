# golden-hour

A python script to generate a timelapse video. Designed specifically to record at sunset, and post to twitter with a weather report.

## Setup

This project assumes that you will run this on [a Raspberry Pi][pi] with a CSI-port camera, although pull requests to broaden that support are certainly accepted. [@goldenhourSEA][goldenhourSEA] runs on a [Pi 3 Model B][model-3] with the [Camera Module V2][camera].

[pi]: https://www.raspberrypi.org
[camera]: https://www.raspberrypi.org/products/camera-module-v2/
[goldenhourSEA]: https://twitter.com/goldenhourSEA
[model-3]: https://www.raspberrypi.org/products/raspberry-pi-3-model-b/

### Installation

#### Installing [`FFmpeg`][ffmpeg]

FFmpeg is used to convert the sequence of photos captured by the camera into a video suitable for uploading to Twitter. FFmpeg must be compiled with x264 support. On Raspberry Pi I found [these instructions][ffmpeg-pi] to be helpful. If you are running this on a Mac, `brew install ffpmeg` should be sufficient.

[ffmpeg]: http://ffmpeg.org
[ffmpeg-pi]: http://www.jeffreythompson.org/blog/2014/11/13/installing-ffmpeg-for-raspberry-pi/

#### Installing `golden-hour`

1. Check out this repo to a convenient location on your Pi.
2. Run `pip install -r requirements` (I recommend doing this in a virtualenv)

#### Configuration

##### Twitter

1. Create a Twitter account.
    - I recommend a name like "goldenhourXYZ", where XYZ is airport code or abbrevation for your city.
    - You may want to associate the account with a phone number, to avoid Twitter's anti-spam measures.
2. Create a [Twitter "app"][twitter-app] for that account.
    - Make sure to set the access permissions to "Read and write", otherwise you won't be able to post tweets.
    - In the root of the repo, create a `twitter_secrets.yaml` file, and put the consumer key, consumer secret, access token, and access token secret in there:

```yaml
consumer_key: CONSUMER KEY
consumer_secret: CONSUMER SECRET
access_token_key: ACCESS TOKEN KEY
access_token_secret: ACCESS TOKEN SECRET
```

[twitter-app]: https://apps.twitter.com

##### Dark Sky *(optional)*

If you want the weather report, [get a Dark Sky API key][dark-sky-api].

[dark-sky-api]: https://darksky.net/dev

#### Running automatically

Once you have everything set up, set up a cron job to run `golden-hour` at the same time every day. Make sure it runs at least one hour before the earliest sunset of the year.

Gotchas:

- `cron` runs in a different environment from your normal shell. In my case, it did not have access to `ffmpeg`, because I had installed it to `/usr/local/bin`, but the `$PATH` only had `/bin` and `/usr/bin`.
- Your Pi may not be configured to your local timezone. Run `date` to see what time it is for your Pi, and set the cron job to run at an appropriate translated time. I set mine to run at 2300, which is 3pm local time.
