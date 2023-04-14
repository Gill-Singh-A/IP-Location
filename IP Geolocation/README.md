# IP Location using ipgeolocation API
A Python Program that gives Geological Information about an IP Address's Location using IPGeolocation's API.

## Requirements
Language Used = Python3<br />
Modules/Packages used:
* tkinter
* tkintermapview
* sys
* json
* requests
* colorama

## Input
* '-t', "--target" : IP Address/Addresses of the Target/Targets to scan Ports (seperated by ',')
* '-v', "--verbose" : Display Information about IP's Location on screen (Default=True)
* '-l', "--locate" : Locate IP's Location on Map (Default=True)
* '-w', "--write" : File to which the IP Location Data has to be dumped
* '-r', "--read" : File from which data dump has to be read

## Output
It displays the Geological Information about the IP Address's Location that it got from IPGeolocation's API and also adds a marker on the map that was created using tkinter and tkintermapview depeding on the input provided by the user.<br /><br />

### Note 
* The location might not be correct
* It is just a program that provides an Interface to display that data that it got from the database of the given service.
* And it is also not live tracking of a device.
* You must replace YOUR_API_KEY on line 56 with your api key that you got from https://ipgeolocation.io/
