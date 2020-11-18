# Bulk download for .png raster tiles

A simple python script for downloading .png raster tiles from a rendering server.

This script works only with the [Slippy map tile names](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#lon.2Flat_to_tile_numbers).
That is the ```http://127.0.0.1:8080/tile/z/x/y.png``` notation.

## Requirements

Python >=3

## Run it

### Example
```shell script
python bulk_download.py --lat_start 49.79 --lon_start 13.88 --lat_end 49.71 --lon_end 14.01 --zoom_min 1 --zoom_max 15 --url http://127.0.0.1:8080/tile
```

### Parameters

Required:
- ```--lat_start <float>``` top left latitude of selected area,
- ```--lon_start <float>``` top left longitude of selected area,
- ```--lat_end <float>``` bottom right latitude of selected area,
- ```--lon_end <float>``` bottom right longitude of selected area,
- ```--zoom_min <integer>``` minimal zoom level (included),
- ```--zoom_max <integer>``` maximal zoom level (included) (may equal to ```--zoom_min```),
- ```--url <string>``` static part of URL of the server (```http://127.0.0.1:8080/tile``` for the above example notation).

Optional:
- ```--output_dir <string>``` output directory name (relative to working directory) (default is ```tiles/```).


## When and when not to use this

The primary reason for existence of this script is to download small areas of
[OpenStreetMap](https://www.openstreetmap.org/) .png raster tiles for offline usage without rendering at all. 

This script can download large amounts of data from specified server.
It can't be used to download raster tiles from [public OpenStreetMap servers](https://tile.openstreetmap.org), 
because of [this reason](https://operations.osmfoundation.org/policies/tiles/) (this would be considered as a heavy use).

This script is meant for downloading rendered raster tiles from a server,
which is owned by the user of this script. An example usage would be a combination of
setting your own local OSM raster tile serving server, 
which is well described [here](https://switch2osm.org/serving-tiles/),
and than downloading the raster tile images via this script.

Note that raster tiles have significant file size. When a larger zoom level is specified, the amount of tiles for
even a small area may be enormous. Make sure to check the storage capacity of your machine when downloading higher zoom levels.