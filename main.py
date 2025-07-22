
import socket
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import platform
import msvcrt

class Colors:
    PURPLE_1 = '\033[38;5;147m'
    PURPLE_2 = '\033[38;5;146m'
    PURPLE_3 = '\033[38;5;145m'
    PURPLE_4 = '\033[38;5;144m'
    PURPLE_5 = '\033[38;5;143m'
    PURPLE_6 = '\033[38;5;142m'
    GREEN = '\033[38;5;82m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def gradient(text, start_color, end_color):
    colors = [start_color, end_color]
    result = ""
    for i, char in enumerate(text):
        if char != " ":
            color = colors[i % 2]
            result += f"{color}{char}{Colors.RESET}"
        else:
            result += char
    return result

def logo():
    logo = f"""
{Colors.PURPLE_1}                    {Colors.BOLD}██╗  ██╗██╗████████╗██╗  ██╗██╗████████╗{Colors.RESET}
{Colors.PURPLE_1}                    {Colors.BOLD}██║ ██╔╝██║╚══██╔══╝██║ ██╔╝██║╚══██╔══╝{Colors.RESET}
{Colors.PURPLE_1}                    {Colors.BOLD}█████╔╝ ██║   ██║   █████╔╝ ██║   ██║{Colors.RESET}
{Colors.PURPLE_1}                    {Colors.BOLD}██╔═██╗ ██║   ██║   ██╔═██╗ ██║   ██║{Colors.RESET}
{Colors.PURPLE_1}                    {Colors.BOLD}██║  ██╗██║   ██║   ██║  ██╗██║   ██║{Colors.RESET}
{Colors.PURPLE_1}                    {Colors.BOLD}╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝   ╚═╝{Colors.RESET}
"""
    print(logo)

def clear(tool=""):
    subprocess.run("cls", shell=True)
    if tool:
        subprocess.run(f'title kitkit - {tool}', shell=True)
    else:
        subprocess.run("title kitkit", shell=True)

def lookup():
    while True:
        clear("lookup")
        print("\n\n")
        logo()
        print("\n\n\n\n\n")
        
        target = input(f"{Colors.PURPLE_1}host@kitkit ` {Colors.RESET}").strip()
        
        if target.lower() == 'back':
            break
            
        if not target:
            break
            
        try:
            import re
            if target.startswith(('http://', 'https://')):
                domain = re.search(r'https?://([^/]+)', target)
                if domain:
                    target = domain.group(1)
            elif '/' in target:
                target = target.split('/')[0]
            
            if target.startswith('www.'):
                target = target[4:]
                
            if not target.replace('.', '').replace('-', '').replace('_', '').isdigit():
                try:
                    resolved_ip = socket.gethostbyname(target)
                    ip = resolved_ip
                except:
                    ip = target
            else:
                ip = target
                
            print()
            print(f"{Colors.PURPLE_1}[ip] {ip}{Colors.RESET}")
            
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                if hostname and hostname != ip:
                    print(f"{Colors.PURPLE_1}[hostname] {hostname}{Colors.RESET}")
            except:
                pass
                
            try:
                aliases = socket.gethostbyaddr(ip)[1]
                if aliases and len(aliases) > 0:
                    print(f"{Colors.PURPLE_1}[aliases] {', '.join(aliases)}{Colors.RESET}")
            except:
                pass
                
            try:
                import requests
                response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    city = data.get('city')
                    if city and city != 'Unknown':
                        print(f"{Colors.PURPLE_1}[city] {city}{Colors.RESET}")
                    
                    region = data.get('region')
                    if region and region != 'Unknown':
                        print(f"{Colors.PURPLE_1}[state] {region}{Colors.RESET}")
                    
                    country = data.get('country')
                    if country and country != 'Unknown':
                        print(f"{Colors.PURPLE_1}[country] {country}{Colors.RESET}")
                    
                    company = data.get('org')
                    if company and company != 'Unknown':
                        company_clean = company.replace('AS', '').replace('Ltd', '').replace('LLC', '').replace('Inc', '').replace('Corp', '').strip()
                        print(f"{Colors.PURPLE_1}[isp] {company_clean}{Colors.RESET}")
                    
                    hostname = data.get('hostname')
                    if hostname and hostname != 'Unknown':
                        print(f"{Colors.PURPLE_1}[hostname] {hostname}{Colors.RESET}")
            except ImportError:
                pass
            except Exception as e:
                pass
                
        except Exception as e:
            print(f"{Colors.PURPLE_1}error: {str(e)}{Colors.RESET}")
            
        input()

