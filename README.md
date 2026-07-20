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
   *(Make sure to change `YOUR_USERNAME` with your actual GitHub username)*

2. **Install required dependencies:**
   Make sure to install the required Python libraries (`requests` and `python-dotenv`).
   ```bash
   pip install requests python-dotenv
   ```

---

## ⚙️ Configuration

Before running the bot, you need to set up your environment variables. 

> **Don't have a 2Captcha API key?** [Register here](https://2captcha.com/auth/register/?from=26096332) to get one.

1. Create a new file named `.env` in the root directory of the project.
2. Open the file and add your credentials using the following format:

```env
# Your GXT Exchange Authorization Bearer Token
BEARER_TOKEN="eyJhbGciOiJFUzI1NiIs..." 

# Your 2Captcha API Key (for bypassing the slider puzzle)
TWOCAPTCHA_API_KEY="your_2captcha_api_key_here"
```

### How to get your `BEARER_TOKEN`:
1. Open [GXT Exchange](https://gxtexchange.com/) and log in to your account.
2. Press `F12` to open Developer Tools and navigate to the **Network** tab.
3. Click on the **Claim** button or navigate to the mining page.
4. Look for network requests made to `supabase.co` (e.g., `user`, `balances`, or `mining_claims`).
5. Click on the request, go to the **Headers** section, and find the `authorization` header. 
6. Copy the long string starting with `eyJ...` (exclude the word "Bearer").

---

## 🚀 Usage

Run the script using Python:

```bash
python bot.py
```

The bot will display your balance, calculate the waiting time, and sleep until it's time to execute the next claim.

---

## 🧩 About CAPTCHA Integration
GXT Exchange periodically uses a custom slider puzzle (`_puzzle_id`) to verify claims. The `solve_puzzle_with_2captcha()` function in this script serves as a **blueprint**. 

Depending on how strictly the platform enforces the CAPTCHA, you may need to manually inspect the specific API endpoints for loading and verifying the puzzle to fully automate the 2Captcha bypass.

---

## ⚠️ Disclaimer
**For Educational Purposes Only.** 
Automating claims using scripts or bots may violate the Terms of Service of GXT Exchange. The creator of this script is not responsible for any account bans, suspensions, or losses incurred while using this software. Use it strictly at your own risk.

---
