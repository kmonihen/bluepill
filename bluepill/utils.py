"""An expanded decorator class for using Placebo when unit testing boto3 calls.

    Typical usage examples:

    bluepill.default_script = script(client_type="cloudformation",
                                     folder_path="responses",
                                     session=boto3_session)
    @bluepill()
    def test_cloudformation(self, client):
        # Use a placebo session with the default settings.
        response = client.get_stack_policy(StackName="SomeTestStack")
        self.assertEqual(response, "some expected response string")
    
    @bluepill(client_type="s3")
        # Use an s3 client with the default settings.
        def test_s3(self, client):
            response = client.get_bucket_tagging(Bucket="SomeTestBucket")
            self.assertEqual(response, "some expected response string")
"""

import placebo
import copy
from functools import wraps


class script():
    """[summary]
    
        Attributes:
            session (boto3.Session): Boto3 session.
            client_type (str): The boto3 client type.
            folder_path (str): The path of the placebo data folder.
            record (bool): Enable recording mode.
    """
    def __init__(self, client_type, folder_path, session, record=False):
        """Set the class variables.

        Args:
            client_type (str): [description]
            folder_path (str): [description]
            session (boto3.Session): [description]
            record (bool, optional): [description]. Defaults to False.
        """
        self.client_type = client_type
        self.folder_path = folder_path
        self.session = session
        self.record = record


class bluepill():
    """A decorator class to help testing with placebo.
    
        Attributes:
            default_script (script, optional): The default script properties to use. Defaults to None.
            script (script): The script configuration.
    """

    default_script = None

    @property
    def script(self):
        """The bluepill configuration."""
        return self.__script

    def __init__(self, **kwargs):
        """Initialize with a bluepill configuration (script)."""
        if "script" in kwargs:
            self.__script = kwargs.get("script")
        elif self.default_script:
            self.__script = copy.deepcopy(self.default_script)
        else:
            raise TypeError("You must provide a script parameter or set the default_script attribute.")

        self.script.client_type = kwargs.get("client_type", self.script.client_type)
        self.script.folder_path = kwargs.get("folder_path", self.script.folder_path)
        self.script.session = kwargs.get("session", self.script.session)
        self.script.record = kwargs.get("record", self.script.record)

    def __call__(self, function, *args, **kwargs):
        """Set up the placebo client and pass the client to the function.

        Args:
            function (func): The function being wrapped with the placebo client.
        """
        @wraps(function)
        def placebo_test(*args, **kwargs):
            """Wrapping the test function.

            Returns:
                func: The wrapped function.
            """
            # Attach to session.
            pill = placebo.attach(self.script.session,
                                  data_path=self.script.folder_path)

            # Set the client for use in the test.
            kwargs["client"] = self.script.session.client(
                self.script.client_type)

            # Record calls if record has been toggled on, otherwise play back existing calls.
            if self.script.record:
                pill.record()
            else:
                pill.playback()

            return function(*args, **kwargs)

        return placebo_test
