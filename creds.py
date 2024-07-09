def edit_creds_function(username: str, password: str):
    with open("creds.py", "r") as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if "username" in line:
            lines[i] = f'username = "{username}"\n'
        elif "password" in line:
            lines[i] = f'password = "{password}"\n'
    
    with open("creds.py", "w") as f:
        f.write("".join(lines))
    
    return True