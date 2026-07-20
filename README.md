# GXT Exchange Auto Claim Bot 🚀

An automated Python script to seamlessly claim mining rewards on GXT Exchange. The bot monitors your GXT balance, calculates the exact time for the next claim based on server data, and automatically executes the claim request.

**Note:** This script includes a foundational structure for integrating [2Captcha](https://2captcha.com/auth/register/?from=26096332) to bypass slider puzzles, which can be further customized based on the specific CAPTCHA endpoints.

---

## ✨ Features
- **Auto Balance Check:** Fetches and displays your real-time GXT balance.
- **Smart Countdown Timer:** Automatically calculates the remaining time until the next claim by reading server data.
- **Headless Execution:** Runs continuously in the background and claims exactly when the timer hits zero.
- **Secure Credentials:** Uses a `.env` file to securely store your Bearer Token and API keys.
- **2Captcha Ready:** Built-in template structure to handle custom slider CAPTCHA bypass.

---

## 📋 Prerequisites
- Python 3.7 or higher installed on your system.
- A registered account on GXT Exchange.
- A [2Captcha Account](https://2captcha.com/auth/register/?from=26096332) (Required if the platform strictly enforces the slider puzzle).

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DropsterMind/GXTmining-BOT.git
   cd GXTmining-BOT
   ```

2. **Install required dependencies:**
   Make sure to install the required Python libraries (`requests` and `python-dotenv`).
   ```bash
   pip install requests python-dotenv
   or
   pip3 install requests python-dotenv
   ```

---

## ⚙️ Configuration

Before running the bot, you need to set up your environment variables. 

> **Don't have a 2Captcha API key?** [Register here](https://2captcha.com/auth/register/?from=26096332) to get one.

1. Create a new file named `.env` in the root directory of the project.
2. Open the file and add your credentials using the following format:

```env
# Your GXT Exchange Tokens
BEARER_TOKEN="eyJhbGciOiJFUzI1NiIs..." 
REFRESH_TOKEN="your_refresh_token_here"

# Your 2Captcha API Key (for bypassing the slider puzzle)
TWOCAPTCHA_API_KEY="your_2captcha_api_key_here"
```

### How to get your `BEARER_TOKEN` and `REFRESH_TOKEN`:
1. Open [GXT Exchange](https://gxtexchange.com/auth?ref=16A2D55A) and log in to your account.
2. Press **F12** to open Developer Tools.
3. Go to the **Application** tab (If you don't see it, click the >> icon next to Network/Console)
4. On the left sidebar, expand **Local Storage**.
5. Look for a key named `sb-eoerppzmsxhgmrcxrika-auth-token` and click on it.. 
6. You will see JSON data similar to:

```json
{
  "access_token": "...",
  "refresh_token": "..."
}
```

Copy:

- `access_token` → Use as your `BEARER_TOKEN`
- `refresh_token` → Use as your `REFRESH_TOKEN`
---

# 🚀 Usage

Run the bot with:

```bash
python bot.py
or
pytohon3 bot.py
```

The bot will:

- Check your current GXT balance.
- Calculate the remaining time until the next claim.
- Sleep until the claim becomes available.
- Automatically refresh expired sessions using the `REFRESH_TOKEN`.
- Update your `.env` file with the latest tokens when necessary.

---

# 🧩 CAPTCHA Integration

GXT Exchange may occasionally require users to solve a custom slider puzzle (`_puzzle_id`) before allowing a claim.

This project includes a template function:

```python
solve_puzzle_with_2captcha()
```

which serves as a starting point for integrating **2Captcha**.

Depending on future updates to GXT Exchange, you may need to inspect the puzzle-related API endpoints and adjust the implementation accordingly.

---

# ⚠️ Disclaimer

> **For Educational Purposes Only**
>
> Automating claims using scripts or bots may violate the Terms of Service of GXT Exchange.
>
> The creator of this project is **not responsible** for any account bans, suspensions, financial losses, or other consequences resulting from the use of this software.
>
> **Use this project entirely at your own risk.**
