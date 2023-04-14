import tkinter
import tkintermapview
from sys import argv
from json import loads
from requests import get
from colorama import Fore, Style

def display_ip_location_info(data):
    max_space = max([len(key) for key, _ in data.items()])+5
    for key, value in data.items():
        if type(value) != dict:
            print(f"{Fore.GREEN}[+]{Fore.BLUE} {key}{' '*(max_space-len(key))}{Fore.CYAN}{Style.BRIGHT}{value}{Fore.RESET}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[+]{Fore.BLUE} {key}")
            max_space_2 = max([len(key) for key, _ in data.items()])+5
            for key_2, value_2 in value.items():
                print(f"{Fore.YELLOW}[*]\t{Fore.BLUE}{key_2}{' '*(max_space_2-len(key_2))}{Fore.GREEN}{Style.BRIGHT}{value_2}{Fore.RESET}{Style.RESET_ALL}")
    print('\n')

def locate_ip_on_map(location_data):
    window = tkinter.Tk()
    window.title("IP Location")
    window.geometry("800x600+100+100")
    map_widget = tkintermapview.TkinterMapView(window, width=800, height=600, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    for data in location_data:
        map_widget.set_marker(float(data["latitude"]), float(data["longitude"]), text=data["ip"])
        map_widget.set_position(float(data["latitude"]), float(data["longitude"]))
    window.mainloop()

def get_ip_location(ips, verbose=False, locate=False):
    api_key = "YOUR_API_KEY"
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip="
    location_data = []
    for ip in ips:
        data = loads(get(f"{url}{ip}").text)
        location_data.append(data)
        if verbose:
            display_ip_location_info(data)
    if locate:
        locate_ip_on_map(location_data)
    return location_data

if __name__ == "__main__":
    get_ip_location(argv[1:], verbose=True, locate=True)