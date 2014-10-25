import github


class Client(object):
    def __init__(self, token, org):
        self.token = token
        self.org = org

    def repos(self):
        github.auth(self.token)
