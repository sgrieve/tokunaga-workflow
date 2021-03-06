#!/bin/bash

# $1 - shapefile name without .shp
# $2 - utm zone
# $3 - north or south

# Set up paths so we have a folder for each sub zone
cd /data/Geog-c2s2/toku/
mkdir $1
cd $1

# Download the tiles we need
python /data/home/faw513/tokunaga-workflow/processing/get_urls.py $1.shp | xargs -n 1 -P 8 wget -nv

# Build virtual raster from tiles
gdalbuildvrt input.vrt *.hgt

# Clip the merged raster using the corresponding shapefile
gdalwarp -multi -wo 'NUM_THREADS=val/ALL_CPUS' -srcnodata -32768 -dstnodata -9999 -cutline /data/home/faw513/tokunaga-workflow/climate_zones/singlepart_files_split/$1.shp -crop_to_cutline -of ENVI input.vrt tmp.bil

# Reproject the clipped raster to utm and save as a floating point file
gdalwarp -t_srs '+proj=utm +zone='$2' +datum=WGS84 +'$3'' -of ENVI -ot Float32 tmp.bil $1.bil

# Tidy up some temp files
rm tmp.*
rm *.hgt
rm *.vrt

# Run the LSD code
cd /data/home/faw513/LSDTopoTools2/src/lsdtt-drivers/

./strahler-hpc-basin.out /data/Geog-c2s2/toku/$1/ /data/Geog-c2s2/toku/$1/ $1

# Remove the raster files
rm /data/Geog-c2s2/toku/$1/$1.bil
rm /data/Geog-c2s2/toku/$1/$1.hdr
rm /data/Geog-c2s2/toku/$1/$1.bil.aux.xml
