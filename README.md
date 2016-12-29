# python-lightning-earthnetworks

This script maps real-time lightning strike locations in the continental United States using a TCP socket datafeed from Earth Networks. 

![Animated-Lightning](screenshots/screenshot_lightning-animated.Gif)

<h1>WHAT</h1>

Earth Networks is a provider of global weather data and operates the Earth Networks Total Lightning Network (ENTLN), one of three lightning networks in the United States that provides real-time information about lightning strikes.  

[Earth Networks - Lightning](https://www.earthnetworks.com/networks/lightning/ "EarthNetworks-Lightning")

Earth Networks provides access to real-time lightning data from the ENTLN via a TCP socket connection, referred to as the ENTLN Data Feed (see link below for a datafeed interface document).

[Earth Networks Total Lightning Network - Data Feed Version 3.0](http://www.bandgap.cs.rice.edu/classes/comp410/resources/SiteAssets/Using%20IoT/WeatherBug%20API%20info/ENTLN%20Lightning%20Data%20Feed%20v3%20ICD%20-%20UM67.pdf "EarthNetworks-LightningDataFeed") *Access to this datafeed is restricted to paying subscribers.

In this script, it is shown how to (i) connect to the ENTLN Data Feed using Python, (ii) parse out lightning data from the JSON payloads received from the TCP socket, and (iii) plot lightning strike locations on a map of the continental United States.

<h1>HOW</h1>

