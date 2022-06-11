from os import listdir
from os.path import isfile, join


class DocumentCollection:
    @staticmethod
    def get_file_names(directory_path):
        # list of files only no directories
        files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
        return files
