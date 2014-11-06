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

    "template_cache": "location_of_cache_for_template_generation",

    "jenkins": {
        "test-instance": {
            "host": "http://localhost:8080",
            "token": "user_token",
            "jobs": [
                {
                    "organization": "your_github_org",
                    "templates": "location_of_templates",
                    "exclude": [
                        "repo1",
                        "repo2"
                    ]
                },
                {
                    "organization": "another_org",
                    "repo": "repo",
                    "templates": "location_of_repo_specific_templates"
                },
                {
                    "file": "location_of_YAML_file",
                    "templates": "location_of_repo_specific_templates"
                }
            ]
        }
    }
}
```

## Usage

#### `chamberlain list-repos [REPO1 REPO2 ...]`
show github repositories and what job templates each one is associated with, or which job templates are associated with the given repos.

**this command caches its results in `~/.chamberlain/repos.json`**

##### Flags:
- `--force-sync`, `-f` : pull repo data from github instead of referencing the cached list of repositories in `~/.chamberlain/repos.json`

#### `chamberlain generate`
generate template files from github repos.

#### `chamberlain sync [TEMPLATE_LOCATION]`
runs [Jenkins Job Builder](https://github.com/openstack-infra/jenkins-job-builder) in `TEMPLATE_LOCATION`, which defaults to `~/.chamberlain/template_cache`

## Contributing
- make your changes
- `pip install tox && tox`

**NOTE**: If you already have `singularity_runner` (via the [`singularity_dsl gem`](https://github.com/behance/singularity_dsl)) just run:

```
singularity_runner test
```

This will install `virtualenv`, bootstrap and run the above in the environment created.
