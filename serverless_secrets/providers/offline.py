import json

class offline(object):
    defaultOptions = {
        'path': '.param_store.json'
    }

    def __init__(self, options):
        options = options if isinstance(options, dict) else {}
        self.merged_options = dict()
        self.merged_options.update(self.default_options)
        self.merged_options.update(options)

    def get_secret(self, parameterNames):
        raise Error("Not implemented")
        # names = parameterNames if isinstance(parameterNames, list) else [parameterNames]
        #
        # with open(self.merged_options["path"], 'r') as f:
        #     data = json.load(f)
        #     result = reduce((lambda obj, name: obj[name] = data[name], return obj), {})
        #
        # return result


    def set_secret(self, name, value, keyId, description=None, is_encrypted=None):
        raise Error("Not implemented")
