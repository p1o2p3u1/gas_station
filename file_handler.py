import os

class FileHandler:

    def __init__(self):
        self.path = "E:/projects/gitlab/biubiu"

    def list_all_files(self):
        """
        list all the files and directories for a given path.
        :return: {
            'path': 'E:/projects/gitlab/biubiu'

        }
        """
        result = {'path': self.path}
        for dirname, dirnames, filenames in os.walk(self.path):
            pass

        return result