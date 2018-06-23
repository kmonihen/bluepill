**build:**[![Build Status](https://circleci.com/gh/kmonihen/BluePill.svg?style=svg)](https://circleci.com/gh/kmonihen/BluePill)
# BluePill :pill:
An expanded decorator class for modifying Placebo playback when unit testing with boto3 calls.

## Requirements
Python 3.6

## Installation
TODO

## Usage Examples
### BluePill with playback
```python
from bluepill import *
import boto3
import unittest

class test_SomeAWSFunctions(unittest.TestCase):

    # Create a default BluePill/Placebo environment
    #
    def setUp(self):
        BluePill.SESSION = boto3.Session(
            aws_access_key_id='1',
            aws_secret_access_key='1',
            aws_session_token='1',
            region_name='none')
        BluePill.FOLDER_PATH = 'placebo/s3-tests'
        BluePill.CLIENT_TYPE = 's3'

    # This test will use the default s3 client and placebo/s3-tests path
    #
    @BluePill()
    def test_your_s3_function(self, client):
        result = s3_fun(cfn_client=client)
        self.assertTrue(result)

    # Very useful for switching mock data paths for a specific test
    #
    @BluePill(folder_path='placebo/s3-tests/test2-bad-data')
    def test_your_s3_function_test2_bad_data(self, client):
        result = s3_fun(cfn_client=client)
        self.assertFalse(result)

    # We want to test cloudformation here, so switch the client and the mock data location
    #
    @BluePill(client_type='cloudformation', folder_path='placebo/cfn-tests')
    def test_your_cloudformation_function(self, client):
        result = cfn_fun(cfn_client=client)
        self.assertTrue(result)
    
    # Disregard using the decorator if you want to run a test without mocking
    #
    def test_your_function_with_real_api_calls(self):
        result = real_fun()
        self.assertTrue(result)
```
### BluePill with recording
```python
from bluepill import *
import boto3
import unittest

class test_SomeAWSFunctions(unittest.TestCase):

    # Create a default BluePill/Placebo environment with recording toggled on.
    # This is useful for gathering initial data and then remove for playback testing.
    #
    def setUp(self):
        BluePill.RECORD = True
        BluePill.SESSION = boto3.Session(
            aws_access_key_id='1',
            aws_secret_access_key='1',
            aws_session_token='1',
            region_name='none')
        BluePill.FOLDER_PATH = 'placebo/s3-tests'
        BluePill.CLIENT_TYPE = 's3'

    # BluePill the method and record api calls on the default boto3 client for ListBuckets
    #
    @BluePill()
    def record_aws_function(self, client):
        client.list_buckets()
    
    # BluePill the method and playback the response to ListBuckets
    #
    @BluePill(record=False)
    def playback_aws_function(self.client):
        client.list_buckets()
```
### Use outside of unit tests
```python
from bluepill import *
import boto3

# Build default args for BluePill
#
BluePill.SESSION = boto3.Session(
    aws_access_key_id='1',
    aws_secret_access_key='1',
    aws_session_token='1',
    region_name='none')
BluePill.FOLDER_PATH = 'placebo/s3-tests'
BluePill.CLIENT_TYPE = 's3'

# BluePill the function using the default args
#
@BluePill()
def aws_function(client):
    client.list_buckets()
```