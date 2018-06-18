from BluePill import BluePill
import unittest

class test_BluePill(unittest.TestCase):

    # setUp
    #
    def setUp(self):
        def testFunction(arg1=1, arg2=2):
            return arg1+arg2
        self.testFunction = testFunction
        self.instance = None
        self.result = None
    
    # test_BluePill__init__
    #
    def test_BluePill__init__(self):
        self.instance = BluePill(self.testFunction)
    
    # test_BluePill__call__
    #
    def test_BluePill__call__(self):
        @BluePill
        def testFunction(arg1=1, arg2=2):
            return arg1+arg2
        self.result = testFunction()

    # test_BluePill__call__with_client_type
    #
    def test_BluePill__call__(self):
        @BluePill(client_type='test')
        def testFunction(arg1=1, arg2=2):
            return arg1+arg2
        self.result = testFunction()