import os
import requests
import time
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv, set_key

# Load konfigurasi dari file .env
ENV_FILE = ".env"
load_dotenv(ENV_FILE)

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
TWOCAPTCHA_API_KEY = os.getenv("TWOCAPTCHA_API_KEY")

SUPABASE_API_KEY = "sb_publishable_j-w0ixQxY1i505RyOrepyQ_9KosAIBA"
BASE_URL = "https://eoerppzmsxhgmrcxrika.supabase.co"
GXT_API_URL = "https://gxtexchange.com/api"

# Headers default
def get_headers():
    return {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.8",
        "apikey": SUPABASE_API_KEY,
        "authorization": f"Bearer {BEARER_TOKEN}",
        "content-type": "application/json",
        "origin": "https://gxtexchange.com",
        "referer": "https://gxtexchange.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "x-client-info": "supabase-js/2.108.2; runtime=web"
    }

def refresh_access_token():
    global BEARER_TOKEN, REFRESH_TOKEN
    print("[*] Token expired. Mencoba mendapatkan token baru dengan Refresh Token...")
    
    url = f"{BASE_URL}/auth/v1/token?grant_type=refresh_token"
    payload = {"refresh_token": REFRESH_TOKEN}
    headers = {
        "apikey": SUPABASE_API_KEY,
        "content-type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            
            # Update variabel global dengan token baru
            BEARER_TOKEN = data.get("access_token")
            REFRESH_TOKEN = data.get("refresh_token")
            
            # Simpan token baru ke file .env agar aman jika bot direstart
            set_key(ENV_FILE, "BEARER_TOKEN", BEARER_TOKEN)
            set_key(ENV_FILE, "REFRESH_TOKEN", REFRESH_TOKEN)
            
            print("[+] Berhasil me-refresh token! Melanjutkan tugas...")
            return True
        else:
            print(f"[-] Gagal me-refresh token. Error: {response.text}")
            print("[-] Solusi: Silakan ambil REFRESH_TOKEN baru dari browser dan update file .env.")
            return False
    except Exception as e:
        print(f"[-] Error saat refresh token: {e}")
        return False

def get_balance():
    print("[*] Mengecek saldo...")
    url = f"{BASE_URL}/rest/v1/balances?select=asset%2Camount"
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            for item in response.json():
                if item['asset'] == 'GXT':
                    print(f"[+] Saldo GXT saat ini: {item['amount']}")
                    return item['amount']
        elif response.status_code == 401:
            # Token mati, jalankan fungsi refresh
            if refresh_access_token():
                # Jika sukses refresh, coba cek saldo lagi (rekursif)
                return get_balance()
            else:
                exit() # Hentikan bot jika refresh gagal total
        else:
            print(f"[-] Gagal mengambil saldo: {response.status_code}")
    except Exception as e:
        print(f"[-] Error: {e}")

def get_next_claim_time():
    url = f"{BASE_URL}/rest/v1/mining_claims?select=id%2Camount%2Crate_per_hour%2Chours_credited%2Cclaimed_at%2Cnext_claim_at&order=claimed_at.desc&limit=1"
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                next_claim_str = data[0]['next_claim_at']
                clean_time_str = next_claim_str[:19]
                return datetime.strptime(clean_time_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        return None
    except Exception as e:
        print(f"[-] Error mengambil jadwal claim: {e}")
        return None

def solve_puzzle_with_2captcha():
    print("[!] Modul bypass Captcha disiapkan. Menggunakan ID statis sementara.")
    # ID statis untuk bypass (Perlu diupdate sesuai alur 2Captcha nanti)
    return "53794aa7-c89c-464a-b1a7-dea5a5e716a4" 

def do_claim():
    print("[*] Menyiapkan eksekusi claim...")
    puzzle_id = solve_puzzle_with_2captcha()
    
    claim_url = f"{BASE_URL}/rest/v1/rpc/claim_mining_v1"
    payload = {
        "_idempotency_key": str(uuid.uuid4()),
        "_puzzle_id": puzzle_id
    }
    
    try:
        response = requests.post(claim_url, headers=get_headers(), json=payload)
        
        if response.status_code in [200, 201]:
            data = response.json()
            if data.get("ok"):
                print(f"[+] BERHASIL CLAIM! Mendapatkan: {data.get('reward')} GXT")
            else:
                print(f"[-] Respons claim OK false: {data}")
        elif response.status_code == 401:
            if refresh_access_token():
                do_claim() # Ulangi claim dengan token baru
        else:
            print(f"[-] Gagal claim (HTTP {response.status_code}): {response.text}")
    except Exception as e:
        print(f"[-] Error saat claim: {e}")

def main():
    print("==============================")
    print("    AUTO CLAIM GXT BOT        ")
    print("==============================\n")
    
    if not REFRESH_TOKEN:
        print("[-] ERROR: REFRESH_TOKEN tidak ditemukan di file .env!")
        return

    while True:
        get_balance()
        next_time = get_next_claim_time()
        
        if next_time:
            now = datetime.now(timezone.utc)
            if now >= next_time:
                print("[!] Waktu claim telah tiba, mengeksekusi...")
                do_claim()
                time.sleep(15) 
            else:
                seconds_left = (next_time - now).total_seconds()
                minutes = int(seconds_left // 60)
                print(f"[*] Menunggu {minutes} menit ({int(seconds_left)} detik) lagi...")
                time.sleep(seconds_left + 2) 
        else:
            print("[-] Tidak ada data jadwal. Coba ulang dalam 60 detik...")
            time.sleep(60)

if __name__ == "__main__":
    main()
