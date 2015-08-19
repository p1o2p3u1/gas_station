import os
import subprocess

from coverage.parser import CodeParser
from app.config_handler import ConfigHandler
import app.parser as parser
from app.dbs import file_db

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
        cache = file_db.query_dirs(self.path)
        if cache:
            return cache
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
                        parser = CodeParser(filename=full_path)
                        statements, _ = parser.parse_source()
                        files.append(("/" + filename, len(statements)))
        result['dirs'] = sorted(dirs)
        result['files'] = sorted(files)

        for dirname in result['dirs']:
            full_path = self.path + '/' + dirname
            result[dirname] = self._dfs(full_path)
        file_db.save_dirs(self.path, result)
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
                    parser = CodeParser(filename=tmp)
                    statements, _ = parser.parse_source()
                    ret.append((tmp.replace(self.path, ''), len(statements)))
        return ret

    def get_source(self, filename, revision=None, repo='svn'):
        """
        get the source text of the file
        :param filename: the name of the source file
        :param revision: the version of the file
        :param repo: svn or git repo
        :return: e.g.
        {
           'filename': 'filename1.py',
           'URL': 'http://svn.netease.com/repo/filename1.py',
           'Revision': '10',
           'text': 'print "hello world"'
        }
        """
        result = {
            'filename': filename
        }
        location = self.path + '/' + filename

        if repo == 'svn':
            # if revision is not given, use svn info to get the current vision
            if not revision:
                p = subprocess.Popen(
                    ['svn', 'info', location],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)

                out, err = p.communicate()
                lines = out.split('\n')
                for line in lines:
                    if line.startswith('URL'):
                        result['URL'] = line[line.index(':') + 1:].strip()
                    elif line.startswith('Last Changed Rev'):
                        revision = line[line.index(':') + 1:].strip()
                        result['Revision'] = revision

            cache = file_db.query_file(filename, revision)
            if cache is not None:
                result['text'] = cache
            else:
                # get the source text for a specific version
                p = subprocess.Popen(
                    ['svn', 'cat', location, '-r', revision],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)

                out, err = p.communicate()
                if len(err) > 0:
                    result['text'] = err
                else:
                    result['text'] = out
                    file_db.save_file(filename, revision, out)
        else:
            # git? next time baby
            pass
        return result

    def show_diff(self, filename, old_version, cur_version, repo='svn'):
        result = {
            'filename': filename,
            'update': []
        }
        location = self.path + '/' + filename
        if repo == 'svn':
            cache = file_db.query_diff(filename, old_version, cur_version)
            if cache:
                result['update'] = cache
            else:
                # get svn diff info with command 'svn diff -r v1:v2 filepath'
                p = subprocess.Popen(
                    ['svn', 'diff', '-r', old_version+':'+cur_version, location],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)

                out, err = p.communicate()
                if len(err) > 0:
                    result['error'] = err
                else:
                    # the output is unidiff format
                    modified = parser.parse_unidiff(out)
                    result['update'] = modified
                    file_db.save_diff(filename, old_version, cur_version, modified)
        else:
            # git?
            pass
        return result

    def show_log(self, filename, limit, repo='svn'):
        """
        list svn logs with command 'svn log filename -l limit'
        :param filename: the name of the file
        :param limit: how many logs should display
        :return:
        """
        result = {
            'filename': filename,
            'limit': limit
        }
        location = self.path + '/' + filename
        if repo == 'svn':
            p = subprocess.Popen(
                ['svn', 'log', location, '-l', limit, '--xml'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            out, err = p.communicate()
            if len(err) > 0:
                result['error'] = err
            else:
                logs = parser.parse_svn_log(out)
                result['logs'] = logs
        else:
            # git?
            pass
        return result


if __name__ == '__main__':
    f = FileHandler()
    print f.list_all_files()