def scan(host, port, protocol='tcp'):
    try:
        if protocol == 'tcp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            sock.close()
            return port, result == 0
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.5)
            try:
                sock.sendto(b'\x00', (host, port))
                sock.recvfrom(1024)
                sock.close()
                return port, True
            except socket.timeout:
                sock.close()
                return port, False
            except:
                sock.close()
                return port, False
    except:
        return port, False

def scanner():
    while True:
        clear("scanner")
        print("\n\n")
        logo()
        print("\n\n\n\n")
        
        print(f"{Colors.PURPLE_1}     [1] common{Colors.RESET}")
        print(f"{Colors.PURPLE_1}     [2] range{Colors.RESET}")
        
        print("\n")
        choice = input(f"{Colors.PURPLE_1}scanner@kitkit ` {Colors.RESET}").strip()
        
        if choice not in ['1', '2']:
            continue
            
        clear()
        print("\n\n")
        logo()
        print("\n\n\n\n")
        
        print(f"{Colors.PURPLE_1}     [1] tcp{Colors.RESET}")
        print(f"{Colors.PURPLE_1}     [2] udp{Colors.RESET}")
        print("\n")
        
        protocol = input(f"{Colors.PURPLE_1}protocol@kitkit ` {Colors.RESET}").strip()
        
        if protocol not in ['1', '2']:
            continue
            
        clear()
        print("\n\n")
        logo()
        print("\n\n\n\n")
        
        target = input(f"{Colors.PURPLE_1}host@kitkit ` {Colors.RESET}").strip()
        
        if not target:
            break
            
        try:
            import re
            if target.startswith(('http://', 'https://')):
                domain = re.search(r'https?://([^/]+)', target)
                if domain:
                    target = domain.group(1)
            elif '/' in target:
                target = target.split('/')[0]
            
            if target.startswith('www.'):
                target = target[4:]
                
            ip = socket.gethostbyname(target)
            
            if choice == '1':
                ports = [21, 22, 23, 25, 53, 80, 110, 137, 138, 139, 143, 443, 445, 548, 587, 993, 995, 1433, 1701, 1723, 3306, 5432, 8008, 8443, 666, 2302, 3453, 3724, 4000, 5154, 6112, 6113, 6114, 6115, 6116, 6117, 6118, 6119, 7777, 10093, 10094, 12203, 14567, 25565, 26000, 27015, 27910, 28000, 50000, 515, 631, 3282, 3389, 5190, 5050, 4443, 1863, 6891, 1503, 5631, 5632, 5900, 6667, 119, 375, 425, 1214, 412, 1412, 2412, 4661, 4662, 4665, 5500, 6346, 6881, 6882, 6883, 6884, 6885, 6886, 6887, 6888, 6889]
            else:
                clear()
                print("\n\n")
                logo()
                print("\n\n\n\n")
                
                start_port = input(f"{Colors.PURPLE_1}start@kitkit ` {Colors.RESET}").strip()
                end_port = input(f"{Colors.PURPLE_1}end@kitkit ` {Colors.RESET}").strip()
                
                try:
                    start = int(start_port)
                    end = int(end_port)
                    if start < 1 or end > 65535 or start > end:
                        break
                    else:
                        ports = range(start, end + 1)
                except:
                    break
            
            open_ports = []
            
            protocol_type = 'tcp' if protocol == '1' else 'udp'
            
            if choice == '2':
                with ThreadPoolExecutor(max_workers=200) as executor:
                    results = list(executor.map(lambda p: scan(ip, p, protocol_type), ports))
                    for port, is_open in results:
                        if is_open:
                            open_ports.append(port)
            else:
                with ThreadPoolExecutor(max_workers=2000) as executor:
                    results = list(executor.map(lambda p: scan(ip, p, protocol_type), ports))
                    for port, is_open in results:
                        if is_open:
                            open_ports.append(port)
            
            print("\n")
            if open_ports:
                for port in sorted(open_ports):
                    print(f"{Colors.GREEN} + {port}{Colors.RESET}")
            else:
                print(f"{Colors.PURPLE_1}none{Colors.RESET}")
                
        except:
            pass
            
        input()
        break



