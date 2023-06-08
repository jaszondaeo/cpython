import cloudscraper
import websocket
import requests
import base64
import json
import time
import threading
from win10toast import ToastNotifier
from websocket import create_connection
from random import randbytes, choice
from fake_useragent import UserAgent

scraper = cloudscraper.create_scraper()
auth = [
    "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"
]
proxiess = [
    "2.56.119.93:5074:xfajrghq:90ej6e3bn1qd",
    "185.199.229.156:7492:xfajrghq:90ej6e3bn1qd",
    "185.199.228.220:7300:xfajrghq:90ej6e3bn1qd",
    "185.199.231.45:8382:xfajrghq:90ej6e3bn1qd",
    "188.74.210.207:6286:xfajrghq:90ej6e3bn1qd",
    "188.74.183.10:8279:xfajrghq:90ej6e3bn1qd",
    "188.74.210.21:6100:xfajrghq:90ej6e3bn1qd",
    "45.155.68.129:8133:xfajrghq:90ej6e3bn1qd",
    "154.95.36.199:6893:xfajrghq:90ej6e3bn1qd",
    "45.94.47.66:8110:xfajrghq:90ej6e3bn1qd"
]

class Game:
    def __init__(self, info):
        self.value = sum([player["betAmount"] for player in info["players"]])
        self.time = info["timeLeft"]
        self.status = info["status"]
        self.winner = info["winner"]
        self.winningColor = info["winningColor"]
        self.id = info["_id"]

class Jackpot:
    def __init__(self, auth: list, proxies: list) -> None:
        self.auth = auth
        self.proxies = proxiess
        self.used_proxies = set()

    class _Websocket:
        def __init__(self, auth: list, proxies: list) -> None:
            self.auth = auth
            self.proxies = proxiess
            self.used_proxies = set()
            self._connection = None

        def connect(self, headers: dict = None) -> websocket.WebSocket:
            if headers is None:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Sec-WebSocket-Version": "13",
                    "Origin": "https://www.piesocket.com",
                    "Sec-WebSocket-Extensions": "permessage-deflate",
                    "Sec-WebSocket-Key": str(base64.b64encode(randbytes(16)).decode('utf-8')),
                    "Connection": "keep-alive, Upgrade",
                    "Sec-Fetch-Dest": "websocket",
                    "Sec-Fetch-Mode": "websocket",
                    "Sec-Fetch-Site": "cross-site",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "Upgrade": "websocket"
                }

            proxy = choice(self.proxies)

            # Ensure each WebSocket connection uses a different IP
            while proxy in self.used_proxies:
                proxy = choice(self.proxies)

            ip, port, login, password = proxy.split(':')

            self._connection = create_connection(
                "wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket",
                suppress_origin=True,
                header=headers,
                http_proxy_host=ip,
                http_proxy_port=int(port),
                http_proxy_auth=(login, password)
            )

            ws = self._connection
            ws.send("40/chat,")
            ws.send(f'42/chat,["auth","{self.auth}"]')

            self.used_proxies.add(proxy)

            return self._connection

        @property
        def connection(self) -> websocket.WebSocket:
            return self._connection

        def solvecaptcha(self):
            apikey = "zerolysimin-a15a342f-01c2-dc34-0ca7-9d67bc86a8eb"
            token_api = "https://token.nocaptchaai.com/token"

            headers = {"Content-Type": "application/json", "apikey": apikey}
            payload = {
                "rqdata": "eyJ0zI1NiJ9.eyJmIjowLCJ....",
                "type": "hcaptcha",
                "enterprise": True,
                "url": "https://bloxflip.com/",
                "sitekey": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
                "useragent": UserAgent().random
            }
            response = requests.post(token_api, json=payload, headers=headers).json()
            time.sleep(20)
            sts = requests.get(response["url"], headers=headers).json()
            return sts["token"]

        def join(self) -> None:
            captcha_result = self.solvecaptcha()
            self._connection.send(f'42/chat,["enter-rain",{{"captchaToken":"{captcha_result};;undefined;;scope"}}]')

        def Websocket(self):
            return self._Websocket(self.auth)

        @classmethod
        def reset_proxies(cls):
            cls.used_proxies = set()

def run_script(auth_token):
    jackpot = Jackpot(auth_token, proxiess)
    websocket = jackpot.Websocket()
    websocket.connect()
    websocket.join()
    time.sleep(15)
    info = scraper.get("https://rest-bf.blox.land/user", headers={"x-auth-token": auth_token}).json()['user']
    checker = scraper.get("https://rest-bf.blox.land/chat/history").json()['rain']['players']
    if info['robloxId'] in checker:
        print(f"Account Joined {info['robloxUsername']}")
    else:
        print(f"Account Not Joined {info['robloxUsername']}")

def show_notification(message, duration):
    toaster = ToastNotifier()

    # Show the notification
    toaster.show_toast("Rain Notification", message, duration=duration)

    # Wait for the notification to disappear
    time.sleep(duration)

    # Hide the notification
    toaster.hide_toast()

print(f"RainJoiner Is Started. Loaded {len(auth)} account(s).")
while True:
    try:
        r = scraper.get('https://rest-bf.blox.land/chat/history').json()
        check = r['rain']
        if check['active']:
            threads = []
            for token in auth:
                thread = threading.Thread(target=run_script, args=token,)
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
                time.sleep(6)
            Jackpot.reset_proxies()
        elif check['active'] == False:
                time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(5)
