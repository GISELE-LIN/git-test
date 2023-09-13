from locust import TaskSet, task
from faker import Faker

# GET /api/v1/geoCity?ip=<ipv4>
class geoCity(TaskSet):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.api_version = "/api/v1"
        self.group = "geoCity"


    @task(1)
    def get_geocity(self):
        faker = Faker()
        ip_addr = faker.ipv4()

        self.client.get(
            f"{self.api_version}/{self.group}?ip={ip_addr}",
            headers=self.user.api_headers,
        )
