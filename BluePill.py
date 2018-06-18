import placebo
import boto3

class BluePill(object):

    # __init__
    #
    def __init__(self, client_type=None):
        print('__init__')
        self.clientType = client_type
    
    # __call__
    #
    def __call__(self, function, *args, **kwargs):
        def wrappedFunction(*args, **kwargs):
            print('Called {fn} with args: {args} using boto3 client {client}'.format(fn=function.__name__,args=args, client=self.clientType))
            return function(*args, **kwargs)
        return wrappedFunction