import json
from pprint import pprint

class Session:
    """ Store a session info
    """

    def __init__(self, id, session_name, host_name, session_id, group, folder, context=None, tech=None, environ=None):

        # atributos comunes a los grupos Servicios y Entornos
        self.id = id
        self.session_id = session_id
        self.session_name = session_name
        self.host_name = host_name
        self.group = group # folder level 1
        self.folder = folder # folder level 2

        # atributos variables
        if group == 'Servicios':
            self.environ = environ # folder level 3
        elif group == 'Entornos':
            self.context = context # folder level 3
            self.tech = tech # folder level 4

    def simple_test(self):
        """ Simple test to check attributes of the class
        """
        s1 = Session("0", "EXTRANET_APACHE_ejld124", "ejld124ges", "Servicios/22.interior/2.desarrollo/EXTRANET_APACHE_ejld124",
                     "Servicios", "22.interior", environ="2.desarrollo")

        s2 = Session("1", "ejld124ges", "ejld124ges", "Entornos/0.desarrollo/EXTRANET/APACHE/ejld124",
                     "Entornos", "0.desarrollo", context="EXTRANET", tech="APACHE")

        print("-----------------------------")
        pprint("s1")
        pprint(vars(s1))
        print("-----------------------------")
        pprint("s2")
        pprint(vars(s2))

    @staticmethod
    def extract_data(fin="Sessions.json"):
        """ Read sessions from a text file
        :param fin: file input to read sessions
        :return:
        """

        with open(fin) as f:
            entry = json.load(f)



def object_decoder(obj):
    # if obj['__type__'] == 'Session':
    return Session(obj['id'], obj['session_name'], obj['host_name'], obj['session_id'],
                           obj['group'], obj['folder'], obj['context'], obj['tech'])

if __name__ == '__main__':
    s1 = json.loads('{"__type__": "Session", "id": "1", "session_name": "ejld1007ges", "host_name": "ejld1007ges", "session_id": "Entornos/0.desarrollo/EXTRANET/WLS1036/ejld1007", "group": "Entornos", "folder": "0.desarrollo", "context": "EXTRANET", "tech": "WLS1036"}', object_hook=object_decoder)
    pprint(vars(s1))
    # json.loads('{"id": "1", "session_name": "ejld1007ges", "host_name": "ejld1007ges", "session_id": "Entornos/0.desarrollo/EXTRANET/WLS1036/ejld1007", "group": "Entornos", "folder": "0.desarrollo", "context": "EXTRANET", "tech": "WLS1036"}', object_hook=object_decoder)
    # Session.extract_data()
