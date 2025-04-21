# 🔁 NGL Spammer v2.0.0

NGL Spammer for spamming users with [ngl.link](https://ngl.link) using Python

Note: Sorry, I didnt have time to make the exe file, so its not available for download at this moment But as soon as i have time, i publish it in the releases section.

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
- Fully rewritten

---

## 👥 Contributors

- **[@tomisek158](https://github.com/tomisek158)** – Owner  
  - Main creator of the project  
  - Wrote the core code and built the tool from scratch  
  - Handles updates, documentation, and overall project direction

- **@NullPlayer** – Developer
  - Focuses on fixing bugs and improving code performance  
  - Optimized the spamming system for better speed and reliability  
  - Testing


## ⚠️ Disclaimer

> For educational use only. The developer is not responsible for misuse.   

---

Made with ❤️ on 🌍
