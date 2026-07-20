import os
import requests
import time
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load konfigurasi dari file .env
load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
TWOCAPTCHA_API_KEY = os.getenv("TWOCAPTCHA_API_KEY")
SUPABASE_API_KEY = "sb_publishable_j-w0ixQxY1i505RyOrepyQ_9KosAIBA"

BASE_URL = "https://eoerppzmsxhgmrcxrika.supabase.co"
GXT_API_URL = "https://gxtexchange.com/api"

HEADERS = {
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

def get_balance():
    print("[*] Mengecek saldo...")
    url = f"{BASE_URL}/rest/v1/balances?select=asset%2Camount"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            for item in response.json():
                if item['asset'] == 'GXT':
                    print(f"[+] Saldo GXT saat ini: {item['amount']}")
                    return item['amount']
        else:
            print(f"[-] Gagal mengambil saldo: {response.status_code}")
    except Exception as e:
        print(f"[-] Error: {e}")

def get_next_claim_time():
    url = f"{BASE_URL}/rest/v1/mining_claims?select=id%2Camount%2Crate_per_hour%2Chours_credited%2Cclaimed_at%2Cnext_claim_at&order=claimed_at.desc&limit=1"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                next_claim_str = data[0]['next_claim_at']
                # Ambil 19 karakter pertama (YYYY-MM-DDTHH:MM:SS) dan set ke UTC
                clean_time_str = next_claim_str[:19]
                return datetime.strptime(clean_time_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        return None
    except Exception as e:
        print(f"[-] Error mengambil jadwal claim: {e}")
        return None

def solve_puzzle_with_2captcha():
    """
    Fungsi ini menangani alur penyelesaian captcha dengan 2Captcha.
    Karena bentuk validasi endpoint GXT belum diketahui spesifikasinya,
    bagian ini memuat kerangka dasarnya.
    """
    print("[*] Memulai proses bypass Captcha...")
    
    # 1. Request ke server GXT untuk mendapatkan data puzzle baru
    # puzzle_req = requests.get(f"{GXT_API_URL}/public/puzzle", headers=HEADERS)
    # data_puzzle = puzzle_req.json()
    # puzzle_id = data_puzzle.get("id")
    # puzzle_image = data_puzzle.get("image")
    
    # 2. Kirim data ke 2Captcha (Contoh tipe Coordinates/Custom)
    # print("[*] Mengirim puzzle ke 2Captcha...")
    # captcha_submit_url = f"http://2captcha.com/in.php?key={TWOCAPTCHA_API_KEY}&method=post&json=1"
    # Di sini kamu akan mengirim base64 gambar puzzle ke 2Captcha
    
    # 3. Tunggu hasil koordinat/token dari 2Captcha
    # res_url = f"http://2captcha.com/res.php?key={TWOCAPTCHA_API_KEY}&action=get&id={captcha_task_id}&json=1"
    
    # 4. Verifikasi hasil tersebut ke endpoint GXT
    # verify_req = requests.post(f"{GXT_API_URL}/public/puzzle/verify", json={"id": puzzle_id, "answer": captcha_answer})
    
    # KEMBALIKAN puzzle_id yang sudah divalidasi
    # return puzzle_id
    
    print("[!] Modul 2Captcha disiapkan. Menunggu logika spesifik endpoint GXT puzzle.")
    # Sementara mengembalikan statis sesuai request sebelumnya untuk testing
    return "53794aa7-c89c-464a-b1a7-dea5a5e716a4" 

def do_claim():
    print("[*] Menyiapkan eksekusi claim...")
    
    # Dapatkan puzzle_id yang sudah di-bypass
    puzzle_id = solve_puzzle_with_2captcha()
    
    claim_url = f"{BASE_URL}/rest/v1/rpc/claim_mining_v1"
    payload = {
        "_idempotency_key": str(uuid.uuid4()),
        "_puzzle_id": puzzle_id
    }
    
    try:
        response = requests.post(claim_url, headers=HEADERS, json=payload)
        
        if response.status_code in [200, 201]:
            data = response.json()
            if data.get("ok"):
                print(f"[+] BERHASIL CLAIM! Mendapatkan: {data.get('reward')} GXT")
            else:
                print(f"[-] Respons claim OK false: {data}")
        else:
            print(f"[-] Gagal claim (HTTP {response.status_code}): {response.text}")
    except Exception as e:
        print(f"[-] Error saat claim: {e}")

def main():
    print("==============================")
    print("    AUTO CLAIM GXT BOT        ")
    print("==============================\n")
    
    if not BEARER_TOKEN or not TWOCAPTCHA_API_KEY:
        print("[-] ERROR: BEARER_TOKEN atau TWOCAPTCHA_API_KEY tidak ditemukan di file .env!")
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
