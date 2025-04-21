import os
import asyncio
import httpx
from colorama import Fore, Style
import random
import time
import datetime

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/89.0"
]

class MessageSender:
    def __init__(self):
        self.messages_sent = 0
        self.error_count = 0
        self.lock = asyncio.Lock()
        self.dead_proxies = set()

    async def test_proxy(self, proxy):
        timeout = 3
        test_url = "https://www.google.com"
        try:
            async with httpx.AsyncClient(proxies={"http://": proxy, "https://": proxy}, timeout=timeout) as client:
                response = await client.get(test_url)
                return response.status_code == 200
        except Exception:
            return False

    async def send_message(self, username, message, proxy, max_retries=2):
        timeout = 5
        if proxy in self.dead_proxies:
            async with self.lock:
                self.error_count += 1
            print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Not sent: Skipping dead proxy {proxy}{Style.RESET_ALL}")
            return False
        user_agent = random.choice(USER_AGENTS)
        headers = {
            'Host': 'ngl.link',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': user_agent,
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
        retries = 0
        while retries <= max_retries:
            try:
                async with httpx.AsyncClient(proxies={"http://": proxy, "https://": proxy}, timeout=timeout) as client:
                    response = await client.post('https://ngl.link/api/submit', headers=headers, data=payload)
                    if response.status_code == 200:
                        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                        async with self.lock:
                            self.messages_sent += 1
                            self.error_count = 0
                            print(f"{Fore.GREEN}+ {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Sent >> {Fore.RED}{message} {Fore.WHITE}to {Fore.RED}{username} {Fore.WHITE}at {Fore.RED}{timestamp} {Fore.WHITE}(#{self.messages_sent}){Style.RESET_ALL}")
                        return True
                    else:
                        retries += 1
                        if retries > max_retries:
                            async with self.lock:
                                self.error_count += 1
                                print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Failed to send to {username} via {proxy} (status {response.status_code}){Style.RESET_ALL}")
                            self.dead_proxies.add(proxy)
                            return False
                        else:
                            await asyncio.sleep(1)
            except Exception as e:
                retries += 1
                if retries > max_retries:
                    async with self.lock:
                        self.error_count += 1
                        print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Failed to send to {username} via {proxy} (error: {e}){Style.RESET_ALL}")
                    self.dead_proxies.add(proxy)
                    return False
                else:
                    await asyncio.sleep(1)
        return False

    async def show_stats(self, start_time):
        elapsed = time.time() - start_time
        print(f"{Fore.CYAN}\nSummary: {self.messages_sent} sent, {self.error_count} errors in {elapsed:.2f} seconds{Style.RESET_ALL}")

async def main():
    print(f"{Fore.CYAN}NGL Sender - Mass anonymous message sender{Style.RESET_ALL}")
    username = input(f"{Fore.YELLOW}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Enter NGL username: {Style.RESET_ALL}").strip()
    if not username:
        print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Username is required!{Style.RESET_ALL}")
        return
    try:
        msg_count = int(input(f"{Fore.YELLOW}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}How many messages to send? {Style.RESET_ALL}"))
        if msg_count <= 0:
            print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Message count must be positive!{Style.RESET_ALL}")
            return
    except ValueError:
        print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Invalid input. Enter a number.{Style.RESET_ALL}")
        return
    custom_message = input(f"{Fore.YELLOW}? {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Enter message (leave empty to use messages.txt): {Style.RESET_ALL}").strip()
    try:
        with open("proxies.txt", "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        def fix_proxy(proxy):
            if not proxy.startswith("http://") and not proxy.startswith("https://"):
                return "http://" + proxy
            return proxy
        proxies = [fix_proxy(proxy) for proxy in proxies]
        if len(proxies) > 10:
            print(f"{Fore.YELLOW}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Using only first 10 proxies out of {len(proxies)} found.{Style.RESET_ALL}")
            proxies = proxies[:10]
    except FileNotFoundError:
        print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Missing proxies.txt!{Style.RESET_ALL}")
        return
    try:
        with open("messages.txt", "r") as f:
            messages = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Missing messages.txt!{Style.RESET_ALL}")
        return
    if not proxies:
        print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}No proxies loaded!{Style.RESET_ALL}")
        return
    if not messages and not custom_message:
        print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}No messages loaded and no custom message provided!{Style.RESET_ALL}")
        return
    sender = MessageSender()
    print(f"{Fore.BLUE}* {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Testing proxies...{Style.RESET_ALL}")
    working_proxies = []
    for i, proxy in enumerate(proxies):
        print(f"{Fore.BLUE}  - {Fore.WHITE}Testing proxy {i+1}/{len(proxies)}: {proxy}{Style.RESET_ALL}", end="\r")
        is_working = await sender.test_proxy(proxy)
        if is_working:
            working_proxies.append(proxy)
            print(f"{Fore.GREEN}  + {Fore.WHITE}Working proxy: {proxy}        {Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}  - {Fore.WHITE}Failed proxy: {proxy}        {Style.RESET_ALL}")
    if not working_proxies:
        print(f"{Fore.RED}- {Fore.LIGHTBLACK_EX}| {Fore.WHITE}No working proxies found!{Style.RESET_ALL}")
        return
    print(f"{Fore.GREEN}* {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Found {len(working_proxies)}/{len(proxies)} working proxies.{Style.RESET_ALL}")
    proxies = working_proxies
    concurrency = 3
    print(f"{Fore.BLUE}* {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Using concurrency: {concurrency} requests per proxy{Style.RESET_ALL}")
    semaphores = {proxy: asyncio.Semaphore(concurrency) for proxy in proxies}
    tasks = []
    print(f"{Fore.GREEN}* {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Starting to send messages...{Style.RESET_ALL}")
    start_time = time.time()
    for i in range(msg_count):
        proxy = proxies[i % len(proxies)]
        message = custom_message if custom_message else random.choice(messages)
        async def sem_task(sender=sender, username=username, message=message, proxy=proxy):
            async with semaphores[proxy]:
                await sender.send_message(username, message, proxy)
        tasks.append(sem_task())
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}! {Fore.LIGHTBLACK_EX}| {Fore.WHITE}Interrupted by user. Stopping...{Style.RESET_ALL}")
    await sender.show_stats(start_time)
    print(f"{Fore.GREEN}\nProgram completed. Press Enter to exit...{Style.RESET_ALL}")
    input()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}\nProgram terminated by user.{Style.RESET_ALL}")