def pinger():
    while True:
        clear("pinger")
        print("\n\n")
        logo()
        print("\n\n\n\n\n")
        
        target = input(f"{Colors.PURPLE_1}pinger@kitkit ` {Colors.RESET}").strip()
        
        if not target:
            break
            
        parts = target.split()
        custom_port = None
        
        if len(parts) == 1:
            host = parts[0]
        elif len(parts) == 2:
            host = parts[0]
            try:
                custom_port = int(parts[1])
                if custom_port < 1 or custom_port > 65535:
                    custom_port = None
            except:
                custom_port = None
        else:
            continue
        
        import re
        if host.startswith(('http://', 'https://')):
            domain_match = re.search(r'https?://([^/]+)', host)
            if domain_match:
                host = domain_match.group(1)
        
        if custom_port is not None:
            port = custom_port
        else:
            if target.startswith(('http://', 'https://')):
                if target.startswith('https://'):
                    port = 443
                else:
                    port = 80
            elif target.startswith('www.'):
                port = 80
            else:
                port = None
        
        try:
            if port is None:
                print()
                while True:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        if key == b'\r':
                            break
                    
                    try:
                        cmd = ["ping", "-n", "1", host]
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        if result.returncode == 0:
                            lines = result.stdout.split('\n')
                            for line in lines:
                                if 'time=' in line:
                                    time_match = line.split('time=')[1].split('ms')[0]
                                    print(f"{Colors.PURPLE_1}{host} | online | icmp{Colors.RESET}")
                                    break
                        else:
                            print(f"{Colors.PURPLE_1}{host} | offline | icmp{Colors.RESET}")
                    except KeyboardInterrupt:
                        break
                    
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        if key == b'\r':
                            break
                    
                    time.sleep(1)
                break
            else:
                try:
                    ip = socket.gethostbyname(host)
                    print()
                    while True:
                        if msvcrt.kbhit():
                            key = msvcrt.getch()
                            if key == b'\r':
                                break
                        
                        start_time = time.time()
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(2)
                            result = sock.connect_ex((ip, port))
                            end_time = time.time()
                            sock.close()
                            
                            if result == 0:
                                response_time = (end_time - start_time) * 1000
                                print(f"{Colors.PURPLE_1}{host} | online | {response_time:.1f}ms | {port}{Colors.RESET}")
                            else:
                                print(f"{Colors.PURPLE_1}{host} | offline | {port}{Colors.RESET}")
                                
                        except:
                            print(f"{Colors.PURPLE_1}{host} | offline | {port}{Colors.RESET}")
                        
                        if msvcrt.kbhit():
                            key = msvcrt.getch()
                            if key == b'\r':
                                break
                            
                        time.sleep(1)
                except:
                    pass
                break
                    
        except:
            pass
            
        break

def main():
    while True:
        clear()
        print("\n\n")
        logo()
        print("\n\n\n\n")
        
        print(f"{Colors.PURPLE_1}     [1] lookup{Colors.RESET}")
        print(f"{Colors.PURPLE_1}     [2] scanner{Colors.RESET}")
        print(f"{Colors.PURPLE_1}     [3] pinger{Colors.RESET}")
        print("\n\n\n")
        
        username = subprocess.run("whoami", shell=True, capture_output=True, text=True).stdout.strip().split('\\')[-1]
        choice = input(f"{Colors.PURPLE_1}{username}@kitkit ` {Colors.RESET}").strip()
        
        if choice == '1':
            lookup()
        elif choice == '2':
            scanner()
        elif choice == '3':
            pinger()
        else:
            continue

try:
    main()
except KeyboardInterrupt:
    sys.exit(0)
