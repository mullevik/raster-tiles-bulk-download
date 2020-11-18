#!/usr/bin/python

import sys
import os
import math
import urllib.request
import urllib.error
import os.path


def compute_tile_numbers(lat, lon, zoom):
    """
    The formula implemented based on
    https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#lon.2Flat_to_tile_numbers.
    Returns xtile, ytile (int, int).
    """
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad)))
                 / math.pi) / 2.0 * n)
    return xtile, ytile


def download(zoom, xtile, ytile, provided_url, output_dir):
    """
    Downloads specific /zoom/xtile/ytile.png tile
    from 'provided_url' into a file.
    Keeps the same directory structure inside the 'output_dir'.
    """
    url = provided_url + "/{}/{}/{}.png".format(zoom, xtile, ytile)
    dir_path = os.path.join(output_dir, "{}/{}/".format(zoom, xtile))
    download_path = os.path.join(output_dir,
                                 "{}/{}/{}.png".format(zoom, xtile, ytile))
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    if not os.path.isfile(download_path):
        try:
            print("downloading tile {}...".format(url), end="")
            source = urllib.request.urlopen(url)
            content = source.read()
            source.close()
            print(" done".format(url), end="")
        except urllib.error.HTTPError as e:
            print("Error when downloading tile {}, this tile was skipped ({})"
                  .format(url, str(e)), file=sys.stderr)
        except urllib.error.URLError as e:
            print("Error when trying to open {}, is the server even running? ({})"
                  .format(url, str(e)), file=sys.stderr)
        else:
            with open(download_path, 'wb') as destination:
                destination.write(content)
    else:
        print("skipping tile {} (already exists)".format(url))


def print_bar(total, current):
    current = (1. / total) * current
    line = 50
    current = int(line * current)
    print("[{}{}]".format("=" * current, " " * (line - current)))


def bulk_download(lat_s, lon_s, lat_e, lon_e, zoom_lb, zoom_ub, url,
                  output_dir="tiles"):
    assert zoom_lb <= zoom_ub
    assert zoom_lb >= 0
    assert zoom_ub <= 20
    assert lat_s > lat_e
    assert lon_s < lon_e

    total_tiles = 0
    count = 0

    for zoom in range(zoom_lb, zoom_ub + 1):

        xtile_s, ytile_s = compute_tile_numbers(lat_s, lon_s, zoom)
        xtile_e, ytile_e = compute_tile_numbers(lat_e, lon_e, zoom)

        amount_x = xtile_e + 1 - xtile_s
        amount_y = ytile_e + 1 - ytile_s
        total_tiles += amount_x * amount_y

    for zoom in range(zoom_lb, zoom_ub + 1):

        xtile_s, ytile_s = compute_tile_numbers(lat_s, lon_s, zoom)
        xtile_e, ytile_e = compute_tile_numbers(lat_e, lon_e, zoom)

        amount_x = xtile_e + 1 - xtile_s
        amount_y = ytile_e + 1 - ytile_s

        this_zoom_tiles = amount_x * amount_y
        print("zoom: {} tiles: {}-{} / {}-{} ({})"
              .format(zoom, xtile_s, xtile_e, ytile_s, ytile_e, this_zoom_tiles))

        for x in range(xtile_s, xtile_e + 1):
            for y in range(ytile_s, ytile_e + 1):
                download(zoom, x, y, url, output_dir)
                
                count += 1
                print_bar(total_tiles, count)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Bulk download raster tiles')
    parser.add_argument('--lat_start', action="store", dest="lat_s", type=float, help="Top left latitude")
    parser.add_argument('--lon_start', action="store", dest="lon_s", type=float, help="Top left longitude")
    parser.add_argument('--lat_end', action="store", dest="lat_e", type=float, help="Bottom right latitude")
    parser.add_argument('--lon_end', action="store", dest="lon_e", type=float, help="Bottom right longitude")
    parser.add_argument('--zoom_min', action="store", dest="zoom_lb", type=int, help="Minimal zoom level (included)")
    parser.add_argument('--zoom_max', action="store", dest="zoom_ub", type=int, help="Maximal zoom level (included)")
    parser.add_argument('--url', action="store", dest="url", type=str, help="URL of the server")
    parser.add_argument('--output_dir', action="store", dest="output_dir", type=str, default="tiles/", help="Output directory")

    args = parser.parse_args()
    bulk_download(args.lat_s, args.lon_s, args.lat_e, args.lon_e,
                  args.zoom_lb, args.zoom_ub,
                  args.url, args.output_dir)
