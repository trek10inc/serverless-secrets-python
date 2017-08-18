import boto3
import os

class aws(object):
    default_options = {
        'apiVersion': '2014-11-06',
        'region': os.getenv('AWS_REGION', 'us-east-1')
    }

    def __init__(self, options):
        options = options if isinstance(options, dict) else {}
        self.merged_options = dict()
        self.merged_options.update(self.default_options)
        self.merged_options.update(options)
        self.ssm = boto3.client('ssm', region_name=self.merged_options["region"], api_version=self.merged_options["apiVersion"])

    def get_secret(self, parameterNames):
        names = parameterNames if isinstance(parameterNames, list) else [parameterNames]
        response = self.ssm.get_parameters(
            Names=names,
            WithDecryption=True
        )
        return response['Parameters']

    def set_secret(self, name, value, keyId, description=None, is_encrypted=None):
        if is_encrypted is None:
            is_encrypted = True

        if description is None:
            description = 'Created with Serverless Secrets'

        secretType = 'SecureString' if isEncrypted else 'String'
        response = self.ssm.put_parameter(
            Name=name,
            Value=value,
            Description=description,
            Type=secretType,
            KeyId=keyId,
            Overwrite=True
        )
