import time
from datetime import datetime as dt
import platform
import ctypes
import os
import sys
from jinja2 import Template  # Necesitarás instalar Jinja2 con pip install Jinja2

# Determinar la ruta del archivo de hosts según el sistema operativo
if platform.system() == "Windows":
    host_path = r"C:\Windows\System32\drivers\etc\hosts"

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

elif platform.system() == "Linux" or platform.system() == "Darwin":
    host_path = "/etc/hosts"
else:
    raise OSError("Sistema operativo no compatible")

temporal_host_path = "hosts"

def is_working_hours(from_hour, to_hour):
    current_time = dt.now()
    return dt(current_time.year, current_time.month, current_time.day, from_hour) < current_time < dt(current_time.year, current_time.month, current_time.day, to_hour)

def generate_script_template(websites, redirect_to):
    script_template = """# Script generado automáticamente
# Bloqueo de sitios web durante las horas de trabajo

{% for website in websites %}
{{ redirect_to }} {{ website }}
{% endfor %}
"""
    template = Template(script_template)
    return template.render(websites=websites, redirect_to=redirect_to)

def write_script_to_file(script_content, file_path):
    with open(file_path, "w") as file:
        file.write(script_content)

def add_websites_hosts_file(websites, host_file, redirect_to):
    script_content = generate_script_template(websites, redirect_to)
    write_script_to_file(script_content, temporal_host_path)

    with open(temporal_host_path, "r") as file:
        content = file.read()

    with open(host_file, "a") as file:
        file.write("\n" + content)

def clean_websites_hosts_file(websites, host_file):
    with open(host_file, "r") as file:
        content = file.readlines()

    with open(host_file, "w") as file:
        for line in content:
            if not any(website in line for website in websites):
                file.write(line)

# Ejemplo de uso
from_hour = None
to_hour = None
websites_list = []

redirect_to = "127.0.0.1"

def run_script(from_hour, to_hour, websites_list, host_path):
    while True:
        if is_working_hours(from_hour, to_hour):
            remaining_hours = to_hour - dt.now().hour
            print(f"Working hours... Sites will be unblocked in {remaining_hours} hours.")
            add_websites_hosts_file(websites_list, host_path, redirect_to)
            sleep_time = 60  # Dormir durante 60 segundos (1 minuto)
        else:
            print("Fun hours...")
            clean_websites_hosts_file(websites_list, host_path)
            sleep_time = 10  # Dormir durante 10 segundos

        # Esperar antes del próximo ciclo
        time.sleep(sleep_time)

# this is going to be a script

if __name__ == "__main__":
    run_script(from_hour, to_hour, websites_list, host_path)