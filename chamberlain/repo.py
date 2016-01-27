def repo_hash(repo):
    return {
        "id": repo.id,
        "full_name": repo.full_name,
        "owner": repo.owner.login,
        "name": repo.name,
        "ssh_url": repo.ssh_url,
        "private": repo.private,
        "fork": repo.fork,
        "html_url": repo.html_url
    }
