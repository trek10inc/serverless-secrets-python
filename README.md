![serverless_secrets_logo](https://cloud.githubusercontent.com/assets/1689118/15905519/23bf2208-2d83-11e6-96fb-7dc1edd359ee.png)

*A no fuss way of getting secrets into your Serverless functions. If you're looking for the node version or the plugin information see [Serverless Secrets](https://github.com/trek10inc/serverless-secrets).*

**Problem:** The Serverless project currently offers no good way of managing secrets.
You could put them in with your environment variables, but what if you are working in a team?
You could put it in the repo, but "secrets" in a git repo is bad practice.

**Solution:** Use the EC2 System Manager Parameter Store to store your secrets,
and use magic environment variables or explicit calls in your code. That's it!

**Requires Python 2.7**

**Serverless Secrets Python is designed for use with Serverless 1.x.**

## Provider support

Currently, Serverless Secrets Python supports AWS only. However, it has been designed to support
other providers down the road. If you are interested, please feel free to send a PR.

## Project setup

### Install Serverless Secrets plugin

In the root of your Serverless project:
`npm install serverless-secrets --save` or `yarn add serverless-secrets`

Add the plugin in `serverless.yml`:
```
plugins:
  - serverless-secrets
```

### Setup Python
In the root of your Serverless project:
`npm install serverless-python-requirements --save`

Create your requirements.txt file and add serverless_secrets

## Environment variables

One way to use Serverless Secrets is to make magic environment variables, which get loaded up with the secret
value at runtime. `secrets.loadFromEnv` uses a configurable regex to find the environment variables to be
created (or replaced). The default regex is `^ss__` (that's 2 underscores). Decryption is done automatically, and
the full plaintext will be loaded into the environment variable. You may still want to do post processing on it,
particularly in the case of the files.

```
# secrets.loadByEnv loads the value of a stored secret
# named 'myParameter' into environment variable myVar
provider:
  environment:
    ss__myVar: myParameter
```

## Offline support

Coming Soon

## CLI

Provided by [Serverless Secrets](https://github.com/trek10inc/serverless-secrets).

## Code usage

*Load secrets based on environment variables*

```
// Given: a secret named 'myParameter' is stored in SSM with value 'mySecret'
// Given: an environment variable named 'ss__myVar' exists with a value of 'myParameter'

from serverless_secrets import secrets
import os

def hello(event, context):
    sec = secrets({})
    sec.loadFromEnv()
    print os.environ
```

*Load secrets explicitly into environment variables*

```
// Given: a secret named 'myParameter' is stored in SSM with value 'mySecret'

from serverless_secrets import secrets
import os

def hello(event, context):
    sec = secrets({})
    sec.loadByName('myVar', 'myParameter')
    print os.environ
```

## API

*Parameters:*
- `options` - object: The configuration object for serverless secrets. This will be merged
 over the top of the defaults
  - `provider` - string: This must be a supported provider. Default value: `'aws'`.
  Currently supported providers: aws, offline.
  - `regex` - string: String version of regex used to select `os.environ` keys for value
  replacement in `secrets.loadFromEnv`. Default value: `'^ss__'` (that's **2** underscores).
  - `trimRegex` - boolean: If set to true, the secret represented by environment variable
  `ss__myVar` will be loaded into environment variable `myVar`. If set to false, the value
  of environment variable `ss__myVar` will be replaced with the secret value.
  Default value: `true`.
  - `allow_offline` - boolean: Enables automatic switch to the offline provider when Serverless
  Offline is detected. Default value: `true`.
  - `provider_options` - object: The options object to be passed to the provider, except for the
  offline provider. This will be merged with the default provider options.
    - Default AWS provider options:
    ```
    {
        'apiVersion': '2014-11-06',
        'region': os.getenv('AWS_REGION', 'us-east-1')
    }
    ```
  - `offline_options` - object: The options object to be passed to the offline provider. This
  is separate from `provider_options` as most users will be be using offline locally but another
  provider when deploying their project. This will be merged with the default offline provider
  options.
    - `path` - string: The path to the JSON file containing offline secrets.
    Default value: `.param_store.json`.

*Returns:* `secrets` instance

### `secrets.loadFromEnv(options)`

*Parameters:*
- `options` - object: The configuration object for loadFromEnv. It is merged over the top of
 the module options (which are merged over the defaults). `regex` and `trimRegex` are relevant.
 Replacing provider related options does nothing.

*Side Effects:* Scans `os.environ` for keys that match `environmentVariableSelectionRegex`.
The corresponding values of the matched keys are requested from the secret store.
The values of the trimmed (if `trimRegex` is `true`) matched keys are then set to the
corresponding values retrieved from the secret store.

### `secrets.loadByName(environmentVariableName, parameterName)`

*Parameters:*
- `environmentVariableName` - string: name of the key to be added to `os.environ` that
will contain the retrieved secret value
- `parameterName` - string: name of the secret to be retrieved from the secret store

*Side Effects:* Retrieves `parameterName` from the secret store and loads it
into `os.environ[environmentVariableName]`

## AWS IAM

Remember to grant your lambda functions access to get parameters from SSM
in your `serverless.yml`:
```
iamRoleStatements:
  - Effect: "Allow"
    Action: "ssm:GetParameters"
    Resource: "arn:aws:ssm:${region}:${awsAccountId}:parameter/*"
```

Protip: If you have a good naming convention for your secrets, such as a prefix of 'myapp-dev',
you can limit access further by making the Resource value be
`"arn:aws:ssm:${region}:${awsAccountId}:parameter/myapp-{opt:stage}*`
