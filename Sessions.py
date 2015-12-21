import json
import os
import shutil
from datetime import datetime

SESSIONS="Sessions" # constant to define root object in .json file
MOBAXTERM_CONFFILE="/home/mobaxterm/MyDocuments/MobaXterm/MobaXterm.ini"
tmstmp = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')


class Session:
    """ Store a session info
    """

    def __init__(self, id, session_name, host_name, session_id, group, folder, context=None, tech=None, environ=None):

        # Common attributes Servicios and Entornos
        self.id = id
        self.session_id = session_id
        self.session_name = session_name
        self.host_name = host_name
        self.group = group # folder level 1
        self.folder = folder # folder level 2

        self.environ = environ # folder level 3

        self.context = context # folder level 3
        self.tech = tech # folder level 4

    @staticmethod
    def read_json(fin="Sessions.json"):
        """
        :param fin: file input to read sessions
        :return: entry: python dictionary with the json
        """

        with open(fin) as f:
            entry = json.load(f)

        return entry

    @staticmethod
    def extract_data():
        """ Read sessions from a .json file and map to a list of Session objects
        :return: ses_list: list of Session objects
        """

        ses_list = []

        entry = Session.read_json()

        # for each session in json
        for json_ses in entry[SESSIONS]:
            # create a new Session object with json data
            ses = Session(**json_ses)
            ses_list.append(ses)

        return ses_list


def backup_config(fin=MOBAXTERM_CONFFILE):
    """ Make a backup of Mobaxterm configuration file
    :param fin:
    :return: backup_file: string containing the backup file name
    """

    global tmstmp
    parent_dir = os.path.dirname(MOBAXTERM_CONFFILE)
    backup_dir = os.path.join(parent_dir, "sessions_backup")
    backup_file = os.path.join(backup_dir, os.path.basename(MOBAXTERM_CONFFILE) + "_" + tmstmp)

    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)

    shutil.copy2(MOBAXTERM_CONFFILE, backup_file)

    return backup_file


def read_config(fin=MOBAXTERM_CONFFILE):
    """ Return a string with the MobaXterm configuration
    :param fin: file input to read
    :return: str_conf: string containg config file
    """

    # return str_conf
    with open(fin) as f:
        str_conf = f.read()
        return str_conf


def dummy_write_config(fin=MOBAXTERM_CONFFILE):
    """ Write Mobaxterm config file, appending (TODO)
    :param fin: Configuration file
    :return:
    """

    with open(fin, mode="a") as f:
        f.write("-------------\n")
        f.write("prueba\n")
        f.write("-------------\n")


if __name__ == '__main__':
    ses_list = Session.extract_data()
    print "Execution: ", tmstmp
    print "Making backup file: ", backup_config()
    print "Writing to config"
    dummy_write_config()
    print "list of Session objects:"
    print ses_list

