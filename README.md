# BluePill :pill:
An expanded decorator class for modifying Placebo playback when unit testing with boto3 calls.

## Requirements
Python 3.6

## Installation
TODO

## Usage Examples
```python
def setUp(self):
    BluePill.SESSION = boto3.Session(
        aws_access_key_id='1',
        aws_secret_access_key='1',
        aws_session_token='1',
        region_name='none')
    BluePill.FOLDER_PATH = 'placebo/s3-tests'
    BluePill.CLIENT_TYPE = 's3'

# This test will use the default s3 client and s3-tests path
#
@BluePill()
def test_you_s3_function(self, client):
    result = s3_fun(cfn_client=client)
    self.assertTrue(result)

# We want to test cloudformation here, so switch the client and the test data location
#
@BluePill(client_type='cloudformation', folder_path='placebo/cfn-tests')
def test_your_cloudformation_function(self, client):
    result = cfn_fun(cfn_client=client)
    self.assertTrue(result)
```