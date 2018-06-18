from BluePill import BluePill
import unittest
import boto3

class test_BluePill(unittest.TestCase):

    # setUp
    #
    def setUp(self):
        self.instance = None
        self.result = None
        self.boto3Session = None
        BluePill.CLIENT_TYPE = None
        BluePill.FOLDER_PATH = None
        BluePill.SESSION = None
    
    # _createSession
    #  Helper function to create boto3 sessions
    def _createSession(self):
        return boto3.Session(
            aws_access_key_id='1',
            aws_secret_access_key='1',
            aws_session_token='1',
            region_name='none')
    
    # test_BluePill__init__no_params_no_class_vars
    #
    def test_BluePill__init__no_params_no_class_vars(self):
        self.assertRaises(ValueError, BluePill)

    # test_BluePill__init__only_folder_path
    #
    def test_BluePill__init__only_folder_path(self):
        self.assertRaises(ValueError, BluePill, folder_path='placebo')

    # test_BluePill__init__only_client_type
    #
    def test_BluePill__init__only_client_type(self):
        self.assertRaises(ValueError, BluePill, client_type='cloudformation')
    
    # test_BluePill__init__only_session
    #
    def test_BluePill__init__only_client_session(self):
        self.assertRaises(ValueError, BluePill, session=self._createSession())

    # test_BluePill__init__only_class_FOLDER_TYPE
    #
    def test_BluePill__init__only_class_FOLDER_TYPE(self):
        BluePill.FOLDER_TYPE = 'placebo'
        self.assertRaises(ValueError, BluePill)

    # test_BluePill__init__only_class_CLIENT_TYPE
    #
    def test_BluePill__init__only_class_CLIENT_TYPE(self):
        BluePill.CLIENT_TYPE = 'cloudformation'
        self.assertRaises(ValueError, BluePill)
    
    # test_BluePill__init__only_class_SESSION
    #
    def test_BluePill__init__only_class_SESSION(self):
        BluePill.SESSION = self._createSession()
        self.assertRaises(ValueError, BluePill)
    
    # test_BluePill__init__all_class_variables
    #
    def test_BluePill__init__all_class_variables(self):
        BluePill.CLIENT_TYPE = 'cloudformation'
        BluePill.FOLDER_PATH = 'placebo'
        BluePill.SESSION = self._createSession()
        self.instance = BluePill()
        self.assertIsInstance(self.instance, BluePill)

    # test_BluePill__init__all_init_variables
    #
    def test_BluePill__init__all_init_variables(self):
        self.instance = BluePill(
            client_type='cloudformation',
            folder_path='placebo',
            session=self._createSession())
        self.assertIsInstance(self.instance, BluePill)

    # test_BluePill__call__set_class_variables
    #
    def test_BluePill__call__set_class_client(self):
        BluePill.CLIENT_TYPE = 'cloudformation'
        BluePill.FOLDER_PATH = 'placebo'
        BluePill.SESSION = self._createSession()
        @BluePill()
        def testFunction(arg1=1, arg2=2):
            return arg1+arg2
        self.result = testFunction()

    # test_BluePill__call__with_client_type
    #
    def test_BluePill__call__with_client_type(self):
        BluePill.FOLDER_PATH = 'placebo'
        BluePill.SESSION = self._createSession()
        @BluePill(client_type='cloudformation')
        def testFunction(arg1=1, arg2=2):
            return arg1+arg2
        self.result = testFunction()
    
    # test_BluePill__call__with_folder_path
    #
    def test_BluePill__call__with_folder_path(self):
        BluePill.CLIENT_TYPE = 'cloudformation'
        BluePill.SESSION = self._createSession()
        @BluePill(folder_path='placebo')
        def testFunction(arg1=1, arg2=2):
            return arg1+arg2
        self.result = testFunction()

    # test_BluePill__call__with_session
    #
    def test_BluePill__call__with_session(self):
        BluePill.CLIENT_TYPE = 'cloudformation'
        BluePill.FOLDER_PATH = 'placebo'
        @BluePill(session=self._createSession())
        def testFunction(arg1=1, arg2=2):
            return arg1+arg2
        self.result = testFunction()