import os
from os import walk, path
from os.path import normpath

class FileHandler:

    def __init__(self):
        self.path = "E:/projects/gitlab/biubiu"

    def list_all_files(self):
        """
        list all the files and directories for a given path.
        ignore .svn, .git, .gitignore, *.pyc
        :return: e.g.: {
            'path': '/home/source'
            'dirs': ['dir1', 'dir2', 'dir3'],
            'files': ['file1', 'file2', 'file3'],
            'dir1': ['/home/source/dir1/f1.py', '/home/source/dir1/a/f2.py'],
            'dir2': ['/home/source/dir3/f1.py', '/home/source/dir3/f2.py', '/home/source/dir3/aa/bb/cc/dd.py']
        }
        """
        result = {
            'path': self.path,
            'dirs': [],
            'files': []
        }
        for dirname, dirs, files in walk(self.path):
            for d in dirs:
                if not d.startswith('.'):
                    result['dirs'].append(d)
            for f in files:
                if not d.startswith('.') and d.endswith('.py'):
                    result['files'].append(f)
            break

        for t_dir in result['dirs']:
            result[t_dir] = []
            sub_path = path.join(self.path, t_dir)
            for dirname, dirs, files in walk(sub_path):
                for t_file in files:
                    if not t_file.startswith('.') and t_file.endswith('.py'):
                        location = path.join(t_dir, t_file)
                        result[t_dir].append(normpath(location))
        return result

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
        location = path.join(self.path, filename)
        with open(location, 'r') as reader:
            result['text'] = reader.read()
        return result
