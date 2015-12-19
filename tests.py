import unittest
import Sessions


class Test(unittest.TestCase):
    def test_json_equals_object(self):
        pass # TODO

    def test_create_session_obj(self):
        """ Simple test create two objects of the class Session, calling its __init__ method
            Creates two Session objects and prints its variables
        """
        id = "0"
        session_name = "EXTRANET_APACHE_ejld124"
        host_name = "ejld124ges"
        session_id = "Servicios/22.interior/2.desarrollo/EXTRANET_APACHE_ejld124"
        group = "Servicios"
        folder = "22.interior"
        environ = "2.desarrollo"
        context = None
        tech = None

        s1 = Sessions.Session(id, session_name, host_name, session_id, group, folder, environ, context, tech)
        self.assertEqual(s1.host_name, host_name)

if __name__ == '__main__':
    unittest.main()