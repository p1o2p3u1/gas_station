import os
from config_handler import ConfigHandler

class FileHandler:

    def __init__(self):
        self.config = ConfigHandler()
        self.path = self.config.path

    def list_all_files(self):
        """
        list all the files and directories for a given path.
        ignore .svn, .git, .gitignore, *.pyc
        :return: e.g.: {
            'path': '/home/source'
            'dirs': ['dir1', 'dir2', 'dir3'],
            'files': ['file1', 'file2', 'file3'],
            'dir1': ['dir1/f1.py', 'dir1/a/f2.py'],
            'dir2': ['dir2/f1.py', 'dir2/f2.py', 'dir2/aa/bb/cc/dd.py'],
            'dir3': []
        }
        """
        result = {
            'path': self.path,
            'dirs': [],
            'files': []
        }
        dirs = []
        files = []
        for filename in os.listdir(self.path):
            # ignore .git .ssh .svn, etc
            if not filename.startswith('.'):
                full_path = os.path.join(self.path, filename)
                if os.path.isdir(full_path):
                    dirs.append(filename)
                else:
                    # ignore .pyc
                    if filename.endswith('.py'):
                        files.append("/" + filename)
        result['dirs'] = sorted(dirs)
        result['files'] = sorted(files)

        for dirname in result['dirs']:
            full_path = self.path + '/' + dirname
            result[dirname] = self._dfs(full_path)

        return result

    def _dfs(self, filename):
        stack = []
        ret = []
        stack.append(filename)
        while len(stack) > 0:
            tmp = stack.pop()
            if os.path.isdir(tmp):
                for item in os.listdir(tmp):
                    # ignore .git .xxoo
                    if not item.startswith('.'):
                        # why not use path.join? because in windows we usually have a\\b and
                        # in linux we usually have a/b, however, the path is the id of some
                        # html element, which may cause conflicts
                        stack.append(tmp + '/' + item)
            else:
                if not tmp.startswith('.') and tmp.endswith('.py'):
                    # ignore .gitignore, *.pyc
                    ret.append(tmp.replace(self.path, ''))
        return ret

    def get_source(self, filename):
        """
        get the source text of the file
        :param filename: the name of the source file.
        :return: e.g. {
            'filename': 'a.py',
            'text': "print 'hi'"
            'revision': 1234
        }
        """
        result = {
            'filename': filename
        }
        location = self.path + '/' + filename
        with open(location, 'r') as reader:
            result['text'] = reader.read()
        return result

if __name__ == '__main__':
    f = FileHandler()
    print f.list_all_files()
