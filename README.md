# BDT2022_Project

This project starts from a specific assignment for the Big Data Technologies course of the Master of Science in Data Science at the University of Trento.
The assignment was the following:
*[transportation] Design and implement a big data system that can support transportation agencies in the design (and monitoring) of policies related to private/public transport and congestion charge zones.*

When developing policies, agencies require a huge amount of data from the region under analysis, in order to justify the decisions and maximize the efficiency of their actions. Our solution tries to offer data retrieval methods for the city of Milan that can be helpful for any agency or other entity that is interested in the transportation system of the city. Specifically, our attempts led to a system that provides the users with real time data about the traffic flow of the city and the weather conditions (an information that, in our vision, could be taken into consideration by agencies to evaluate the traffic situation itself), together with a bunch of historical datasets about transportation means and conditions for the city of Milan. 
This choice comes from the necessity to offer enough data about the city to help agencies taking informed decisions, but also from the limited amount of time and resources we had at our disposal for the development of the project.
Thus, we're perfectly aware that better solutions (mostly for what concerns the variety of the data, their completeness and their integration) are possible and, indeed, preferable. However, given the aforementioned constraints, we prefered to focus on providing something simpler but working. 
Finally, we decide to provide also some suggestions about how to retrieve and eventually analyze/display the collected data.
About this last point, unfortunately we cannot offer nice comparisons and relationships between the historical and the real-time data because of the time lag - since the historical data are mostly yearly-based whereas the real-time data have been collected on an hourly basis.

## Getting the real-time data
About real-time data, as anticipated, we include in our big data system two different solutions, one about traffic flow and one about weather. The real-time data about traffic flows can obviously be used to create a big database where each street is associated to the expected speed of the vehicles and the actually-registered speed (in fact, the ration between these two information provides the traffic situation), and the variations of these parameters could be compared along time.
The same is also reletable to the weather data. This provides the hourly situation of several weather parameters (temperature, wind, humidity, and so on) about the city of Milan, and they can be easily used to collect an historical series that can then be compared and related to the traffic flow information - and also, hypothetically, to the historical use of the transportation means if those data would come in a smaller time raster.

For what concerns the traffic flow data, after having examined different sources - specifically, we look at the TomTom's Traffic APIs, at the Google Maps API, and at the OpenStreetMap data - we ended up fetching the Here Traffic API due to their greater accessibility and completeness. As a matter of fact, most of the other options only offer static information and, mostly, no clue about actual traffic flows.
On the contrary, the Here Traffic API (in their seventh version) provides different options to gather the actual mean speed of the vehicles for each city street, and thus a clever way to compute the traffic status.
Moreover, the Here Traffic API offer several options for the setting of parameters like the geographical boundaries or the zoom.
As specified on their website, *"the HERE Traffic API v7 is a REST API that provides real-time traffic flow and incident information".* In particular, regarding the traffic flow information, it *"provides access to real-time traffic flow data in JSON, including information on speed and jam factor for the region(s) defined in each request. The Traffic API v7 can also deliver additional data such as the geometry of the road segments in relation to the flow".*
Also, *"the response from the flow endpoint provides a list of flow objects together with the last updated time of the source data. Each flow object consists of a location field containing a location reference and a currentFlow field describing the current traffic conditions [...]. A current flow object contains 3 speed values:*

- *freeFlow - the reference speed along the roadway when no traffic is present*

- *speed - the expected speed along the roadway; will not exceed the legal speed limit*

- *speedUncapped - the expected speed along the roadway; may exceed the legal speed limit*

While the first two values allow us to compute the traffic status of a specific street - since the ratio between the actual speed and the expected speed when there's no traffic describes the difference between the current situation and the ideal one -, the third could be useful from a regulatory point of view, as it could be exploited to monitor the maximal speed reached in each street and, eventually, impose some speed limits.
Ultimately, the traffic real-time data are collected fetching the Here Traffic API once an hour, and then stored in a SQL database table with the following fields: *'date_time', 'name', 'length', 'lat', 'lon', 'actual_speed', 'uncapped_speed', 'free_flow_speed', 'jam_factor', 'traversability'*.

For what concerns the weather real-time data ... [ANNA]

## Getting the historical data
The need for historical data comes from the unavailability of real-time data about the public transport system for the city of Milan. Luckily, the city has a large amount of historical data (most of them updated with irregular frequency) on its portal at https://dati.comune.milano.it/, and many of them are about transportation.
Among all the ones available, we decided to select only the ones that appear to provide the most valuable information, and the ones that are more related with the purpose of our project.
Accordingly, we selected 44 datasets about transportation (mainly), viability, population and air (another factor that could and should be considered by agencies when drafting policies), but many others could have been included.
Then, we suggest two solutions for retrieving them: the first one is to store each dataset as a SQL database table, so to having them at disposal for analyses and visualizations; the second one is about storing in a SQL database table all the links to the datasets, and then query the database when that particular link is needed.
Both the solutions are viable, but the latter is probably preferable since the datasets are updated with irregular frequency, and this option allows to retrieve always the most recent ones; on the other hand, retrieving and storing the datasets could lead some analysis to be based on old data, specially if they are applied some time after the data retrieval.
