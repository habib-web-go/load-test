import random
import string
import time
from typing import Any, Callable

import grpc
import grpc.experimental.gevent as grpc_gevent
from grpc_interceptor import ClientInterceptor
from locust import User, task, HttpUser
from locust.exception import LocustError

from protos import authpb_pb2_grpc, authpb_pb2, sqlpb_pb2_grpc, sqlpb_pb2

grpc_gevent.init_gevent()
char_set = (string.ascii_uppercase + string.digits) * 20


def generate_nonce():
    return ''.join(random.sample(char_set * 20, 20))


def gen_message_id():
    return random.randint(0, 10 ** 6) * 2


class LocustInterceptor(ClientInterceptor):
    def __init__(self, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.env = environment

    def intercept(
            self,
            method: Callable,
            request_or_iterator: Any,
            call_details: grpc.ClientCallDetails,
    ):
        response = None
        exception = None
        start_perf_counter = time.perf_counter()
        response_length = 0
        try:
            response = method(request_or_iterator, call_details)
            response_length = response.result().ByteSize()
        except grpc.RpcError as e:
            exception = e

        self.env.events.request.fire(
            request_type="grpc",
            name=call_details.method,
            response_time=(time.perf_counter() - start_perf_counter) * 1000,
            response_length=response_length,
            response=response,
            context=None,
            exception=exception,
        )
        return response


class GrpcUser(User):
    abstract = True
    stub_class = None

    def __init__(self, environment):
        super().__init__(environment)
        for attr_value, attr_name in ((self.host, "host"), (self.stub_class, "stub_class")):
            if attr_value is None:
                raise LocustError(f"You must specify the {attr_name}.")

        self._channel = grpc.insecure_channel(self.host)
        interceptor = LocustInterceptor(environment=environment)
        self._channel = grpc.intercept_channel(self._channel, interceptor)

        self.stub = self.stub_class(self._channel)


class AuthUser(GrpcUser):
    host = "localhost:5052"
    stub_class = authpb_pb2_grpc.AuthServiceStub

    @task
    def get_auth_key(self):
        message_id = gen_message_id()
        response: authpb_pb2.ReqPQResponse = self.stub.reqPQ(
            authpb_pb2.ReqPQRequest(
                nonce=generate_nonce(),
                messageId=message_id,
            )
        )
        p = int(response.p)
        g = int(response.g)
        client_a = random.randint(1, p - 1)
        a = pow(g, client_a, p)
        self.stub.reqDHParams(
            authpb_pb2.reqDHParamsRequest(
                nonce=response.nonce,
                serverNonce=response.serverNonce,
                messageId=message_id + 2,
                a=str(a)
            )
        )


class BizUser(GrpcUser):
    host = "localhost:5062"
    stub_class = sqlpb_pb2_grpc.SQLServiceStub

    @task
    def get_users(self):
        message_id = gen_message_id()
        self.stub.getUsers(
            sqlpb_pb2.GetUsersRequest(
                messageId=message_id,
                authKey=self.auth_key,
            )
        )

    @task
    def get_users_with_sql_inject(self):
        message_id = gen_message_id()
        self.stub.getUsersWithSqlInject(
            sqlpb_pb2.GetUsersWithSqlInjectRequest(
                messageId=message_id,
                authKey=self.auth_key,
            )
        )

    def on_start(self):
        with grpc.insecure_channel('localhost:5052') as channel:
            stub = authpb_pb2_grpc.AuthServiceStub(channel)
            message_id = gen_message_id()
            response: authpb_pb2.ReqPQResponse = stub.reqPQ(
                authpb_pb2.ReqPQRequest(
                    nonce=generate_nonce(),
                    messageId=message_id,
                )
            )
            p = int(response.p)
            g = int(response.g)
            client_a = random.randint(1, p - 1)
            a = pow(g, client_a, p)
            response: authpb_pb2.reqDHParamsResponse = stub.reqDHParams(
                authpb_pb2.reqDHParamsRequest(
                    nonce=response.nonce,
                    serverNonce=response.serverNonce,
                    messageId=message_id + 2,
                    a=str(a)
                )
            )
            b = int(response.b)
            auth_key = pow(b, client_a, p)
            self.auth_key = str(auth_key)


class GatewayUser(HttpUser):
    @task
    def get_users(self):
        data = {
            "authKey": self.auth_key,
            "messageId": gen_message_id(),
        }
        self.client.post("/biz/get_users", json=data)

    @task
    def get_users_with_sql_inject(self):
        data = {
            "authKey": self.auth_key,
            "messageId": gen_message_id(),
        }
        self.client.post("/biz/get_users_with_sql_inject", json=data)

    def on_start(self):
        message_id = gen_message_id()
        data = {
            "messageId": message_id,
            "nonce": generate_nonce(),
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
