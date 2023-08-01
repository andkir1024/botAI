from commonData import mainConst, user


class userDB:
    def __init__(self, isModel):
        self.isModel = isModel
        return
    def getUserInfo(self, id):
        if mainConst.DB_TEST:
            return self.getTestUserInfo(id)
        return None
    def getTestUserInfo(self, id):
        if id == 1335723885:
            return user()
        return None    