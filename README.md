# 🔁 NGL Auto Messenger v2

NGL Spammer for spamming users with [ngl.link](https://ngl.link) using Python

---

## ⚙️ Features

- ✅ Fast message sending with threads
- 🧱 Proxy support (`proxies.txt`)
- ✉️ Random/custom messages from `messages.txt`
- 🎨 Color-coded output using `colorama`
- 📊 Stats after completion (time, messages/sec)
- 🛑 Auto pause on too many errors
- 💬 CLI prompts for username, threads, message count

---

## 📦 Requirements

- Python 3.7+
- Install dependencies:

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
requests
colorama
```


## 🚀 Usage

```bash
python main.py
```

Follow the prompts to input:
- NGL username
- Message (or leave blank to randomize)
- Number of messages
- Thread count

---

## 🆕 Changelog 2.0.0

- Replaced `async` logic with **multi-threading** for better stability
- Removed `httpx`, now using **`requests`** for simpler setup
- **Improved error handling** (auto pause after 5 fails)
- **Thread count selection**
- Fully rewritten for easier editing and running

---

## ⚠️ Disclaimer

> For educational use only. The developer is not responsible for misuse.   

---

Made with ❤️ by [tomisek158](https://github.com/tomisek158)
