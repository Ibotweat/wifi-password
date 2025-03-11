import subprocess
import re

def get_wifi_passwords():
    # Récupère la liste des profils Wi-Fi enregistrés
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
    profiles = re.findall(r"Profil Tous les utilisateurs\s*:\s(.*)", command_output.stdout)

    wifi_list = []

    for profile in profiles:
        profile = profile.strip()
        # Récupère les détails du profil, y compris le mot de passe
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"], capture_output=True, text=True)
        password = re.search(r"Contenu de la clé\s*:\s(.*)", profile_info.stdout)

        wifi_list.append({
            "SSID": profile,
            "Password": password.group(1) if password else "Non trouvé"
        })

    return wifi_list

# Afficher les résultats
wifi_data = get_wifi_passwords()
for wifi in wifi_data:
    print(f"SSID: {wifi['SSID']}, Password: {wifi['Password']}")
