import socket

def send_pisugar_command(command):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect("/tmp/pisugar-server.sock")
            sock.send(command.encode("utf-8"))
            response = sock.recv(1024).decode("utf-8")
            return response.strip().split(":")[1].strip()

    except Exception as e:
        print("Error:", str(e))
    
    return None

def get_battery_level():
    response = send_pisugar_command("get battery\n")
    return float(response) if response is not None else None

def is_running_on_battery():
    charging_status = send_pisugar_command("get battery_charging\n")
    return charging_status.lower() == "false" if charging_status is not None else None

def is_battery_charging():
    charging_status = send_pisugar_command("get battery_charging\n")
    return charging_status.lower() == "true" if charging_status is not None else None

if __name__ == "__main__":
    battery_level = get_battery_level()
    if is_running_on_battery():
        if battery_level is not None:
            print(f"Battery Level: {battery_level}%")
        else:
            print("Failed to retrieve battery level.")
    else:
        print("Running on Power")
