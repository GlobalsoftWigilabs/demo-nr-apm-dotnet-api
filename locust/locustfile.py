from locust import HttpUser, TaskSet, LoadTestShape, between, task
from random import randint

class CustomerTask(TaskSet):
    @task()
    def index(self):
        self.client.get("/Movies")

    @task()
    def movieDetails(self):
        id = randint(1,6)
        self.client.get(f"/Movies/Details/{id}", name="/Movies/Details")

    @task(2)
    def orders(self):
        id = randint(1,6)
        self.client.get(f"/Orders/AddItemToShoppingCart/{id}", name="/Orders")

class ActorTask(TaskSet):
    @task()
    def actors(self):
        self.client.get("/Actors")

    @task()
    def actorDetails(self):
        id = randint(1,5)
        self.client.get(f"/Actors/Details/{id}", name="/Actors/Details")

class AdminTask(TaskSet):
    @task()
    def cinemas(self):
        self.client.get("/Cinemas")


class ETicketUser(HttpUser):
    wait_time = between(2, 5)

    tasks = [
        CustomerTask,
        ActorTask,
        AdminTask
    ]

class StagesLoad(LoadTestShape):
    stages = [
        {"duration": 60*6, "users": 10, "spawn_rate": 10},
        {"duration": 60*3, "users": 50, "spawn_rate": 10},
        {"duration": 60*4, "users": 100, "spawn_rate": 10},
        {"duration": 60*5, "users": 30, "spawn_rate": 10},
        {"duration": 60*3, "users": 10, "spawn_rate": 10},
        {"duration": 60*4, "users": 5, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
    



