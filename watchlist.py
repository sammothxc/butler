# watchlist.py
import os
import json
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
watchlist_file = "/home/butler/butler/watchlist.txt"
opts = FirefoxOptions()
opts.add_argument("--headless")

def log_in(USERNAME: str, PASSWORD: str, driver) -> None:
    driver.get("https://www.instagram.com/accounts/login")
    driver.find_element(By.NAME, 'username').send_keys(USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, \
        '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button'))).click()
    time.sleep(5)

def status_check(username: str, driver) -> list[bool, str, bool]:
    '''
    checks if account exists, its id and if its private (returned in this order)
    '''
    # get the text from site
    url = "https://www.instagram.com/web/search/topsearch/?query=" + username
    driver.get(url)
    text = driver.page_source
    res = [False, "", False]
    text = text[text.index("{"):]

    first_name_index = text.index('"username":"') + len('"username":"')
    first_id_index = text.index('"pk_id":"') + len('"pk_id":"')
    first_private_index = text.index('"is_private":') + len('"is_private":')
    
    res[0] = text[first_name_index:first_name_index + len(username)] == username # is the first match our username?
    if res[0]:
        res[1] = text[first_id_index:text.index('"', first_id_index)]
        res[2] = not text[first_private_index:text.index('"', first_private_index)] == "false"

    return res

def get_json(username, driver): # no longer used
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

def encode(string: str) -> str: # no longer used
    # I fucked this one up a bit in the original, isalpha instead of isnumeric
    return "".join(char for char in string if char.isalpha())

def get_most_likely(usernames, alts) -> list[str]: # no longer used
    return [alt for alt in list(alts) if encode(alt) in {encode(name) for name in usernames}]

def check_username(driver, username, potential_alts): # no longer used
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

def check_watchlist_function() -> dict[str: list[bool, str, bool]]:
    '''
    checks usernames from watchlist_file
    returns a dict with usernames as keys and a list of exists:bool, id:str, private:bool as values
    expects watchlist file with a trailing newline
    expects creds in .env file
    '''

    MAIN_USERNAME = os.getenv('IG_USERNAME')
    MAIN_PASSWORD = os.getenv('IG_PASSWORD')

    # create driver and log in
    driver = webdriver.Firefox(options=opts)
    driver.implicitly_wait(10)
    log_in(MAIN_USERNAME, MAIN_PASSWORD, driver)

    exists = {}

    # iter through the lines, strip them from newlines and run the check on them
    with open(watchlist_file, "r", encoding="utf-8") as wanted:
        exists = {username: status_check(username, driver) for username in map(str.strip, wanted)}
    
    return exists

def list_watchlist_function():
    '''
    lists the usernames in the watchlist_file and the links to their accounts
    returns a single string if no errors occured, False otherwise
    expects file with a trailing newline
    '''

    try:
        with open(watchlist_file, "r", encoding="utf-8") as wanted:
            result = "\n".join(f"[{username.strip()}](https://www.instagram.com/{username})" for username in wanted)
            return result
    except Exception as e:
        print(e)
        return False

def add_to_watchlist_function(username: str) -> bool:
    '''
    adds a username to the watchlist_file if it's not already there
    returns True if username was added, False otherwise
    expects file with a trailing newline
    '''

    with open(watchlist_file, "r", encoding="utf-8") as wanted:
        # this reads through only the usernames not the links, less string = less time
        usernames = wanted.read()
        if usernames.startswith(username+"\n") or "\n"+username+"\n" in usernames:
            return False
    
    try:
        with open(watchlist_file, "a", encoding="utf-8") as wanted:
            wanted.write(username + "\n")
    except:
        return False
    return True

def remove_from_watchlist_function(username: str) -> bool:
    '''
    remove username from the watchlist_file if it's there
    returns True if username was in file and was removed, False otherwise
    expects a file with a trailing newline
    '''

    # get all the usernames in a single string
    with open(watchlist_file, "r", encoding="utf-8") as wanted:
        usernames = wanted.read()
    
    # delete the username from the string and check if it was deleted
    if usernames.startswith(username + "\n"):
        new_usernames = usernames[len(username) + 1:]
    else:
        new_usernames = usernames.replace("\n" + username + "\n", "\n")
        if len(usernames) == len(new_usernames):
            return False

    # write the string without the deleted username
    with open(watchlist_file, "w", encoding="utf-8") as wanted:
        wanted.write(new_usernames)

    return True
