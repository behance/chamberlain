import yaml


def generate_project(params, jobs):
    project = {param: val for (param, val) in params.iteritems()}
    project["jobs"] = jobs
    return yaml.safe_dump([{"project": project}],
                          encoding='utf-8',
                          allow_unicode=True)


def template_name(repo):
    return "project-%s.yml" % repo.replace("/", "_")
