import json
import os
import shutil
from datetime import datetime

SESSIONS="Sessions" # constant to define root object in .json file
MOBAXTERM_CONFFILE="/home/mobaxterm/MyDocuments/MobaXterm/MobaXterm.ini"
TMSTMP = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
BOOKMARK_TAG = '[Bookmarks_Sessions_putty_to_moba]'
USERNAME = "JCANOLAB"
PROXY = "proxyges"
PORT = "1080"
FONT_SIZE = "11"
TERM = "xterm"

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

    global TMSTMP
    parent_dir = os.path.dirname(MOBAXTERM_CONFFILE)
    backup_dir = os.path.join(parent_dir, "sessions_backup")
    backup_file = os.path.join(backup_dir, os.path.basename(MOBAXTERM_CONFFILE) + "_" + TMSTMP)

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


def get_group_objs(given_list, value):
    """ Return a list of objects based on group
    :param given_list: list to extract objects
    :param value: value of the attribute group
    :return: new list of objects that match criteria
    """
    new_list = []
    for x in given_list:
        if x.group == value:
            new_list.append(x)

    return new_list


def dummy_write_config(l, fin=MOBAXTERM_CONFFILE):
    """ Write Mobaxterm config file, appending (TODO)
    :param fin: Configuration file
    :param l: list of objects to write
    :return:
    """

    with open(fin, mode="a") as f:
        f.write(BOOKMARK_TAG + "\n")
        f.write("SubRep=level3\n")
        f.write("ImgNum=41\n")

        for obj in l:
            f.write(obj.session_name + "=#109#0%" + obj.host_name + "%22%" + USERNAME + "%%-1%-1%%%22%%0%0%Interactive shell%%%-1%0%0%2%" + PROXY + "%" + PORT + "%%0#Source Code Pro%" + FONT_SIZE + "%0%0%0%15%236,236,236%0,0,0%180,180,192%0%-1%0%%" + TERM + "%-1%0%0,0,0%54,54,54%255,96,96%255,128,128%96,255,96%128,255,128%255,255,54%255,255,128%96,96,255%128,128,255%255,54,255%255,128,255%54,255,255%128,255,255%236,236,236%255,255,255%80%24%0#0" + "\n")

        f.write("\n")

if __name__ == '__main__':
    ses_list = Session.extract_data()
    print "Execution: ", TMSTMP
    print "Making backup file: ", backup_config()

    entornos_list = get_group_objs(ses_list, "Entornos")
    servicios_list = get_group_objs(ses_list, "Servicios")

    print "Writing to config"
    dummy_write_config(entornos_list)
    dummy_write_config(servicios_list)
