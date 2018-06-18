# BluePill
# Author: Keith Monihen, 2018
#
# An expanded decorator class for using Placebo when unit testing boto3 calls.
#
# Provides:
#  BluePill class
import placebo
import boto3

class BluePill(object):

    # Set these as defaults in the TestCase setUp.
    SESSION = None # A boto3 session that Placebo attaches to.
    CLIENT_TYPE=None # The boto3 client type. 
    FOLDER_PATH=None # The path of the placebo data folder

    # __init__
    #
    # Optional Parameters:
    #  client_type (String) - The boto3 client type.
    #  folder_path (String) - The path of the placebo data folder.
    #  session (boto3.Session) - A boto3 session that Placebo attaches to.
    def __init__(self, client_type=None, folder_path=None, session=None):
        # Either use the provided values or the class values
        self.session = session if session else self.SESSION
        self.clientType = client_type if client_type else self.CLIENT_TYPE
        self.folderPath = folder_path if folder_path else self.FOLDER_PATH

        # Raise exception if none of the required variables are provided
        if not self.clientType: raise ValueError("You must provide 'client_type' parameter or set the 'CLIENT_TYPE' class variable.")
        if not self.folderPath: raise ValueError("You must provide 'folder_path' parameter or set the 'FOLDER_PATH' class variable.")
        if not self.session: raise ValueError("You must provide the 'session' parameter or set the 'SESSION' class variable.")
    
    # __call__
    #
    def __call__(self, function, *args, **kwargs):
        def wrappedFunction(*args, **kwargs):
            # Attach the session to the response data and start playback
            pill = placebo.attach(self.session, data_path=self.folderPath)

            client = self.session.client(self.clientType)
            #TODO: get client to test function
            
            pill.playback()
            return function(*args, **kwargs)
        return wrappedFunction