from distutils.core import setup

version = '0.2.3'

setup(
  name = 'serverless_secrets',
  packages = ['serverless_secrets'],
  version = version,
  description = 'A library for accessing secrets for use in serverless applications',
  author = 'Trek10',
  author_email = 'kwinner@trek10.com',
  url = 'https://github.com/trek10inc/serverless-secrets-python',
  download_url = 'https://github.com/trek10inc/serverless-secrets-python/archive/' + version + '.tar.gz',
  keywords = ['serverless', 'secrets'],
  classifiers = [],
  include_package_data=True,
  install_requires=[
    'boto3'
  ],
)
