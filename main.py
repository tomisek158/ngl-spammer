import os
import concurrent.futures
import requests
from colorama import Fore, Style
import random
import time
import threading
import datetime

class MessageSender:
    def __init__(self):
        self.messages_sent = 0
        self.lock = threading.Lock()

    def send_message(self, username, message, proxy):
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
            'question': message,
            'deviceId': '0',
            'gameSlug': '',
            'referrer': '',
        }

        try:
            response = requests.post('https://ngl.link/api/submit', headers=headers, data=payload, proxies=proxy, timeout=1)
            if response.status_code == 200:
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                with self.lock:
                    self.messages_sent += 1
                    print(f"{Fore.GREEN}+ {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Sent >> {Fore.RED}{username} {Fore.WHITE}at {Fore.RED}{timestamp} {Fore.WHITE}(#{self.messages_sent}){Style.RESET_ALL}")
        except Exception:
            pass

    def show_stats(self, start_time):
        end_time = time.time()
        duration = end_time - start_time
        total_sent = self.messages_sent
        mps = total_sent / duration if duration > 0 else 0
        print(f"\n{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Total messages: {Fore.RED}{total_sent}{Style.RESET_ALL}")
        print(f"{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Duration: {Fore.RED}{duration:.2f} seconds{Style.RESET_ALL}")
        print(f"{Fore.RED}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Messages per second: {Fore.RED}{mps:.2f}{Style.RESET_ALL}")

def main():
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

    username = input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Username: {Fore.RED}")
    custom_message = input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Custom Message (Leave blank for random from messages.txt): {Fore.RED}")

    while True:
        try:
            msg_count = int(input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Message count: {Fore.RED}"))
            break
        except ValueError:
            print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Invalid input. Enter a number.{Style.RESET_ALL}")

    while True:
        try:
            threads = int(input(f"{Fore.RED}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Thread count: {Fore.RED}"))
            break
        except ValueError:
            print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Please enter a valid number for threads.{Style.RESET_ALL}")

    with open("proxies.txt", "r") as f:
        proxies = f.read().splitlines()

    with open("messages.txt", "r") as f:
        messages = f.read().splitlines()

    sender = MessageSender()

    try:
        start_time = time.time()
        while msg_count > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                for proxy in proxies:
                    message = custom_message if custom_message else random.choice(messages)
                    futures.append(executor.submit(sender.send_message, username, message, {"http": proxy, "https": proxy}))
                    msg_count -= 1
                    if msg_count <= 0:
                        break

                concurrent.futures.wait(futures)

        sender.show_stats(start_time)

    except KeyboardInterrupt:
        sender.show_stats(start_time)

if __name__ == "__main__":
    main()
