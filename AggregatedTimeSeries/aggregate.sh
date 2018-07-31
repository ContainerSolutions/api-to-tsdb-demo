#!/bin/bash

# Root

python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "/" --metprefix "root.capacity"

# Movies

python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "/Movies/" --metprefix "movies.capacity"

# TV Shows

python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "/TV Shows/" --metprefix "tvshows.capacity"

# Users

python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "/Share/hazel/" --metprefix "user.hazel.capacity"
python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "/Share/madison/" --metprefix "user.madison.capacity"
python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "/Share/silas/" --metprefix "user.silas.capacity"
python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "/Share/walter/" --metprefix "user.walter.capacity"
python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "/Share/kade/" --metprefix "user.kade.capacity"

