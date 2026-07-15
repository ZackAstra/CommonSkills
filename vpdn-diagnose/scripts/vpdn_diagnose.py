import subprocess
import json
import os
import sys
import winreg

def run_cmd(cmd, encoding='gbk'):
    """Execute a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding=encoding, errors='replace')
        return {'returncode': result.returncode, 'output': result.stdout + result.stderr}
    except Exception as e:
        return {'returncode': -1, 'output': str(e)}

def read_reg(path, value_name, hive=winreg.HKEY_CURRENT_USER):
    """Read a Windows registry value."""
    try:
        with winreg.OpenKey(hive, path) as key:
            val, typ = winreg.QueryValueEx(key, value_name)
            return {'value': str(val), 'type': str(typ)}
    except FileNotFoundError:
        return {'value': None, 'error': 'Not found'}
    except Exception as e:
        return {'value': None, 'error': str(e)}

def get_vpn_connections():
    """Get list of configured VPN/dial-up connections."""
    pbk_dirs = [
        os.path.expandvars(r'%APPDATA%\Microsoft\Network\Connections\Pbk'),
        os.path.expandvars(r'%PROGRAMDATA%\Microsoft\Network\Connections\Pbk'),
    ]
    connections = []
    for d in pbk_dirs:
        if os.path.exists(d):
            try:
                files = [f for f in os.listdir(d) if f.endswith('.pbk')]
                connections.extend(files)
            except Exception:
                pass
    return connections

def diagnose():
    """Run comprehensive VPDN diagnosis and return results dict."""
    results = {}

    # 1. Proxy Settings (Registry)
    results['proxy_enable'] = read_reg(
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
        'ProxyEnable'
    )
    results['proxy_server'] = read_reg(
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
        'ProxyServer'
    )
    results['proxy_override'] = read_reg(
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
        'ProxyOverride'
    )
    results['winhttp_proxy'] = run_cmd('netsh winhttp show proxy')

    # 2. System Services
    services = [
        'RasMan',
        'RemoteAccess',
        'Telephony',
        'NetworkConnections',
        'RemoteAccessConnectionManager',
        'TrustService',
    ]
    for svc in services:
        results[f'service_{svc}'] = run_cmd(f'sc query {svc}')

    # 3. Network Interfaces
    results['interfaces'] = run_cmd('netsh interface show interface')
    results['ipconfig'] = run_cmd('ipconfig /all')
    results['route'] = run_cmd('route print')

    # 4. VPDN Client Files
    vpdn_dir = r'C:\Program Files (x86)\dx_vpdn'
    if os.path.exists(vpdn_dir):
        results['vpdn_files'] = os.listdir(vpdn_dir)
    else:
        results['vpdn_files'] = 'NOT_FOUND'

    # 5. VPDN PBK Configurations
    results['vpn_connections'] = get_vpn_connections()

    # 6. Windows Event Logs (RasClient, last 48 hours)
    results['rasclient_events'] = run_cmd(
        'wevtutil qe Application '
        '/q:"*[System[Provider[@Name=\'RasClient\'] and EventID=20227 and '
        'TimeCreated[timediff(@SystemTime) <= 172800000]]]" '
        '/f:text /c:20'
    )

    # 7. Active Processes
    results['vpdn_process'] = run_cmd('tasklist /FI "IMAGENAME eq VPDN*" /FO LIST')
    results['trustagent_process'] = run_cmd('tasklist /FI "IMAGENAME eq dx_TrustAgent*" /FO LIST')

    # 8. Network Connections & Ports
    results['netstat'] = run_cmd('netstat -an | findstr "1723 500 4500 443 80"')
    results['listeners'] = run_cmd('netstat -ano | findstr "LISTENING"')

    # 9. Firewall Status
    results['firewall'] = run_cmd('netsh advfirewall show currentprofile')

    # 10. DNS
    results['dns_flush'] = run_cmd('ipconfig /flushdns')
    results['dns_display'] = run_cmd('ipconfig /displaydns')

    # 11. WMI Permissions (for 651 errors)
    results['wmi_perms'] = run_cmd('icacls "C:\\Windows\\System32\\LogFiles\\WMI"')

    # 12. Environment Proxy Variables
    results['env_http_proxy'] = os.environ.get('HTTP_PROXY', 'not_set')
    results['env_https_proxy'] = os.environ.get('HTTPS_PROXY', 'not_set')
    results['env_all_proxy'] = os.environ.get('ALL_PROXY', 'not_set')

    return results

def save_report(results, output_path=None):
    """Save diagnosis results to a JSON file."""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), 'vpdn_diagnosis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return output_path

def print_summary(results):
    """Print a human-readable summary of key findings."""
    print("=" * 60)
    print("VPDN DIAGNOSIS SUMMARY")
    print("=" * 60)

    # Proxy check
    proxy = results.get('proxy_enable', {})
    if proxy.get('value') == '1':
        server = results.get('proxy_server', {}).get('value', 'unknown')
        print(f"[ALERT] System proxy is ENABLED: {server}")
        print("        This is the #1 cause of 'VPDN server access failed'")
    else:
        print("[OK] System proxy is disabled")

    # Services
    print("\n[SERVICES]")
    for key, val in results.items():
        if key.startswith('service_'):
            svc_name = key.replace('service_', '')
            out = val.get('output', '')
            if 'RUNNING' in out:
                print(f"  [OK] {svc_name}: RUNNING")
            elif 'STOPPED' in out:
                print(f"  [WARN] {svc_name}: STOPPED")
            elif '1060' in out:
                print(f"  [INFO] {svc_name}: Not installed (may be normal)")
            else:
                print(f"  [?] {svc_name}: {out[:60]}")

    # VPDN process
    print("\n[PROCESSES]")
    vpdn = results.get('vpdn_process', {}).get('output', '')
    if 'VPDN' in vpdn:
        print("  [OK] VPDN client is running")
    else:
        print("  [INFO] VPDN client not running (may be closed)")

    trust = results.get('trustagent_process', {}).get('output', '')
    if 'dx_TrustAgent' in trust:
        print("  [OK] TrustAgent is running")
    else:
        print("  [INFO] TrustAgent not running")

    # Events
    events = results.get('rasclient_events', {}).get('output', '')
    if 'CoId=' in events:
        print("\n[EVENT LOG] Recent RasClient errors found:")
        # Extract error codes
        import re
        codes = re.findall(r'错误代码为 (\d+)', events)
        if codes:
            print(f"  Recent error codes: {', '.join(set(codes))}")
    else:
        print("\n[EVENT LOG] No recent RasClient errors (client may not reach dial stage)")

    print("\n" + "=" * 60)

def main():
    """Main entry point."""
    results = diagnose()
    output_path = save_report(results)
    print_summary(results)
    print(f"\nFull report saved to: {output_path}")
    return results

if __name__ == '__main__':
    main()
