class order:
    def __init__(self, id = -1):
        self.id = str(id)

    def order(self, user_id):
        date = str(int(round(time.time() * 1000)))
        succes = sql.input("INSERT INTO `order` (`id`, `user_id`, `date`) VALUES (NULL, %s, %s)", \
        (0, user_id, date))
        if not succes:
            return [False, "data input error", 500]
        res = sql.get("SELECT `id`  FROM `order` WHERE `user_id` = %s AND `date` = %s", (user_id, date))
        if len(res) > 0:
            self.id = str(res[0][0])
            return [True, {"order_id": self.id}, None]
        return [False, "data read error", 500]
