import random
import string

from locust import HttpUser, task


class HabibUser(HttpUser):
    char_set = (string.ascii_uppercase + string.digits) * 20

    def generate_nonce(self):
        return ''.join(random.sample(self.char_set * 20, 20))

    @staticmethod
    def gen_message_id():
        return random.randint(0, 10 ** 6) * 2

    @task
    def get_users(self):
        data = {
            "authKey": self.auth_key,
            "messageId": self.gen_message_id(),
        }
        self.client.post("/biz/get_users", json=data)

    @task
    def get_users_with_sql_inject(self):
        data = {
            "authKey": self.auth_key,
            "messageId": self.gen_message_id(),
        }
        self.client.post("/biz/get_users_with_sql_inject", json=data)

    def on_start(self):
        message_id = self.gen_message_id()
        data = {
            "messageId": message_id,
            "nonce": self.generate_nonce(),
        }
        response = self.client.post("/auth/req_pq", json=data)
        res = response.json()
        p = int(res['p'])
        g = int(res['g'])
        client_a = random.randint(1, p - 1)
        a = pow(g, client_a, p)
        data = {
            "nonce": res["nonce"],
            "serverNonce": res["serverNonce"],
            "messageId": message_id + 2,
            "a": str(a),
        }
        response = self.client.post("/auth/req_dh_params", json=data)
        res = response.json()
        b = int(res["b"])
        auth_key = pow(b, client_a, p)
        self.auth_key = str(auth_key)
