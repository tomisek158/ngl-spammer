import os
import concurrent.futures
import requests
from colorama import Fore, Style
import random
import datetime
import threading
import time

class MessageDispatcher:
    def __init__(self, max_fails=5, pause_duration=10):
        self.sent_messages = 1
        self.failure_count = 0
        self.max_fails = max_fails
        self.pause_duration = pause_duration
        self.counter_lock = threading.Lock()

    def post_message(self, username, message_text, proxy_server):
        headers = {
            'Host': 'ngl.link',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0',
            'origin': f'https://ngl.link/{username}',
            'referer': f'https://ngl.link/{username}',
            'accept-language': 'en-US,en;q=0.9',
        }

        payload = {
            'username': username,
            'question': message_text,
            'deviceId': '0',
            'gameSlug': '',
            'referrer': '',
        }

        try:
            response = requests.post('https://ngl.link/api/submit', headers=headers, data=payload, proxies=proxy_server, timeout=10)
            if response.status_code == 200:
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                with self.counter_lock:
                    print(f"{Fore.GREEN}+ {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Send >> {Fore.RED}{username} {Fore.WHITE}at {Fore.RED}{timestamp} {Fore.WHITE}(#{self.sent_messages}){Style.RESET_ALL}")
                    self.sent_messages += 1
                self.failure_count = 0
            else:
                print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Failed to send message. Status code: {Fore.RED}{response.status_code}{Style.RESET_ALL}")
                self.increment_failure()
        except Exception as e:
            print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Error while sending message: {Fore.RED}{str(e)}{Style.RESET_ALL}")
            self.increment_failure()

    def increment_failure(self):
        self.failure_count += 1
        if self.failure_count > self.max_fails:
            print(f"{Fore.YELLOW}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Too many errors; pausing for {self.pause_duration} seconds...{Style.RESET_ALL}")
            time.sleep(self.pause_duration)
            self.failure_count = 0

    def report_statistics(self, start_time, completion_reason):
        end_time = time.time()
        total_duration = end_time - start_time
        total_sent = self.sent_messages - 1
        mps = total_sent / total_duration if total_duration > 0 else 0
        print(f"\n{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.RED}{completion_reason}{Style.RESET_ALL}")
        print(f"{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Total messages sent: {Fore.RED}{total_sent}{Style.RESET_ALL}")
        print(f"{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Duration: {Fore.RED}{total_duration:.2f} sec{Style.RESET_ALL}")
        print(f"{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Messages per second: {Fore.RED}{mps:.2f}{Style.RESET_ALL}")

def start_messaging():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(Fore.RED + """
███╗   ██╗ ██████╗ ██╗         ███████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗ 
████╗  ██║██╔════╝ ██║         ██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
██╔██╗ ██║██║  ███╗██║         ███████╗██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
██║╚██╗██║██║   ██║██║         ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
██║ ╚████║╚██████╔╝███████╗    ███████║██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═╝  ╚═══╝ ╚═════╝ ╚══════╝    ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝

by tomisek158 
    """ + Style.RESET_ALL)

    ngl_username = input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Username: {Fore.RED}")
    custom_message = input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Custom Message (leave blank to use messages from messages.txt): {Fore.RED}")

    while True:
        try:
            message_count = int(input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Message count: {Fore.RED}"))
            break
        except ValueError:
            print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Invalid input. Please enter a number.{Style.RESET_ALL}")

    while True:
        try:
            thread_num = int(input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Thread count: {Fore.RED}"))
            break
        except ValueError:
            print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Please provide a valid number for threads.{Style.RESET_ALL}")

    with open("proxies.txt", "r") as proxy_file:
        proxy_list = proxy_file.read().splitlines()

    with open("messages.txt", "r") as messages_file:
        messages = messages_file.read().splitlines()

    dispatcher = MessageDispatcher()

    try:
        start_time = time.time()
        while message_count > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_num) as executor:
                futures = []
                for proxy in proxy_list:
                    current_message = custom_message if custom_message else random.choice(messages)
                    futures.append(executor.submit(dispatcher.post_message, ngl_username, current_message, {"http": proxy, "https": proxy}))
                    message_count -= 1
                    if message_count <= 0:
                        break

                concurrent.futures.wait(futures)

        dispatcher.report_statistics(start_time, "All messages sent!")

    except KeyboardInterrupt:
        dispatcher.report_statistics(start_time, "Stopped by user.")

if __name__ == "__main__":
    start_messaging()
