# load test habib web service

first you need create python virtual envirment

then install pip packages

```shell
pip install -r requierments.txt
```

then run locust and use ui to run test

```shell
locust
```

### results

I ran load tests with 50 users and get these results.

1. auth server:
![alt text](screenshots/auth-server.png "Title")
2. biz server:
![alt text](screenshots/biz-server.png "Title")
3. gateway server:
![alt text](screenshots/gateway-server.png "Title")