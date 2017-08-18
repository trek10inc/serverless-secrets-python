import os
import re
from serverless_secrets.providers import *

class secrets(object):
    default_options = {
        'provider': 'aws',
        'regex': '^ss__',
        'trim_regex': True,
        'allow_offline': True
    }

    def __init__(self, options):
        options = options if isinstance(options, dict) else {}
        self.merged_options = dict()
        self.merged_options.update(self.default_options)
        self.merged_options.update(options)
        if os.environ.get("IS_OFFLINE") is not None and self.merged_options["allow_offline"]:
            self.merged_options["provider"] = "offline"

        provider_options = self.merged_options.get("provider_options", {})
        offline_options = self.merged_options.get("offline_options", {})

        if self.merged_options["provider"] == "aws":
            self.provider = aws(provider_options)
        elif self.merged_options["provider"] == "offline":
            self.provider = offline(offline_options)
        else:
            raise ValueError("Provider not supported: ", self.merged_options["provider"])

    def unique(self, array):
        return list(set(array))

    def loadFromEnv(self, envVarSelectionRegex=None):
        if envVarSelectionRegex is None:
            envVarSelectionRegex = self.merged_options['regex']

        regex = re.compile(envVarSelectionRegex)
        selected_env_names = list(filter(lambda x: regex.search(x), os.environ))
        parameter_names = self.unique(list(map(lambda x: os.environ[x], selected_env_names)))

        if len(parameter_names) < 1:
            return []

        data = self.provider.get_secret(parameter_names)
        missing_parameters = []

        for env_var_name in selected_env_names:
            for item in data:
                if item['Name'] == os.environ[env_var_name]:
                    new_env_var_name = regex.sub("", env_var_name) if self.merged_options['trim_regex'] else env_var_name
                    os.environ[new_env_var_name] = item['Value']

        #TODO Throw error for missing items? Need to add in the list above just being lazy
        # if len(missing_parameters) > 0:
        #     s = ", ".join(missing_parameters)
        #     raise ValueError("Secrets could not be obtained for the following env variables: ", s)


    def loadByName(self, env_var_name, parameter_name):
        item = self.provider.get_secret(parameter_name)
        if item['Name'] == os.environ[env_var_name]:
            new_env_var_name = regex.sub("", env_var_name) if self.merged_options['trim_regex'] else env_var_name
            os.environ[new_env_var_name] = item['Value']
        else:
            raise ValueError("Secret could not be obtained for env variable: ", env_var_name)
