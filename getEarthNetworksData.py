#!/usr/bin/env python

import socket
import struct
import json
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

#####################################
### REFERENCES

# ENTLN Data Feed Documentation: http://www.bandgap.cs.rice.edu/classes/comp410/resources/SiteAssets/Using%20IoT/WeatherBug%20API%20info/ENTLN%20Lightning%20Data%20Feed%20v3%20ICD%20-%20UM67.pdf
# Parse byte string payload: http://stackoverflow.com/questions/27428936/python-size-of-message-to-send-via-socket
# Map of CONUS: http://geodesygina.com/matplotlib.html
# Plot lat/lng point on map: https://peak5390.wordpress.com/2012/12/08/matplotlib-basemap-tutorial-plotting-points-on-a-simple-map/

#####################################
### CONNECTION INFO

# TCP URL FOR ENTLN
TCP_URL = 'lx.datamart.earthnetworks.com'
TCP_PORT = 80

# TCP URL (SSL) FOR ENTLN
#TCP_SSL_URL = TCP_URL
#TCP_SSL_PORT = 443

#####################################
### AUTHENTICATION MESSAGE 

# PARTER ID (PROVIDED BY EARTH NETWORKS)
a_partner_id = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'

# VERSION
a_version = '3'

# FORMAT
# 1 - ASCII format (UTF-8 format)
# 2 - Binary format
a_format = '1' 

# TYPE
# 1 - Flash
# 2 - Pulse
# 3 - Combination Flash and Pulse
a_type = '2'

# AUTHENTICATION PAYLOAD 
msg_authenticate = {
	"p": a_partner_id,
	"v": a_version,
	"f": a_format,
	"t": a_type
}

#####################################
### DEFINE FUNCTIONS

# INITIALIZE MAP OF CONUS
def initMap():

	# Plot Interactive Mode
	plt.ion()

	# Create New Map
	m = Basemap(projection='merc',llcrnrlat=20,urcrnrlat=50,\
				llcrnrlon=-130,urcrnrlon=-60,lat_ts=20,resolution='i')
				
	# Draw Coastlines, Countries, States
	m.drawcoastlines()
	m.drawcountries()
	m.drawstates()

	# Draw Parallels and Meridians.
	parallels = np.arange(-90.,91.,5.)

	# Label the Meridians and Parallels
	m.drawparallels(parallels,labels=[False,True,True,False])

	# Draw Meridians and Labels
	meridians = np.arange(-180.,181.,10.)
	m.drawmeridians(meridians,labels=[True,False,False,True])
	m.drawmapboundary(fill_color='grey')

	plt.title("Lightning!")
	plt.show()
	
	return m
	
# PLOT LIGHTNING STRIKE ON MAP
def plotStrike(m, data):

	# Extract Lat/Lon from Message
	lat = float(data['latitude'])
	lon = float(data['longitude'])
	
	# Convert to Map XY
	x,y = m(lon, lat)
	
	# Add XY Point to Map
	m.plot(x, y, 'rx', markersize=18)
	
	# Pause Plot to Allow Refresh
	plt.pause(0.1)

# Get Socket Message
def get_msg(s):
	header_bytes = 4
	count = struct.unpack('>i', _get_block(s, header_bytes))[0]
	return _get_block(s, count-header_bytes)

# Get Message Block
def _get_block(s, count):
    if count <= 0:
        return ''
    buf = ''
    while len(buf) < count:
        buf2 = s.recv(count - len(buf))
        if not buf2:
            # error or just end of connection?
            if buf:
                raise RuntimeError("underflow")
            else:
                return ''
        buf += buf2		
    return buf

#####################################
### INITIALIZE MAP

m = initMap();
		
#####################################
### START SOCKET
  
raw_input("Press Enter to start socket connection...")
print ''
 
# Connect to Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_URL, TCP_PORT))

# Socket Authentication
msg_authenticate_o = json.dumps(msg_authenticate)
print msg_authenticate_o
print ''
s.send(msg_authenticate_o)

# Start Getting Messages...
while True:  

	# Get Message from Socket
	payload = get_msg(s)
	
	# Convert to JSON object
	payload_o = json.loads(payload)
	print payload_o
	print ''

	# Check if strike, then... 
	# NOTE: This is a crude way to validate a data payload vs a keep-alive payload.
	if 'latitude' in payload_o:
			
		# PLOT LIGHTNING STRIKE
		plotStrike(m,payload_o)
 