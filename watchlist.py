# watchlist.py
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

watchlist_file = "/home/butler/butler/watchlist.txt"
creds_file = "/home/butler/butler/creds.txt"

def log_in(USERNAME, PASSWORD, driver):
    driver.get("https://www.instagram.com/accounts/login")
    
    driver.find_element(By.NAME, 'username').send_keys(USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD)

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, \
        '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button'))).click()

def get_json(username, driver):
    url = "https://www.instagram.com/web/search/topsearch/?query=" + username
    driver.get(url)
    text = driver.page_source

    if "{" not in text or "users" not in text:
        return {}

    text = text[text.index("{"):]
    text = text[:text.index("<")]

    try:
        return json.loads(text)
    except:
        return {}

def encode(string):
    return "".join([char for char in string if char.isnumeric()])

def get_most_likely(usernames, alts):
    return [alt for alt in list(alts) if encode(alt) in set([encode(name) for name in usernames])]

def check_username(driver, username, potential_alts):
    users_json = get_json(username, driver=driver)
    if users_json == {}:
        print("invalid JSON")
        return False

    exists = (False,)
    for user in users_json['users']:
        is_wanted = user['user']['full_name'] == username or user['user']['username'] == username
        if not is_wanted:
            potential_alts.add(user['user']['full_name'])
        else:
            exists = (True, user['user']['pk_id'])
            
    return exists

def check_watchlist_function():
    with open(watchlist_file, "r", encoding="utf-8") as wanted:
        usernames_to_check = wanted.read().split(";")
    
    with open(creds_file, "r") as pass_file:
        creds = pass_file.read().split(";")

    MAIN_USERNAME = creds[0]
    MAIN_PASSWORD = creds[1]

    potential_alts = set()
    exists = {}

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    log_in(MAIN_USERNAME, MAIN_PASSWORD, driver)
    time.sleep(5)

    for username in usernames_to_check:
        exists[username] = check_username(driver, username, potential_alts)
        time.sleep(1)
    
    return exists

def list_watchlist_function():
    try:
        with open(watchlist_file, "r", encoding="utf-8") as wanted:
            content = wanted.read().strip()
            if not content:
                return False
            
            usernames = content.split(";")
            return "\n".join(usernames)
    except FileNotFoundError:
        return False
    except Exception as e:
        return False

def add_to_watchlist_function(username):
    with open(watchlist_file, "a", encoding="utf-8") as wanted:
        wanted.write(username + ";")

    return True
    
def remove_from_watchlist_function(username):
    with open(watchlist_file, "r", encoding="utf-8") as wanted:
        usernames = wanted.read().split(";")
    
    with open(watchlist_file, "w", encoding="utf-8") as wanted:
        wanted.write(";".join([name for name in usernames if name != username]))
    
    return True