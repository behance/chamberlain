import subprocess
import re


def clone(url, dest):
    subprocess.call(["git clone %s %s" % (url, dest)], shell=True)


def remote_url(remote):
    remote_cmd = "git remote -v|grep %s|cut -s -f2|cut -d' ' -f1|uniq"
    return subprocess.check_output(remote_cmd % remote, shell=True)


def name_from_url(url):
    return re.sub(r".git$", "", url.split(":", 1)[-1]).strip()


def name_from_local_remote(remote):
    return name_from_url(remote_url(remote))
