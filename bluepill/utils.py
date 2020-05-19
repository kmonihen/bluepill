"""An expanded decorator class for using Placebo when unit testing boto3 calls.

    Typical usage examples:
    bp_config = script(client_type="cloudformation",
                       folder_path="responses",
                       session=boto3_session)
    @bluepill(bp_config)
    def test_cloudformation(self, client):
        response = client.get_stack_policy(StackName="TestStack")
        self.assertEqual(response, "some expected response string")
)
"""

import placebo


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
            script (script): The script configuration.
    """
    @property
    def script(self):
        """The bluepill configuration."""
        return self.__script

    def __init__(self, script):
        """Initialize with a bluepill configuration (script)."""
        self.__script = script

    def __call__(self, function, *args, **kwargs):
        """Set up the placebo client and pass the client to the function.

        Args:
            function (func): The function being wrapped with the placebo client.
        """
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
