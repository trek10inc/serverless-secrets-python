from setuptools import setup, find_packages

version = '0.2.4'

setup(
  name = 'serverless_secrets',
  packages = find_packages(),
  version = version,
  description = 'A library for accessing secrets for use in serverless applications',
  author = 'Trek10, Inc',
  author_email = 'package-management@trek10.com',
  url = 'https://github.com/trek10inc/serverless-secrets-python',
  download_url = 'https://github.com/trek10inc/serverless-secrets-python/archive/' + version + '.tar.gz',
  keywords = ['serverless', 'secrets'],
  classifiers = [],
  include_package_data=True,
  install_requires=[
    'boto3'
  ],
)
