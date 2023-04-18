import ipinfo
import tkinter
import tkintermapview
from datetime import date
from optparse import OptionParser
from pickle import dump, load
from sys import argv
from time import strftime, localtime
from colorama import Fore, Back, Style


status_color = {
	'+': Fore.GREEN,
	'-': Fore.RED,
	'*': Fore.YELLOW,
	':': Fore.CYAN,
	' ': Fore.WHITE,
}

def get_time():
	return strftime("%H:%M:%S", localtime())
def display(status, data):
	print(f"{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {get_time()}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}")


def get_arguments(*args):
	parser = OptionParser()
	for arg in args:
		parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
	return parser.parse_args()[0]

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
        try:
            map_widget.set_marker(float(data["latitude"]), float(data["longitude"]), text=data["ip"])
            map_widget.set_position(float(data["latitude"]), float(data["longitude"]))
        except:
            pass
    window.mainloop()

def get_ip_location(ips, verbose=False, locate=False):
    access_token = "YOUR_ACCESS_TOKEN_KEY"
    handler = ipinfo.getHandler(access_token)
    location_data = []
    for ip in ips:
        data = handler.getDetails(ip).all
        location_data.append(data)
        if verbose:
            display_ip_location_info(data)
    if locate:
        locate_ip_on_map(location_data)
    return location_data

if __name__ == "__main__":
    data = get_arguments(('-t', "--target", "target", "IP Address/Addresses of the Target/Targets to scan Ports (seperated by ',')"),
                         ('-v', "--verbose", "verbose", "Display Information about IP's Location on screen (Default=True)"),
                         ('-l', "--locate", "locate", "Locate IP's Location on Map (Default=True)"),
                         ('-w', "--write", "write", "File to which the IP Location Data has to be dumped"),
                         ('-r', "--read", "read", "File from which data dump has to be read"))
    if data.read:
        try:
            with open(data.read, 'rb') as file:
                location_data = load(file)
        except FileNotFoundError:
            display('-', f"{Back.MAGENTA}{data.read}{Back.RESET} File not found!")
            exit(0)
        except:
            display('-', f"Error reading from file {Back.MAGENTA}{data.read}{Back.RESET}")
            exit(0)
        for ip_location_data in location_data:
            display_ip_location_info(ip_location_data)
        if data.locate:
            locate_ip_on_map(location_data)
        exit(0)
    if not data.target:
        display('-', "Please specify a Target")
        exit(0)
    else:
        data.target = data.target.split(',')
    if not data.verbose:
        data.verbose = True
    else:
        if data.verbose == "False":
            data.verbose = False
        else:
            data.verbose = True
    if not data.locate:
        data.locate = True
    else:
        if data.locate == "False":
            data.locate = False
        else:
            data.locate = True
    location_data = get_ip_location(data.target, verbose=data.verbose, locate=data.locate)
    if data.write:
        with open(data.write, 'wb') as file:
            dump(location_data, file)