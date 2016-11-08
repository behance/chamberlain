def repo_hash(repo):
    return {
        "id": repo.id,
        "full_name": repo.full_name.lower(),
        "owner": repo.owner.login.lower(),
        "name": repo.name.lower(),
        "ssh_url": repo.ssh_url,
        "private": repo.private,
        "fork": repo.fork,
        "html_url": repo.html_url
    }
