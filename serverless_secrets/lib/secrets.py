import os
import re
import json
from serverless_secrets.providers import aws

class secrets(object):
    CONFIG_FILE_NAME = ".serverless-secrets.json"

    def get_storage_provider(options):
        if options["provider"] == "aws":
            return aws(provider_options)
        else:
            raise ValueError("Provider not supported: ", options["provider"])

    def __init__(self):
        config_path = os.path.join(os.getcwd(), self.CONFIG_FILE_NAME)
        with open(config_path) as config:
            self.secrets = json.load(config)

    def _unique(array):
        return list(set(array))

    def load(self, options):
        options = options if isinstance(options, dict) else {}
        merged_options = dict(self.secrets[options]) #TODO: Figure this part out
        merged_options.update(options)

        environment_secrets = dict(self.secrets[environments][$global])
        environment_secrets.update(self.secrets[environments[os.environ.get('_HANDLER').split('.')[1]]])
        parameter_names = _unique(environment_secrets.values())
        if len(parameter_names) < 1:
            return

        provider = getStorageProvider(merged_options)
        data = provider.get_secret(parameter_names)
        missing_parameters = []

        for key in data:
            if key in os.environ:
                os.environ[key] = data[key]
            else:
                missing_parameters.append(key)

        if missing_parameters.length > 0:
            message = "Secrets could not be obtained for the following environment variables: " + ", ".join(missing_parameters)
            if merged_options.logOnMissingSecret:
                print message
            if merged_options.throwOnMissingSecret:
                raise ValueError(message)


    def load_by_name(self, env_var_name, parameter_name, options):
        options = options if isinstance(options, dict) else {}
        merged_options = dict(self.secrets[options]) #TODO: Figure this part out
        merged_options.update(options)
        provider = getStorageProvider(merged_options)

        item = provider.get_secret(parameter_name)
        if item['Name'] == os.environ[env_var_name]:
            new_env_var_name = regex.sub("", env_var_name) if self.merged_options['trim_regex'] else env_var_name
            os.environ[new_env_var_name] = item['Value']
        else:
            raise ValueError("Secret could not be obtained for env variable: ", env_var_name)




# 'use strict'

# const path = require('path')
# const _ = require('lodash')
# const constants = require('../lib/constants')
#
# const secrets = require(path.join(process.cwd(), constants.CONFIG_FILE_NAME))
#
# function getStorageProvider (options) {
#   switch (options.provider) {
#     case 'aws':
#       return (require('../lib/providers/aws'))(options.providerOptions || {})
#     default:
#       throw new Error(`Provider not supported: ${options.provider}`)
#   }
# }
#
# function loadByName (envVarName, parameterName, options) {
#   const mergedOptions = Object.assign({}, secrets.options, options)
#   const provider = getStorageProvider(mergedOptions)
#   return provider.getSecret(parameterName).then(data => {
#     if (data[parameterName]) {
#       process.env[envVarName] = data[parameterName]
#     } else {
#       const message = `Secret could not be obtained for environment variable: ${envVarName}`
#       if (mergedOptions.logOnMissingSecret) console.log(message)
#       if (mergedOptions.throwOnMissingSecret) throw new Error(message)
#     }
#   })
# }
#
# module.exports = {
#   load,
#   loadByName
# }
