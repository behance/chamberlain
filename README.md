Chamberlain
====

Automated Jenkins configuration for your GitHub repos.

Uses:
- [PyGithub](https://github.com/jacquev6/PyGithub) to gather repo data.
- [Jenkins Job Builder](https://github.com/openstack-infra/jenkins-job-builder) to configure Jenkins

## Configuration

```ruby
{
    "cache": "location_of_cache_for_template_generation",
    "jenkins": {
        "test-instance": {
            "host": "http://localhost:8080",
            "token": "user_token",
            "jobs": [
                {
                    "organization": "your_github_org",
                    "templates": "location_of_templates"
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
    },
    "github": {
        "token": "your_oauth_token"
    }
}
```

## Usage

#### `chamberlain list-repos`
- `--force-sync`, `-f`
- `--list-templates`, `-t`
