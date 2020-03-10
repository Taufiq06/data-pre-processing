## Solar Irradiance Retrieval and Pre-processing
This file describes the process used to retrieve and pre-process the [Global Solar Atlas Version 2](https://globalsolaratlas.info/download/world) for [display on Resource Watch](https://resourcewatch.org/data/explore/Solar-Irradiance).

Two datasets from this atlas were downloaded and pre-processed:
1) Average daily global horizontal irradiance (9 arcsec resolution)
2) Average daily photovoltaic power potential (30 arcsec resolution)

Below, we describe the steps used to process each of these files.

##### Average daily global horizontal irradiance (9 arcsec resolution)
1) Download the data from the [source website](https://globalsolaratlas.info/download/world). The files can be found near the bottom of the page. For global horizontal irradiation, the following High Resolution GIS Data files were downloaded:
  - EEN segment - *GHI, DIF, GTI, DNI - LTAy_DailySum (GeoTIFF)*
  - EES segment - *GHI, DIF, GTI, DNI - LTAy_DailySum (GeoTIFF)*
  - EN segment - *GHI, DIF, GTI, DNI - LTAy_DailySum (GeoTIFF)*
  - ES segment - *GHI, DIF, GTI, DNI - LTAy_DailySum (GeoTIFF)*
  - WN segment - *GHI, DIF, GTI, DNI - LTAy_DailySum (GeoTIFF)*
  - WS segment - *GHI, DIF, GTI, DNI - LTAy_DailySum (GeoTIFF)*
  - WWN segment - *GHI, DIF, GTI, DNI - LTAy_DailySum (GeoTIFF)*
  - WWS segment - *GHI, DIF, GTI, DNI - LTAy_DailySum (GeoTIFF)*
2) Unzip each of the downloaded files.
3) Upload only the *GHI.tif* file in each of these folders to an image collection in Google Earth Engine (GEE).
4) Mosaic all of the images together into a single, global image using the following GEE code:

```
//Load in image collection
var ic = ee.ImageCollection('users/resourcewatch/ene_031a_solar_irradiance_GHI);
//Mosaic image
var mosaic = ic.mosaic();
//Get projection
var projection = ic.first().projection();
var crs = projection.getInfo().crs;
var transform = projection.getInfo().transform;
//Save global bounds!
var rect = [-180, -89.9, 180, 89.9];
var bounds = ee.Geometry.Rectangle(rect,null,false);
//Export image
Export.image.toAsset({
  image: mosaic,
  description: 'GHI_250_mosaic',
  assetId: 'users/resourcewatch/ene_031a_solar_irradiance_GHI/GHI_250_mosaic',
  crs: crs,
  crsTransform: transform,
  region: bounds,
  maxPixels: 1e13
});
//Print one image from collection
print(ic.first());
//Print scale in meters at the equator
print(ic.first().projection().nominalScale());
Map.addLayer(mosaic);


```
##### Average daily photovoltaic power potential (30 arcsec resolution)
1) Download the data from the [source website](https://globalsolaratlas.info/download/world). The files can be found near the bottom of the page. For global horizontal irradiation, the following GIS Data files were downloaded:
  - PVOUT - Photovoltaic power potential - *PVOUT-LTAm_AvgDailyTotals(GeoTIFF)*
2) Unzip the downloaded file.
3) Upload each of the 12 tiff files in the folder to an image collection in GEE.
4) Mosaic all of the images together into a single, global image using the following GEE code:
```
//Load in image collection
var ic = ee.ImageCollection('users/resourcewatch/ene_031a_global_solar_atlas_PVOUT);
//Mosaic image
var mosaic = ic.mosaic();
//Get projection
var projection = ic.first().projection();
var crs = projection.getInfo().crs;
var transform = projection.getInfo().transform;
//Save global bounds!
var rect = [-180, -89.9, 180, 89.9];
var bounds = ee.Geometry.Rectangle(rect,null,false);
//Export image
Export.image.toAsset({
  image: mosaic,
  description: 'solar_PVOUT_mosaic',
  assetId: 'users/resourcewatch/ene_031a_global_solar_atlas_PVOUT/solar_PVOUT_mosaic',
  crs: crs,
  crsTransform: transform,
  region: bounds,
  maxPixels: 1e13
});
//Print one image from collection
print(ic.first());
//Print scale in meters at the equator
print(ic.first().projection().nominalScale());
Map.addLayer(mosaic);
```


You can view the processed, Solar Irradiance dataset [here](https://resourcewatch.org/data/explore/Solar-Irradiance).

You can also download original dataset [from the source website](https://globalsolaratlas.info/download/world).

###### Note: This retrieval of and preprocessing of data was documented by [Tina Huang](https://www.wri.org/profile/tina-huang).
