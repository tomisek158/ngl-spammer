import os
import concurrent.futures
import requests
from colorama import Fore, Style
import random
import datetime
import threading
import time

class MessageSender:
    def __init__(self, max_errors=5, wait_time=10):
        self.message_counter = 1
        self.error_count = 0
        self.max_errors = max_errors
        self.wait_time = wait_time
        self.message_counter_lock = threading.Lock()

    def send_request(self, ngl_username, message, proxy):
        headers = {
            'Host': 'ngl.link',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0',
            'origin': f'https://ngl.link/{ngl_username}',
            'referer': f'https://ngl.link/{ngl_username}',
            'accept-language': 'en-US,en;q=0.9',
        }

        data = {
            'username': ngl_username,
            'question': message,
            'deviceId': '0',
            'gameSlug': '',
            'referrer': '',
        }

        try:
            response = requests.post('https://ngl.link/api/submit', headers=headers, data=data, proxies=proxy, timeout=10)
            if response.status_code == 200:
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                with self.message_counter_lock:
                    print(f"{Fore.GREEN}+ {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Send >> {Fore.RED}{ngl_username} {Fore.WHITE}at {Fore.RED}{timestamp} {Fore.WHITE}{self.message_counter}{Style.RESET_ALL}")
                    self.message_counter += 1
                self.error_count = 0
            else:
                print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Not Sent (Status Code: {Fore.RED}{response.status_code}{Fore.WHITE}){Style.RESET_ALL}")
                self.handle_error()
        except Exception as e:
            print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Error while sending request: {Fore.RED}{str(e)}{Style.RESET_ALL}")
            self.handle_error()

    def handle_error(self):
        self.error_count += 1
        if self.error_count > self.max_errors:
            print(f"{Fore.YELLOW}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Waiting {self.wait_time} seconds due to too many errors...{Style.RESET_ALL}")
            time.sleep(self.wait_time)
            self.error_count = 0

    def handle_stats(self, start_time, reason):
        end_time = time.time()
        total_time = end_time - start_time
        total_messages = self.message_counter - 1
        mps = total_messages / total_time if total_time > 0 else 0
        print(f"\n{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.RED}{reason}{Style.RESET_ALL}")
        print(f"{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Total messages sent: {Fore.RED}{total_messages}{Style.RESET_ALL}")
        print(f"{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Total time: {Fore.RED}{total_time:.2f} seconds{Style.RESET_ALL}")
        print(f"{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Average MPS: {Fore.RED}{mps:.2f}{Style.RESET_ALL}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(Fore.RED + """
███╗   ██╗ ██████╗ ██╗         ███████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗ 
████╗  ██║██╔════╝ ██║         ██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
██╔██╗ ██║██║  ███╗██║         ███████╗██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
██║╚██╗██║██║   ██║██║         ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
██║ ╚████║╚██████╔╝███████╗    ███████║██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═╝  ╚═══╝ ╚═════╝ ╚══════╝    ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝

by NullSquad
    """ + Style.RESET_ALL)

    ngl_username = input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}NGL Username: {Fore.RED}")
    message_input = input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}NGL Message (leave blank to use messages from messages.txt): {Fore.RED}")

    while True:
        try:
            count = int(input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}MESSAGE Count: {Fore.RED}"))
            break
        except ValueError:
            print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Please enter a valid number.{Style.RESET_ALL}")

    while True:
        try:
            thread_count = int(input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Number of Threads: {Fore.RED}"))
            break
        except ValueError:
            print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Please enter a valid number.{Style.RESET_ALL}")

    with open("proxies.txt", "r") as proxy_file:
        proxy_list = proxy_file.read().splitlines()

    with open("messages.txt", "r") as messages_file:
        messages = messages_file.read().splitlines()

    sender = MessageSender()

    try:
        start_time = time.time()
        while count > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = []
                for proxy in proxy_list:
                    current_message = message_input if message_input else random.choice(messages)
                    futures.append(executor.submit(sender.send_request, ngl_username, current_message, {"http": proxy, "https": proxy}))
                    count -= 1
                    if count <= 0:
                        break

                concurrent.futures.wait(futures)

        sender.handle_stats(start_time, "All messages sent!")

    except KeyboardInterrupt:
        sender.handle_stats(start_time, "Stopping by user...")

if __name__ == "__main__":
    main()
