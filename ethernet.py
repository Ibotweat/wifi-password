import subprocess
import re

def get_wifi_passwords():
    wifi_profiles = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True).stdout
    profile_names = re.findall(r"Profil Tous les utilisateurs\s*:\s(.*)", wifi_profiles)

    wifi_data = {}

    for name in profile_names:
        name = name.strip()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True, text=True).stdout
        password_match = re.search(r"Contenu de la clé\s*:\s(.*)", profile_info)
        
        wifi_data[name] = password_match.group(1).strip() if password_match else "Non trouvé"

    return wifi_data

if __name__ == "__main__":
    passwords = get_wifi_passwords()
    for wifi, password in passwords.items():
        print(f"SSID: {wifi} | Password: {password}")
