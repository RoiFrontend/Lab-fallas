import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

REPO_DIR = r"C:\Users\roger\Downloads\lab-fallas\lab-fallas"
EVIDENCIAS_DIR = os.path.join(REPO_DIR, "docs", "evidencias")
os.makedirs(EVIDENCIAS_DIR, exist_ok=True)

def run_cmd(cmd):
    print(f"[CMD] {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=REPO_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [ERROR]: {res.stderr.strip()[:150]}")
    else:
        print(f"  [OK]: {res.stdout.strip()[:120]}")
    return res

def init_driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1280,840')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver

def capture_k8s_exp(driver, name, target_reqs=90, sleep_after=1):
    print(f"\n--- Capturando K8s: {name} ---")
    driver.get("http://localhost:8090/")
    time.sleep(1)
    
    # Asegurar que el target apunte al NodePort de K8s: http://localhost:30080/
    target_input = driver.find_element(By.ID, 'target')
    target_input.clear()
    target_input.send_keys("http://localhost:30080/")
    time.sleep(0.5)
    
    clear_btn = driver.find_element(By.ID, 'clear')
    clear_btn.click()
    time.sleep(0.5)
    
    play_btn = driver.find_element(By.ID, 'play')
    play_btn.click()
    
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
            
    play_btn.click()
    time.sleep(sleep_after)
    
    out_path = os.path.join(EVIDENCIAS_DIR, name)
    driver.save_screenshot(out_path)
    print(f"  [GUARDADO] {out_path} (Total={total_el.text}, Errores={errs_el.text})")
    return out_path

def main():
    print("Iniciando captura de evidencias de Kubernetes Kind en Monitor...")
    driver = init_driver()
    
    # 1. C3: 3 Pods en Kubernetes atendiendo en Round Robin
    capture_k8s_exp(driver, "monitor_C3_k8s_3replicas.png", target_reqs=96)
    
    # 2. C5: Escalar a 5 replicas (aparecen 2 colores nuevos)
    run_cmd("kubectl scale deployment/api --replicas=5")
    time.sleep(5)
    capture_k8s_exp(driver, "monitor_C5_k8s_5replicas.png", target_reqs=100)
    
    # 3. C6: Detener worker ais86-worker (simulando caida de servidor fisico)
    print("Deteniendo ais86-worker...")
    run_cmd("docker stop ais86-worker")
    # Capturar ventana de fallo y detección
    time.sleep(3)
    capture_k8s_exp(driver, "monitor_C6_k8s_nodo_caido.png", target_reqs=80)
    # Revivir nodo
    run_cmd("docker start ais86-worker")
    time.sleep(5)
    
    # 4. C7: Despliegue roto (ROMPER_HEALTH=1)
    run_cmd("kubectl scale deployment/api --replicas=3")
    time.sleep(5)
    run_cmd("kubectl set env deployment/api ROMPER_HEALTH=1")
    time.sleep(8)
    capture_k8s_exp(driver, "monitor_C7_k8s_despliegue_roto.png", target_reqs=96)
    run_cmd("kubectl rollout undo deployment/api")
    time.sleep(3)
    
    driver.quit()
    print("\n¡Capturas de Kubernetes Kind generadas con éxito!")

if __name__ == '__main__':
    main()
