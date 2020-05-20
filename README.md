
#  bluepill
An expanded decorator class for modifying Placebo playback when unit testing with boto3 calls.

## Requirements
Python 3.6+

## Installation
TODO

## Usage Examples
### bluepill with playback
```python
from bluepill.utils import bluepill, script
import boto3
import unittest

class test_SomeAWSFunctions(unittest.TestCase):

    def setUp(self):
        """Create a default bluepill/Placebo environment."""
        placebo_session = boto3.Session(
            aws_access_key_id="1",
            aws_secret_access_key="1",
            aws_session_token="1",
            region_name="1")
        bluepill.default_script = script(folder_path="placebo/s3-tests" client_type="s3", session=placebo_session)

    @bluepill()
    def test_your_s3_function(self, client):
        """This test will use the default s3 client and placebo/s3-tests path."""
        result = s3_fun(cfn_client=client)
        self.assertTrue(result)

    @bluepill(folder_path='placebo/s3-tests/test2-bad-data')
    def test_your_s3_function_test2_bad_data(self, client):
        """Very useful for switching mock data paths for a specific test."""
        result = s3_fun(cfn_client=client)
        self.assertFalse(result)

    @bluepill(client_type='cloudformation', folder_path='placebo/cfn-tests')
    def test_your_cloudformation_function(self, client):
        """We want to test cloudformation here, so switch the client and the mock data location."""
        result = cfn_fun(cfn_client=client)
        self.assertTrue(result)
    
    def test_your_function_with_real_api_calls(self):
        """Disregard using the decorator if you want to run a test without mocking."""
        result = real_fun()
        self.assertTrue(result)
```
### BluePill with recording
```python
from bluepill.utils import bluepill, script
import boto3
import unittest

class test_SomeAWSFunctions(unittest.TestCase):
    """Create a default bluepill/placebo environment with recording toggled on. This is useful for gathering initial data and then remove for playback testing."""

    def setUp(self):
        """Create a default bluepill/Placebo environment."""
        placebo_session = boto3.Session(
            aws_access_key_id="1",
            aws_secret_access_key="1",
            aws_session_token="1",
            region_name="1")
        bluepill.default_script = script(folder_path="placebo/s3-tests" client_type="s3", session=placebo_session, record=True)

    @bluepill()
    def record_aws_function(self, client):
        """bluepill the method and record api calls on the default boto3 client for ListBuckets."""
        client.list_buckets()
    
    @bluepill(record=False)
    """bluepill the method and playback the response to ListBuckets."""
    def playback_aws_function(self.client):
        client.list_buckets()
```
### Use outside of unit tests
```python
from bluepill import bluepill, script
import boto3

# The script configuration for bluepill
placebo_session = boto3.Session(
    aws_access_key_id="1",
    aws_secret_access_key="1",
    aws_session_token="1",
    region_name="1")
bp_script = script(folder_path="placebo/s3-tests" client_type="s3", session=placebo_session)


@bluepill(bp_script)
def aws_function(client):
    """bluepill the function using the provided script config."""
    client.list_buckets()
```