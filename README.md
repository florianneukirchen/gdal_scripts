# Hopefully helpful scripts for geodata

## Sentinel Layerstack
Use ZIP files downloaded from Coperincus Dataspace to create a mosaiced VRT 
layerstack with a given resolution. Uses the jp2 files avaible in the Graticule folder
without any resampling (but note that there are already downsampled versions). Also add the band number as band description (very helpful in QGIS).

For stack with the 20 m resolution jp2 files:
```
sentinel-layerstack.py *.zip
```
And simply open the vrt file in QGIS.

See `sentinel-layerstack.py -h` for more options.
