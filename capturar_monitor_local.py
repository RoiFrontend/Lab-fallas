import os
import sys
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

REPO_DIR = r"C:\Users\roger\Downloads\lab-fallas\lab-fallas"
EVIDENCIAS_DIR = os.path.join(REPO_DIR, "docs", "evidencias")
os.makedirs(EVIDENCIAS_DIR, exist_ok=True)

def run_cmd(cmd, env_vars=None):
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
    print(f"[CMD] {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=REPO_DIR, env=env, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [ERROR] code={res.returncode}: {res.stderr.strip()[:200]}")
    else:
        print(f"  [OK] {res.stdout.strip()[:120]}")
    return res

def wait_for_api(url="http://localhost:8085/api/", timeout=15):
    import urllib.request
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            req = urllib.request.urlopen(url, timeout=2)
            if req.status == 200:
                return True
        except Exception:
            time.sleep(0.5)
    return False

def init_driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1280,840')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    return driver

def capture_experiment(driver, name, target_reqs=85, sleep_after=1):
    print(f"--- Capturando experimento: {name} ---")
    clear_btn = driver.find_element(By.ID, 'clear')
    clear_btn.click()
    time.sleep(0.5)
    
    play_btn = driver.find_element(By.ID, 'play')
    play_btn.click() # Start
    
    # Wait until total >= target_reqs or max 20 seconds
    t0 = time.time()
    total_el = driver.find_element(By.ID, 'total')
    errs_el = driver.find_element(By.ID, 'errs')
    
    while time.time() - t0 < 25:
        time.sleep(0.5)
        try:
            tot = int(total_el.text)
            if tot >= target_reqs:
                break
        except Exception:
            pass
            
    play_btn.click() # Pause
    time.sleep(sleep_after)
    
    out_path = os.path.join(EVIDENCIAS_DIR, name)
    driver.save_screenshot(out_path)
    print(f"  [GUARDADO] {out_path} (Total={total_el.text}, Errores={errs_el.text})")
    return out_path

def main():
    print("Iniciando captura automatizada de experimentos en el Monitor...")
    
    # 1. B1 - Round Robin normal con 3 replicas
    print("\n=== EXP B1: Round Robin (3 réplicas, memoria local) ===")
    run_cmd("docker compose down")
    run_cmd("docker compose up -d")
    wait_for_api()
    time.sleep(2)
    
    driver = init_driver()
    driver.get("http://localhost:8085/")
    time.sleep(1)
    capture_experiment(driver, "monitor_B1_round_robin.png", target_reqs=96)
    
    # 2. B2a - Matar lab-fallas-api-2 con nginx.conf (bueno)
    print("\n=== EXP B2a: Failover transparente con nginx.conf bueno ===")
    run_cmd("docker kill lab-fallas-api-2")
    time.sleep(1)
    capture_experiment(driver, "monitor_B2a_failover_exitoso.png", target_reqs=96)
    
    # 3. B2b - Matar replica con nginx-defectuoso.conf
    print("\n=== EXP B2b: Fallas visibles con nginx-defectuoso.conf (errores 504) ===")
    run_cmd("docker start lab-fallas-api-2")
    run_cmd("docker compose up -d --force-recreate lb", env_vars={"NGINX_CONF": "nginx-defectuoso.conf"})
    wait_for_api()
    time.sleep(2)
    run_cmd("docker kill lab-fallas-api-2")
    time.sleep(1)
    driver.get("http://localhost:8085/")
    time.sleep(1)
    capture_experiment(driver, "monitor_B2b_nginx_defectuoso_rojos.png", target_reqs=96)
    
    # 4. B3 - Estado compartido en Redis
    print("\n=== EXP B3: Estado compartido con Redis ===")
    run_cmd("docker start lab-fallas-api-2")
    run_cmd("docker compose up -d api lb", env_vars={"REDIS_URL": "redis://redis:6379/0", "NGINX_CONF": "nginx.conf"})
    wait_for_api()
    time.sleep(2)
    driver.get("http://localhost:8085/")
    time.sleep(1)
    capture_experiment(driver, "monitor_B3_redis_compartido.png", target_reqs=96)
    
    # 5. B4a - Réplica lenta con Round Robin
    print("\n=== EXP B4a: Réplica lenta con Round Robin (concurrencia 8) ===")
    # Concurrencia 8
    conc_select = Select(driver.find_element(By.ID, 'conc'))
    conc_select.select_by_visible_text('8')
    time.sleep(0.5)
    # Marcar una replica lenta
    slow_btn = driver.find_element(By.ID, 'slow')
    slow_btn.click()
    time.sleep(1)
    capture_experiment(driver, "monitor_B4a_lenta_round_robin.png", target_reqs=80)
    
    # 6. B4b - Réplica lenta con least_conn
    print("\n=== EXP B4b: Réplica lenta con least_conn (concurrencia 8) ===")
    run_cmd("docker compose up -d --force-recreate lb", env_vars={"REDIS_URL": "redis://redis:6379/0", "NGINX_CONF": "nginx-least-conn.conf"})
    time.sleep(2)
    driver.get("http://localhost:8085/")
    time.sleep(1)
    conc_select = Select(driver.find_element(By.ID, 'conc'))
    conc_select.select_by_visible_text('8')
    time.sleep(0.5)
    capture_experiment(driver, "monitor_B4b_lenta_least_conn.png", target_reqs=80)
    
    # Limpieza: Restaurar a estado limpio
    print("\n=== Restaurando ambiente limpio ===")
    run_cmd("docker compose up -d --force-recreate lb api", env_vars={"NGINX_CONF": "nginx.conf"})
    
    driver.quit()
    print("\n¡Todas las capturas del monitor local fueron generadas con éxito en docs/evidencias/!")

if __name__ == '__main__':
    main()
