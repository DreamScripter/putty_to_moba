import json

SESSIONS="Sessions" # constant to define root object in .json file

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

if __name__ == '__main__':
    ses_list = Session.extract_data()
    print("")
    print("list of Session objects:")
    print(ses_list)

