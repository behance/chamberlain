Chamberlain
====

Automated Jenkins configuration for your GitHub repos.

Libs Used:
- [github3.py](https://github.com/sigmavirus24/github3.py) to gather repo data.
- [Jenkins Job Builder](https://github.com/openstack-infra/jenkins-job-builder) to configure Jenkins.

## Installation

```
git clone git@github.com:behance/chamberlain.git
cd chamberlain
sudo python setup.py install
```

## Configuration

**lives in `~/.chamberlain/config.json`, automatically created if DNE**

```ruby
{
    "github": {
        "auth": {
            "token": "your_oauth_token"
        },
        "orgs": [
            "behance",
            "behanceops"
        ]
    },
    "jenkins": {
        "instances": [
            {
                "name": "bejankins",
                "host": "http://bejankins.dev-be-aws.net:8080",
                "token": "67a374b31117d62ba3798a11f138ba93"
            }
        ],
        "jobs": [
            {
                "instance": "bejankins",
                "owner": "behanceops",
                "templates": [
                    "branch-cookbook-{repo}",
                    "master-cookbook-{repo}"
                ],
                "exclude": [
                    "misc",
                    "deploy-jenkins",
                    "chef",
                    "yum",
                    "users",
                    "openssl",
                    "presentations",
                    "scripts"
                ]
            }
        ]
    }
}
```

## Usage

#### Universal Flags
- `--force-sync`, `-f` : pull repo data from github instead of referencing the cached list of repositories in `~/.chamberlain/github_repos.json`.

#### Universal Args
- `repos` : list of repositories to perform actions on.

**e.g.**: `chamberlain generate behance/repo1 matcher_word`

Internally, the list of repos that is generated for the commands to use will be filtered based on partial matches for `behance/repo1` and `matcher_word`

### Commands

#### `chamberlain map [REPO1 REPO2 ...]`
show github repositories and what job templates each one is associated with, or which job templates are associated with the given repos.

**this command caches its results in `~/.chamberlain/github_repos.json`**

#### `chamberlain generate [REPO1 REPO2 ...]`
Given directories with YAML templates, prepares a workspace and generates project-template YAML files in the workspace.

**WARNING: This command wipes the given directory clean**

**Flags**
```
  -t, --templates   list of directories containing templates (default: [ cwd() ]
  -w, --workspace   prepare a target template directory
```

#### `chamberlain sync [REPO1 REPO2 ...]`
Generates the workspace (using the same procedure as the `generate` command) and runs [Jenkins Job Builder](https://github.com/openstack-infra/jenkins-job-builder) in the application workspace, which defaults to `~/.chamberlain/workspace`

## Contributing
- make your changes
- `pip install tox && tox`

**NOTE**: If you already have `singularity_runner` (via the [`singularity_dsl gem`](https://github.com/behance/singularity_dsl)) just run:

```
singularity_runner test
```

This will install `virtualenv`, bootstrap and run the above in the environment created.
