## Global Bus Rapid Transit Dataset Pre-processing
This file describes the data pre-processing that was done to [the Global Bus Rapid Transit](https://brtdata.org/) for [display on Resource Watch](https://resourcewatch.org/data/explore/Cities-with-Bus-Rapid-Transit).

The Global Bus Rapid Transit (BRT) data can be found on the source website. The data is, however, not downloadable from the source website. The data includes the name of the BRT system, the year it commenced, the location of the BRT (city and region), and the source. Each of these values are provided for BRT systems launched between 1986 and 2019. 

Because we wanted to display the data on Resource Watch for all the BRT systems, a complete dataset was compiled from the data found on the source website and coordinates were joined from another dataset for mapping purposes. 

Below, we describe the actions taken to compile a complete dataset and join coordinates to the cities:
1. Copy and paste the data table from the source website to an Excel table.
2. Join the Global Bus Rapid Transit data (“cit_043_bus_rapid_transit”) with the “city_centroid” dataset on Resource Watch’s Carto account over the “city” column with the following SQL statement:
```
SELECT city_centroid.city, cit_043_cities_with_bus_rapid_transit.city, city_centroid.the_geom, cit_043_cities_with_bus_rapid_transit.source, cit_043_cities_with_bus_rapid_transit.value, cit_043_cities_with_bus_rapid_transit.country
FROM "wri-rw".city_centroid
INNER JOIN cit_043_cities_with_bus_rapid_transit ON city_centroid.city= cit_043_cities_with_bus_rapid_transit.city;

```
You can view the processed Global Bus Rapid Transit (BRT) dataset [on Resource Watch](https://resourcewatch.org/data/explore/Cities-with-Bus-Rapid-Transit).

You can also download original dataset [from the source website](https://brtdata.org/indicators/systems/year_system_commenced).

###### Note: This dataset processing was done by [Ken Wakabayashi](https://www.wri.org/profile/ken-wakabayashi), and QC'd by [Liz Saccoccia](https://www.wri.org/profile/liz-saccoccia).
