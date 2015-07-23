import ConfigParser

class ConfigHandler:

    def __init__(self):
        self.config = ConfigParser.RawConfigParser(allow_no_value=True)
        self.config.read('app.config')
        self.path = self.config.get('svn', 'source_location').lower().replace('\\', '/')

if __name__ == '__main__':
    c = ConfigHandler()
    print c.path


