"""Tests for the bluepill decorator class and the script configuration class."""

from bluepill.utils import bluepill, script
import unittest
import boto3


class test_bluepill(unittest.TestCase):
    """Test the bluepill decorator class."""
    def _create_session(self):
        """Helper function to create boto3 sessions."""
        return boto3.Session(aws_access_key_id='1',
                             aws_secret_access_key='1',
                             aws_session_token='1',
                             region_name='none')

    def test_script(self):
        """Test the script class."""
        test_session = self._create_session()
        test_script_all_params = script(client_type="cloudformation",
                                        folder_path="responses",
                                        session=test_session,
                                        record=True)
        self.assertEqual(test_script_all_params.client_type, "cloudformation")
        self.assertEqual(test_script_all_params.folder_path, "responses")
        self.assertEqual(test_script_all_params.session, test_session)
        self.assertEqual(test_script_all_params.record, True)

        test_script_default_record = script(client_type="cloudformation",
                                            folder_path="responses",
                                            session=test_session)
        self.assertEqual(test_script_default_record.record, False)

    def test_bluepill_no_script(self):
        """Test instantiating bluepill without a script config. Should throw a TypeError."""
        with self.assertRaises(TypeError):
            self.instance = bluepill()  # pylint: disable=no-value-for-parameter

    def test_bluepill_with_script(self):
        """Test instantiating bluepill with a script config."""
        test_script = script(client_type="cloudformation",
                             folder_path="responses",
                             session=self._create_session())
        self.instance = bluepill(script=test_script)

    def test_bluepill__call__(self):
        """Test the bluepill decorator."""
        test_script = script(client_type="cloudformation",
                             folder_path="responses",
                             session=self._create_session())

        @bluepill(test_script)
        def testFunction(client, arg1=1, arg2=2):
            return arg1 + arg2

        self.assertEqual(testFunction(), 3)

    def test_bluepill_call_without_client(self):
        """Test the bluepill decorator without specifying the client parameter."""
        test_script = script(client_type="cloudformation",
                             folder_path="responses",
                             session=self._create_session())

        @bluepill(test_script)
        def testFunction():
            return True

        self.assertRaises(TypeError, testFunction)

    def test_BluePill__call__recording(self):
        """Test bluepill recording."""
        test_script = script(client_type="s3",
                             folder_path="test/responses/record",
                             session=self._create_session(),
                             record=True)

        @bluepill(test_script)
        def testRecord(client):
            return True

        self.assertTrue(testRecord())
