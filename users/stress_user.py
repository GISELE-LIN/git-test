from locust import constant
from tasks.geoCity import geoCity
from users.user import User
from tasks.geoCity import geoCity


class StressUser(User):

    wait_time = constant(1)
    tasks = {
        geoCity: 1,
    }

    def on_start(self):
        self.login()
