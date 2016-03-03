import yaml
from copy import copy


def generate_project(params, jobs):
    project = copy(params)
    project["jobs"] = jobs
    return yaml.safe_dump([{"project": project}],
                          encoding='utf-8',
                          allow_unicode=True)


def template_name(repo):
    return "project-%s.yml" % repo.replace("/", "_")
