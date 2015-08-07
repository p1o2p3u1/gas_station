import ConfigParser

class ConfigHandler:

    def __init__(self):
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.read('app.config')
        print config
        self.path = config.get('svn', 'source_location').replace('\\', '/')
        self.db_user = config.get('mysql', 'username')
        self.db_pass = config.get('mysql', 'passwd')
        self.db_name = config.get('mysql', 'dbname')
        self.db_host = config.get('mysql', 'host')
        self.db_port = config.get('mysql', 'port')
        self.db_charset = config.get('mysql', 'charset')

if __name__ == '__main__':
    c = ConfigHandler()
    print c.path


