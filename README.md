![serverless_secrets_logo](https://cloud.githubusercontent.com/assets/1689118/15905519/23bf2208-2d83-11e6-96fb-7dc1edd359ee.png)

*An opinionated tool for safely managing and deploying Serverless projects and their secrets. If you're looking for the node version or the plugin information see [Serverless Secrets](https://github.com/trek10inc/serverless-secrets)*

## Contents
- [Why](#why)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [CLI](#cli)
- [Client](#client)
- [Misc](#misc)

## Why?

**Problem:** The Serverless framework currently offers no way to manage secrets, keys, etc.
You could put them in with your environment variables, but what if you are working in a team?
You could put it in the repo, but "secrets" in a git repo is bad practice.
You could use other tools to simply encrypt with KMS, but you end up storing them in S3 or back in the repo again.
Also, none of these solutions ensures that your secrets have actually been created before deployment...

**Solution:** Serverless Secrets stores your secrets in a place designed for secrets. For AWS, this is
the EC2 Parameter Store, which supports encryption, including custom KMS keys. In addition, Serverless
Secrets offers automated validation of your secrets' presence, making your deployments that much closer
to **bulletproof (TM)**.

## Requirements

### Local requirements

Node.js 6.5 or greater for CLI.

### Client requirements

The bundled client is for Python only. For other languages, see the following table.

| Language   | Link                                                                                               |
|------------|----------------------------------------------------------------------------------------------------|
| Node.js    | [https://github.com/trek10inc/serverless-secrets](https://github.com/trek10inc/serverless-secrets) |

If you develop a client, please send us a PR to link to your client. All clients should allow for multi-provider support.
Clients need only implement the `getSecret` provider method.

### Framework requirements
Serverless Secrets 1.0.0 and greater is designed for use with Serverless 1.x.

### Provider requirements

Currently, Serverless Secrets only supports AWS. However, it has been designed with support for
other providers in mind down the road. We welcome PRs for this too.

#### AWS

The bundled client requires Python 2/3 (or greater in the future). Feel free to develop and contribute your
own clients for other languages.

### Offline support

Serverless Secrets Python does not work with [Serverless Offline](https://github.com/dherault/serverless-offline).

## Configuration

### Adding Serverless Secrets Plugin to your project

In the root of your Serverless project:
`npm install serverless-secrets --save-dev` or `yarn add serverless-secrets --dev`

Add the plugin to your `serverless.yml`:
```
plugins:
  - serverless-secrets
```

### Adding serverless_secrets to your project

In the root of your Serverless project:
`npm install serverless-python-requirements --save`

Create your requirements.txt file and add serverless_secrets

*This is only a suggestion. If your prefer an alternate method of setting up python requirements feel free to do so.*

### Environment Secrets

With a standard Serverless project, you can use the `envrionment` property to add environment variables
to individual functions as well as to all of your functions via the `provider` section. We augment this
concept by adding an `environmentSecrets` section to the provider and any function. Just like
`environment`, the properties under the `environmentSecrets` property become environment variables,
with the keys becoming the environment variable names. However, the values of the properties under
`environmentSecrets` are the names of the secrets in the secure store (e.g. Parameter Store for AWS).
Once you have set your secrets with the CLI (see below), just make sure they are all listed correctly in
`environmentSecrets`. You should not duplicate any `environmentSecrets` keys in `environment`. This is
checked during the validation step. Here's an example:

```
provider:
  environment:
    API_USER: asdf@asdf.com
  environmentSecrets:
    API_KEY: '/my-project/${opt:stage}/API_KEY'
```

After loading the secrets, `os.environ[API_KEY]` would contain the stored secret value.

### custom.serverlessSecrets section

There are a number of options avaliable to customize how Serverless Secrets operates. These should be
set under `custom.serverlessSecrets` in your `serverless.yml`. Here's an example showing that the
secrets are stored in us-west-2 and listing 2 KMS keys for use with the CLI:

```
custom:
  serverlessSecrets:
    providerOptions:
      region: us-west-2
    keys:
      default: "alias/myDefaultKey"
      anotherKey: "alias/myOtherKey"
```

#### options

The following options apply to both the custom section *and the client methods*. The custom section
values will be deployed to your functions and become the default values for the client methods.

- `throwOnMissingSecret` - boolean: If set to true, an error will be thrown if any secret
is unable to be retrieved. Default value: `false`.
- `logOnMissingSecret` - boolean: If set to true, an message will be logged if any secret
is unable to be retrieved. Default value: `true`.
- `providerOptions` - object: The options object to be passed to the CLI/client provider. This will
*overwrite* the default provider options.
  - Default AWS provider options:
  ```
  {
    apiVersion: '2014-11-06',
    region: os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
  }
  ```

The following options apply only to the custom section as they are only used in deploy/package CLI
operations:

- `skipValidation` - boolean: If set to true, validation of the existence of your secrets in
your provider's secret store will not be performed during deployment/packaging operations.
Default value: `false`.
- `omitPermissions` - boolean: If set to true, permissions will not automatically be added
to your functions' IAM roles to allow them access to secrets. In that case, you will need to add
those permissions manually. Default value: `false`.
  - AWS: This grants permission to the `ssm:GetParameters` action.
- `resourceForIamRole` - string | [string]: This is the string or array of strings that become the
value of `Resource` in the IAM role that grants the `ssm:GetParameters` action. This does nothing
if `omitPermissions` is true. Default value: '*'.

## CLI

Provided by [Serverless Secrets](https://github.com/trek10inc/serverless-secrets/tree/rewrite#cli).

### Processing during packaging

Serverless Secrets performs a good amount of its magic during any operation that include packaging of
your project. Let's cover those steps:
1. All configuration data is written to a JSON file called `.serverless-secrets.json`.
Note: while it does not contain any secret data, you probably still ought to add this to your `.gitignore`
(or other VCS exclusion config).
2. `.serverless-secrets.json` is added to your package
3. All of your `environmentSecrets` are converted intact to regular environment variables. This is *strictly*
for documentation purposes. We find it helpful to be able to see in the provider's console that the secret
variables exist, even if the values are only the lookup keys. If you remove or change these values, it will
have no effect.
4. Permissions to access the secret store are injected into roles.
5. Secret validation is performed. For details on this process, see the `serverless secrets validate` CLI command.
It is worth noting that failure to validate still throws an error which makes this useful as part of any good CI
process.

## Client

The client can automatically load all of your secrets into environment variables, or you can choose to load
them individually. Decryption is done automatically, meaning that the full plaintext will be loaded into the
environment variable. You may still want to do post processing on it, particularly in the case of the files.

### `secrets.load(options)`

*Parameters:*
- `options` - object: The options object as described in the `custom.serverlessSecrets` section above.
It is merged over the top of the `custom.serverlessSecrets` configuration.

*Returns:* None

*Side effects:* Uses generated configuration to determine the environment variables to be filled
and the keys to request from the secret store to fill those variables. After the secret store
responds, the environment variables are then set to the corresponding returned secrets.

*Sample code:*
```
// Given: a secret named '/my-project/dev/api-key' is stored in SSM with value 'mySecret'
// Given: an environmentSecret named 'API_KEY' exists with a value of '/my-project/dev/api-key'

from serverless_secrets import secrets
import os

def handler(event, context):
    options = {}
    secrets.load(options)
    # os.environ[API_KEY] now contains 'mySecret'
```

### `client.load_by_name(environmentVariableName, parameterName, options)`

*Parameters:*
- `environmentVariableName` - string: name of the key to be added to `os.environ` that
will contain the retrieved secret value
- `parameterName` - string: name of the secret to be retrieved from the secret store
- `options` - object: The options object as described in the `custom.serverlessSecrets` section above.
It is merged over the top of the `custom.serverlessSecrets` configuration.

*Returns:* Promise

*Side effects:* Retrieves `parameterName` from the secret store and loads it into `os.environ[environmentVariableName]`

*Sample code:*
```
// Given: a secret named '/my-project/dev/api-key' is stored in SSM with value 'mySecret'

from serverless_secrets import secrets
import os

def handler(event, context):
    options = {}
    secrets.load_by_name("API_KEY", "/my-project/dev/api-key", options)
    # os.environ[API_KEY] now contains 'mySecret'
```

## Misc

### AWS IAM

If you disable automatic permission injection, remember to grant your lambda functions
access to get parameters from SSM
in your `serverless.yml`. Example:

```
provider:
  iamRoleStatements:
    - Effect: "Allow"
      Action: "ssm:GetParameters"
      Resource: "arn:aws:ssm:${region}:${awsAccountId}:parameter/*"
```

## Future feature ideas

- Clone secrets from one region to another
