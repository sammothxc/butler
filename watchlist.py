# watchlist.py
import os
import json
import time
from typing import Union, List, Dict, Tuple
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
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
        '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button'))).click()
    time.sleep(6)
    ## implement a check for the login


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

    # check the first user that pops up

    first_name_index = text.index('"username":"') + len('"username":"')
    res[0] = text[first_name_index:first_name_index + len(username)] == username # is the first match our username?

    if res[0]: # found em first try
        first_id_index = text.index('"pk_id":"') + len('"pk_id":"')
        first_private_index = text.index('"is_private":') + len('"is_private":')
        res[1] = text[first_id_index:text.index('"', first_id_index)]
        res[2] = not text[first_private_index:text.index(',', first_private_index)] == "false"

    else: # playing hard to get, much slower but should be bulletproof
        try:
            text = text[:text.rindex("}") + 1]
            users_json = json.loads(text)
            for user in users_json['users']:
                res[0] = user['user']['username'] == username
                if res[0]:
                    res[1] = user['user']['pk_id']
                    res[2] = user['user']['is_private']
                    break
        except Exception as e:
            print(e)

    print(res)
    return res


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
    print("logged in")
    exists = {}

    # iter through the lines, strip them from newlines and run the check on them
    with open(watchlist_file, "r", encoding="utf-8") as wanted:
        exists = {username: status_check(username, driver) for username in map(str.strip, wanted)}
    
    print(exists)
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

# version 2.0 - work in progress

'''
this version expects the data in a .csv file,
with a semicolon (;) or a colon (,) as a delimiter:
+----------+----------+----------+----------+----------+
|    ID    | username | category |   tags   |  status  |
+----------+----------+----------+----------+----------+
| 00000000 | abcdefgh |  pixels  |   full   |  active  |
| 00000001 | a0b1c2d3 |   real   |   part   |suppressed|
|          | a=>.()sd |          |          |eliminated|
+----------+----------+----------+----------+----------+

the .csv file is expected WITHOUT the column heads,
saved in utf-8, with trailing newline.
'''

# log_in and check_username stay the same

def get_validation() -> tuple[set[str], set[str], set[str]]:
    '''
    returns allowed values of category, status and tags
    '''
    category = {"pixels", "real", ""}
    status = {"active", "suppressed", "eliminated"}
    tags = {"full", "part", ""}
    return (category, status, tags)


def add_to_watchlist_2(username: str, user_id:str="", category:str="", tags:str="", status:str="active", file_path:str=watchlist_file) -> bool:
    '''
    adds a new line to the list, if the name isn't already there,
    optional arguments allow filling the other columns
    '''

    delimiter = ","
    # check the input
    if username == "":
        return False

    allowed = get_validation()
    for i, arg in enumerate((category, status, tags)):
        if arg not in allowed[i]:
            return False


    # check list for username
    with open(file_path, "r", encoding="utf-8") as wanted:
        if ";" in wanted.read():
            delimiter = ";"
        for line in wanted:
            if line.split(delimiter)[1] == username:
                return False

    # write

    with open(watchlist_file, "a", encoding="utf-8") as wanted:
        wanted.write(delimiter.join((user_id, username, category, tags, status)) + "\n")
        return True

  
def remove_from_watchlist_2(username: str, file_path:str=watchlist_file) -> bool:
    '''
    removes username from the list if it's there
    '''
    delimiter = ","
    with open(file_path, "r", encoding="utf-8") as wanted:
        if ";" in wanted.read():
            delimiter = ";"
        lines = [line for line in wanted if line.split(delimiter)[1] != username]
        if len(lines) == len(wanted.readlines()):
            return False
    
    with open(file_path, "w", encoding="utf-8") as wanted:
        for line in lines:
            wanted.write(line)


def list_watchlist_2(file_path: str=watchlist_file):
    '''
    prints out formatted data from the file and links to the accounts,
    returns a single string if no errors occured, False otherwise,
    expects file with a trailing newline
    '''
    delimiter = ","
    try:
        with open(file_path, "r", encoding="utf-8") as wanted:
            if ";" in wanted.read():
                delimiter = ";"
            result = "\n".join(f"{username} ({user_id}): {status} {tags} {category}" for user_id, username, category, tags, status in map(str.strip().split(delimiter), wanted))
            return result

    except Exception as e:
        print(e)
        return False


def check_watchlist_2(file_path:str=watchlist_file) -> None:
    '''
    checks usernames from watchlist_file and updates them
    expects watchlist file with a trailing newline
    expects creds in .env file
    '''
    delimiter = ","

    MAIN_USERNAME = os.getenv('IG_USERNAME')
    MAIN_PASSWORD = os.getenv('IG_PASSWORD')

    # create driver and log in
    driver = webdriver.Firefox(options=opts)
    driver.implicitly_wait(10)
    log_in(MAIN_USERNAME, MAIN_PASSWORD, driver)
    print("logged in")
    i = 0

    # iter through the lines, strip them from newlines and run the check on them
    res_lines = []
    with open(file_path, "r", encoding="utf-8") as wanted:
        if ";" in wanted.read():
            delimiter = ";"
        for line in wanted:
            user_id, username, category, tags, status = line.strip().split(delimiter)

            # this bit shouldn't come to be useful but leave it just in case
            if status == "eliminated":
                res_lines.append(line)
                continue

            check = status_check(username, driver)
            new_status = "eliminated" if not check[0] else ("suppressed" if check[2] else "active")
            new_id = user_id if user_id != "" else check[1]
            new_line = delimiter.join(new_id, username, category, tags, new_status)
            res_lines.append(new_line + "\n")
            i += 1
        j = len(wanted.readlines())
    
    response = input(f"changed {str(i)} out of {str(j)} lines, are you sure you want to overwrite? Y/N: ")
    if response not in "Yy":
        return


    with open(file_path, "w", encoding="utf-8") as wanted:
        for line in res_lines:
            wanted.write(line)
        print("watchlist updated")
