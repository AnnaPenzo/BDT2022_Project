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

## Getting the historical data
