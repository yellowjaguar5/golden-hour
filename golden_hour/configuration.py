import schema
import yaml

from golden_hour import tweet, location


GOLDENHOUR_CONFIGURATION_SCHEMA = schema.Schema({
    'location': location.LOCATION_CONFIG_SCHEMA,
    schema.Optional('twitter'): tweet.TWITTER_CONFIG_SCHEMA,
    schema.Optional('darksky_key'): str,
    schema.Optional('climacell_key'): str,
    schema.Optional('use_air_quality_sensor'): bool,
})


def load_configuration(config_file_path):
    with open(config_file_path) as config_file:
        config = yaml.load(config_file.read())

    return GOLDENHOUR_CONFIGURATION_SCHEMA.validate(config)
