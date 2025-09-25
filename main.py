import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import msvcrt
import warnings
warnings.filterwarnings('ignore')


def logo():
    logo = f"""
\033[38;5;147m                    \033[1m██╗  ██╗██╗████████╗██╗  ██╗██╗████████╗\033[0m
\033[38;5;147m                    \033[1m██║ ██╔╝██║╚══██╔══╝██║ ██╔╝██║╚══██╔══╝\033[0m
\033[38;5;147m                    \033[1m█████╔╝ ██║   ██║   █████╔╝ ██║   ██║\033[0m
\033[38;5;147m                    \033[1m██╔═██╗ ██║   ██║   ██╔═██╗ ██║   ██║\033[0m
\033[38;5;147m                    \033[1m██║  ██╗██║   ██║   ██║  ██╗██║   ██║\033[0m
\033[38;5;147m                    \033[1m╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝   ╚═╝\033[0m
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
        
        target = input(f"\033[38;5;147mhost@kitkit ` \033[0m").strip()
        
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
                    resolvedIp = socket.gethostbyname(target)
                    ip = resolvedIp
                except:
                    ip = target
            else:
                ip = target
                
            print()
            print(f"\033[38;5;147m[ip] {ip}\033[0m")
            
            try:
                import urllib.request
                import json
                with urllib.request.urlopen(f"https://ipinfo.io/{ip}/json", timeout=3) as response:
                    if response.status == 200:
                        data = json.load(response)
                        city = data.get('city')
                        if city and city != 'Unknown':
                            print(f"\033[38;5;147m[city] {city}\033[0m")
                        region = data.get('region')
                        if region and region != 'Unknown':
                            print(f"\033[38;5;147m[state] {region}\033[0m")
                        country = data.get('country')
                        if country and country != 'Unknown':
                            print(f"\033[38;5;147m[country] {country}\033[0m")
                        company = data.get('org')
                        if company and company != 'Unknown':
                            companyClean = company.replace('AS', '').replace('Ltd', '').replace('LLC', '').replace('Inc', '').replace('Corp', '').strip()
                            print(f"\033[38;5;147m[isp] {companyClean}\033[0m")
                        hostname = data.get('hostname')
                        if hostname and hostname != 'Unknown':
                            print(f"\033[38;5;147m[hostname] {hostname}\033[0m")
            except ImportError:
                pass
            except Exception as e:
                pass
                
        except Exception as e:
            print(f"\033[38;5;147merror: {str(e)}\033[0m")
            
        input()
        break

def dns():
    while True:
        clear("dns")
        print("\n\n")
        logo()
        print("\n\n\n\n\n")
        
        target = input(f"\033[38;5;147mdns@kitkit ` \033[0m").strip()
        
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
                
            print()
            
            try:
                aRecords = socket.getaddrinfo(target, None, socket.AF_INET)
                ips = list(set([addr[4][0] for addr in aRecords]))
                for ip in ips:
                    print(f"\033[38;5;147m[A] {ip}\033[0m")
            except:
                pass
                
            try:
                aaaaRecords = socket.getaddrinfo(target, None, socket.AF_INET6)
                ipv6s = list(set([addr[4][0] for addr in aaaaRecords]))
                for ipv6 in ipv6s:
                    print(f"\033[38;5;147m[AAAA] {ipv6}\033[0m")
            except:
                pass
                
            try:
                import subprocess
                nsResult = subprocess.run(['nslookup', '-type=NS', target], capture_output=True, text=True, timeout=5)
                if nsResult.returncode == 0:
                    lines = nsResult.stdout.split('\n')
                    for line in lines:
                        if 'nameserver' in line.lower():
                            ns = line.split('=')[-1].strip().rstrip('.')
                            if ns and not ns.startswith('Non-'):
                                print(f"\033[38;5;147m[NS] {ns}\033[0m")
            except:
                pass
                
            try:
                mxResult = subprocess.run(['nslookup', '-type=MX', target], capture_output=True, text=True, timeout=5)
                if mxResult.returncode == 0:
                    lines = mxResult.stdout.split('\n')
                    for line in lines:
                        if 'mail exchanger' in line.lower():
                            mx = line.split('=')[-1].strip().rstrip('.')
                            if mx:
                                print(f"\033[38;5;147m[MX] {mx}\033[0m")
            except:
                pass
                
            try:
                txtResult = subprocess.run(['nslookup', '-type=TXT', target], capture_output=True, text=True, timeout=5)
                if txtResult.returncode == 0:
                    lines = txtResult.stdout.split('\n')
                    for line in lines:
                        if 'text =' in line.lower():
                            txt = line.split('=', 1)[-1].strip().strip('"')
                            if txt:
                                print(f"\033[38;5;147m[TXT] {txt}\033[0m")
            except:
                pass
                
            try:
                cnameResult = subprocess.run(['nslookup', '-type=CNAME', target], capture_output=True, text=True, timeout=5)
                if cnameResult.returncode == 0:
                    lines = cnameResult.stdout.split('\n')
                    for line in lines:
                        if 'canonical name' in line.lower():
                            cname = line.split('=')[-1].strip().rstrip('.')
                            if cname:
                                print(f"\033[38;5;147m[CNAME] {cname}\033[0m")
            except:
                pass
                
            try:
                soaResult = subprocess.run(['nslookup', '-type=SOA', target], capture_output=True, text=True, timeout=5)
                if soaResult.returncode == 0:
                    lines = soaResult.stdout.split('\n')
                    for line in lines:
                        if 'primary name server' in line.lower():
                            soa = line.split('=')[-1].strip().rstrip('.')
                            if soa:
                                print(f"\033[38;5;147m[SOA] {soa}\033[0m")
            except:
                pass
                
            try:
                ptrResult = subprocess.run(['nslookup', '-type=PTR', target], capture_output=True, text=True, timeout=5)
                if ptrResult.returncode == 0:
                    lines = ptrResult.stdout.split('\n')
                    for line in lines:
                        if 'name =' in line.lower():
                            ptr = line.split('=')[-1].strip().rstrip('.')
                            if ptr:
                                print(f"\033[38;5;147m[PTR] {ptr}\033[0m")
            except:
                pass
                
            try:
                srvResult = subprocess.run(['nslookup', '-type=SRV', target], capture_output=True, text=True, timeout=5)
                if srvResult.returncode == 0:
                    lines = srvResult.stdout.split('\n')
                    for line in lines:
                        if 'service =' in line.lower():
                            srv = line.split('=')[-1].strip()
                            if srv:
                                print(f"\033[38;5;147m[SRV] {srv}\033[0m")
            except:
                pass
                
            try:
                cadResult = subprocess.run(['nslookup', '-type=CAA', target], capture_output=True, text=True, timeout=5)
                if cadResult.returncode == 0:
                    lines = cadResult.stdout.split('\n')
                    for line in lines:
                        if 'caa record' in line.lower():
                            caa = line.split('=')[-1].strip()
                            if caa:
                                print(f"\033[38;5;147m[CAA] {caa}\033[0m")
            except:
                pass
                
        except Exception as e:
            print(f"\033[38;5;147merror: {str(e)}\033[0m")
            
        input()
        break

def scan(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        sock.close()
        return port, result == 0
    except:
        return port, False

def scanner():
    while True:
        clear("scanner")
        print("\n\n")
        logo()
        print("\n\n\n\n")
        
        print(f"\033[38;5;147m     [1] common\033[0m")
        print(f"\033[38;5;147m     [2] range\033[0m")
        
        print("\n")
        choice = input(f"\033[38;5;147mscanner@kitkit ` \033[0m").strip()
        
        if choice not in ['1', '2']:
            continue
            
        clear()
        print("\n\n")
        logo()
        print("\n\n\n\n")
        
        print(f"\033[38;5;147m     [1] tcp\033[0m")
        
        protocol = '1'
        
        clear()
        print("\n\n")
        logo()
        print("\n\n\n\n")
        
        target = input(f"\033[38;5;147mhost@kitkit ` \033[0m").strip()
        
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
                
                startPort = input(f"\033[38;5;147mstart@kitkit ` \033[0m").strip()
                endPort = input(f"\033[38;5;147mend@kitkit ` \033[0m").strip()
                
                try:
                    start = int(startPort)
                    end = int(endPort)
                    if start < 1 or end > 65535 or start > end:
                        break
                    else:
                        ports = range(start, end + 1)
                except:
                    break
            
            openPorts = []
            
            if choice == '2':
                with ThreadPoolExecutor(max_workers=200) as executor:
                    results = list(executor.map(lambda p: scan(ip, p), ports))
                    for port, isOpen in results:
                        if isOpen:
                            openPorts.append(port)
            else:
                with ThreadPoolExecutor(max_workers=2000) as executor:
                    results = list(executor.map(lambda p: scan(ip, p), ports))
                    for port, isOpen in results:
                        if isOpen:
                            openPorts.append(port)
            
            print("\n")
            if openPorts:
                for port in sorted(openPorts):
                    print(f"\033[38;5;82m + {port}\033[0m")
            else:
                print(f"\033[38;5;147mnone\033[0m")
                
        except:
            pass
            
        input()
        break


def pingHost(host, port=None):
    if port is None:
        try:
            cmd = ["ping", "-n", "1", host]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'time=' in line:
                        timeMatch = line.split('time=')[1].split('ms')[0]
                        return f"{host} | online | {timeMatch}ms | icmp"
            return f"{host} | offline | icmp"
        except:
            return f"{host} | offline | icmp"
    else:
        try:
            startTime = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            endTime = time.time()
            sock.close()
            
            if result == 0:
                responseTime = (endTime - startTime) * 1000
                return f"{host} | online | {responseTime:.1f}ms | {port}"
            else:
                return f"{host} | offline | {port}"
        except:
            return f"{host} | offline | {port}"

def pinger():
    while True:
        clear("pinger")
        print("\n\n")
        logo()
        print("\n\n\n\n\n")
        
        target = input(f"\033[38;5;147mpinger@kitkit ` \033[0m").strip()
        
        if not target:
            break
            
        parts = target.split()
        customPort = None
        
        if len(parts) == 1:
            host = parts[0]
        elif len(parts) == 2:
            host = parts[0]
            try:
                customPort = int(parts[1])
                if customPort < 1 or customPort > 65535:
                    customPort = None
            except:
                customPort = None
        else:
            continue
            
        if '/' in host and host.count('.') == 3:
            try:
                network, cidr = host.split('/')
                cidr = int(cidr)
                if cidr < 8 or cidr > 30:
                    continue
                    
                import ipaddress
                subnet = ipaddress.IPv4Network(f"{network}/{cidr}", strict=False)
                hosts = list(subnet.hosts())
                
                print()
                print(f"\033[38;5;147msubnet {len(hosts)}\033[0m")
                print()
                
                with ThreadPoolExecutor(max_workers=50) as executor:
                    if customPort:
                        results = list(executor.map(lambda h: pingHost(str(h), customPort), hosts))
                    else:
                        results = list(executor.map(lambda h: pingHost(str(h)), hosts))
                    
                    for result in results:
                        if 'online' in result:
                            print(f"\033[38;5;82m + {result}\033[0m")
                        else:
                            print(f"\033[38;5;147m - {result}\033[0m")
                
                input()
                break
                
            except Exception as e:
                print(f"\033[38;5;147merror: {str(e)}\033[0m")
                input()
                break
        
        import re
        if host.startswith(('http://', 'https://')):
            domainMatch = re.search(r'https?://([^/]+)', host)
            if domainMatch:
                host = domainMatch.group(1)
        
        if customPort is not None:
            port = customPort
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
                                    timeMatch = line.split('time=')[1].split('ms')[0]
                                    print(f"\033[38;5;147m{host} | online | {timeMatch}ms | icmp\033[0m")
                                    break
                        else:
                            print(f"\033[38;5;147m{host} | offline | icmp\033[0m")
                    except KeyboardInterrupt:
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
                        
                        startTime = time.time()
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(2)
                            result = sock.connect_ex((ip, port))
                            endTime = time.time()
                            sock.close()
                            
                            if result == 0:
                                responseTime = (endTime - startTime) * 1000
                                print(f"\033[38;5;147m{host} | online | {responseTime:.1f}ms | {port}\033[0m")
                            else:
                                print(f"\033[38;5;147m{host} | offline | {port}\033[0m")
                                
                        except:
                            print(f"\033[38;5;147m{host} | offline | {port}\033[0m")
                        
                        time.sleep(1)
                    break
                except:
                    pass
                    
        except:
            pass
            

def main():
    while True:
        clear()
        print("\n\n")
        logo()
        print("\n\n\n\n")
        
        print(f"\033[38;5;147m     [1] lookup\033[0m")
        print(f"\033[38;5;147m     [2] dns\033[0m")
        print(f"\033[38;5;147m     [3] scanner\033[0m")
        print(f"\033[38;5;147m     [4] pinger\033[0m")
        print("\n\n\n")
        
        username = subprocess.run("whoami", shell=True, capture_output=True, text=True).stdout.strip().split('\\')[-1]
        choice = input(f"\033[38;5;147m{username}@kitkit ` \033[0m").strip()
        
        if choice == '1':
            lookup()
        elif choice == '2':
            dns()
        elif choice == '3':
            scanner()
        elif choice == '4':
            pinger()
        else:
            continue

try:
    main()
except KeyboardInterrupt:
    sys.exit(0)
