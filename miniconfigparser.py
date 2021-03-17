class MiniConfigParser():
    def __init__(self, location="config.ini"):
        """Load and interpret config. Returns config."""
        with open(location, 'rt') as f:
            raw_config = f.readlines()
        full_config = {}
        for line in raw_config:
            key = line.split('=')[0]
            value = '='.join(line.split('=')[1:])
            full_config[key] = value
        self.config = self._special_mappings(full_config)
        return self.config

    def _special_mappings(config):
        """Do some extra processing. For example, convert to int."""
        config['display_clock'] = int(config['display_clock'])
        config['display_dio'] = int(config['display_dio'])
        return config

    def __getitem__(self, item):
        """Allow this class to be used as a list."""
        return self.config[item]

