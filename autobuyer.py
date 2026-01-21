import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


#==========================================

url = "https://www.neopets.com/objects.phtml?type=shop&obj_type=2"
CSV_PATH = "Morphing Potion" 
REFRESH_SEC = 5

# catch and read the potion list
def load_wanted_potion(csv_path: str) -> set[str]:
    wanted = set()
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line and line != "name":
                wanted.add(line)
    return wanted

# chrome setting
def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--disable-notifications")
    service = Service("chromedriver.exe") 
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# login
def login(driver: webdriver.Chrome, username: str, password: str):
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    u = wait.until(EC.presence_of_element_located((By.ID, "loginUsername")))
    p = driver.find_element(By.ID, "loginPassword")

    u.clear()
    u.send_keys(username)

    p.clear()
    p.send_keys(password)
    p.submit()

    time.sleep(2)
    driver.add_cookie({"name": "lang", "value": "en"})
    driver.refresh()
    time.sleep(2)