# tsdb
This is a series of python scripts to populate a time series database with selected analytics from a Qumulo cluster. The type of analytical data can be selected while running the scripts.

## Overview
TSDBs are databases that are optimized for time series data. Time Series Databases typically have a high transaction volume and, as such, are not practical for traditional relational database management software. 
TSDBs are great for queries for historical data, replete with time ranges and roll ups. With a TSDB, it is also easy to perform complex queries using mathematical functions (like min, max, average, mean, modulo, etc).

## Time Series Databases
The following is an incomplete list of the types of Time Series Databases available as open source. There are numerous additional TSDBs available for purchase. That list is not included in this document.
* [Blueflood](http://blueflood.io)
* [Druid](http://druid.io)
* [InfluxDB](http://influxdb.com)
* [KairosDB - built on top of Cassandra - fork of OpenTSDB](https://github.com/kairosdb/kairosdb)
* [Newts - built on Cassandra](https://github.com/OpenNMS/newts)
* [OpenTSDB - built on top of HBase](http://www.opentsdb.net/)
* [Prometheus](http://prometheus.io/)
* [SiteWhere](http://www.sitewhere.org/)
* [TSDB (Time Series Database)](https://code.google.com/p/tsdb/)
* [Graphite (with Carbon)](https://github.com/graphite-project/carbon)

This project will focus exclusively on using Graphite with Carbon as the time series database. If you wish to use another database, you will
have to modify the python scripts that capture the analytical data from the Qumulo cluster. Providing information on using another
time series database is outside the scope of this document.

## Displaying Time Series Data
Clearly, having the data is not the same as viewing the data. You will need to have some graphing software that can read your time series
database and graph the data in a pleasing format. The graphing software should be able to create bar, line, or point charts (or combine them). 
Additionally, it would be nice if it could do complex mathematical functions on your data for additional data points.

We have selected Grafana as the graphics engine as it creates truly beautiful dashboards composed of one or more graph panels.
and is completely open source. Grafana can be read about in detail at [Grafana.org](http://www.grafana.org)

Below are some example dashboards with graphs to give you an idea of what your environment could look like:

![dashboard_example](/README_images/dashboard_example.png)
![nice_dashboard](/README_images/nice_dashboard.png)

## Focus of this project
This project will demonstrate how to install, configure, and manage a time series database. We will show you how to install Graphite, Grafana, and 
the scripts to capture analytics from your Qumulo cluster. 

## Requirements
* Qumulo cluster and API credentials for the cluster
* Ubuntu Linux Server version 15 or above
* Ubuntu Linux Server must have continuous access to Qumulo cluster

### Installed on Ubuntu Server
The following software must be installed on the Ubuntu Server

* cron
* python 2.7
* Graphite Web and Graphite Carbon
* Django
* Postgres
* Apache Web Server
* Qumulo API python library
* Grafana
* TSDB analytics capture scripts

Other than cron and python, the following sections will describe how to install all of the software that you will need
to start capturing analytics from your Qumulo cluster and displaying that information using Grafana.

## Installation Steps
### 1. Install Graphite

Install Graphite by following these steps: [Install Graphite](READMEs/install_graphite.md)

### 2. Install Grafana

Install Grafana by following the steps listed on the [Grafana.org website](http://docs.grafana.org/installation/debian/)

#### Add a Grafana Data Source

Before you can access your Graphite database, you must add a data source to Grafana. Since Grafana can use multiple different types
of time series databases, you must add a data source that specifies that you are using Graphite as your time series database.

Install a [Grafana Data Source](http://docs.grafana.org/datasources/graphite/) for Graphite

### 3. Install Qumulo API python library

The Qumulo REST API python library is available directly from PyPi.

Simply run

```shell
  pip install -r requirements.txt
```

You can verify that you have the Qumulo REST API installed by running the following command at a command prompt:

```shell
  pip list
```

You should see something like the following output:

```shell
qumulo-api (1.2.17)
```

NOTE: The version number following the qumulo-api may be different than listed above.

### 4. Install the tsdb scripts

```shell
git clone git@github.com:Qumulo/tsdb.git
```

#### Add python paths to your .profile

You will need to modify your .profile to include a path
for the python libraries referenced in the tsdb python scripts. 

In your home directory on the Ubuntu server, edit the file .profile

```shell
vi ~/.profile
```

 and add the following lines:

```shell
#
# Python Path
#

export TSDBScripts="`pwd`/API_Software/tsdb"
export PYTHONPATH="$PYTHONPATH:$TSDBScripts"
```

This example assumes that you have downloaded the Qumulo API and tsdb scripts into a subdirectory
called "API_Software" within your home directory. Change appropriately if this is not the case.

### 5. A brief note about metrics

Time Series Databases typically only store three values; a Timestamp, a name, and a value. 
The "name" is called a metric.

The small amount of data stored is one of the primary reasons that a Time Series Database is so
fast. It is possible with a TSDB to read millions of data points (metrics) in the same time
that it would take to read hundreds of thousands of data points in a traditional relational database.

Metrics are simply names separated by periods (.). An example would be "filetype.jpg.count" and
"filetype.jpg.size". In this example, we can see that if you wish to store two datapoints on the
filetype of jpg, you would have to create two entries in your TSDB. One of those metrics would
use the name "filetype.jpg" and add "count" to form a complete metric of "filetype.jpg.count" and the other would add "size" to form a complete metric of "filetype.jpg.size". 

### 6. Scripts to populate TSDB

If you look in the directory created by downloading the TSDB scripts from github, you will 
find a subdirectory called "AggregatedTimeSeries".

The AggregatedTimeSeries scripts will use the aggregation api calls to retrieve directory 
level analytics from the Qumulo cluster. These api calls are extremely fast; typically on 
the order of only several milliseconds. 

#### AggregatedTimeSeries

This script will populate a TSDB with information from a single directory within the Qumulo 
cluster. Use this script for directories that you wish to track (I.E.: the entire root 
filesystem, home directories, project directories, etc).

The values populated within the TSDB are:

```shell
PREFIX.size
PREFIX.files.count
PREFIX.dirs.count
```

The name PREFIX in the above example is arbitrary. You will have the opportunity to change it in
the actual call to the script.

The arguments to the script are:

```shell
	usage: aggregated-time-series.py [-h] --cluster CLUSTER --metprefix METPREFIX
	                                 [--username USERNAME] [--password PASSWORD]
					 [--timehost TIMEHOST] [--rootdir ROOTDIR]

	where:

		--cluster CLUSTER = cluster DNS name or IP address
		--metprefix METPREFIX = value to store in place of word PREFIX in above example
		--username USERNAME = login name to cluster (default is admin)
		--password PASSWORD = login password to cluster (default is admin)
		--timehost TIMEHOST = DNS name or IP address to machine running TSDB
		--rootdir ROOTDIR = Directory from which to gather information to populate TSDB
```

There is a bash shell script in the same directory with some examples. Let's take a look at 
those examples:

```shell
vi aggregate.sh
```

```shell
#!/bin/bash                                                                                            

# Root                                                                                                 

python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "\
/" --metprefix "root.capacity"

# Movies                                                                                               

python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "\
/Movies/" --metprefix "movies.capacity"

# TV Shows                                                                                             

python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "\
/TV Shows/" --metprefix "tvshows.capacity"

# Users                                                                                                

python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "\
/Share/hazel/" --metprefix "user.hazel.capacity"
python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "\
/Share/madison/" --metprefix "user.madison.capacity"
python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "\
/Share/silas/" --metprefix "user.silas.capacity"
python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "\
/Share/walter/" --metprefix "user.walter.capacity"
python aggregated-time-series.py --cluster 192.168.49.135 --password a --timehost graphite --rootdir "\
/Share/kade/" --metprefix "user.kade.capacity"
```

This example bash shell script will populate the TSDB with several items. 

First, is the "root" 
filesystem. Since any aggregate contains a count of all objects and the total size of all objects, 
retrieving an aggregate at the root level (the "/" in a filesystem), you can expect to see the
total number of objects and the size of those objects for the entire filesystem.

Next are two projects directories; Movies and TV Shows.

Finally, we will retrieve information on several user home directories; Hazel, Madison, Silas,
Walter, and Kade.

What will we see in the TSDB? Let's pick one of the home directories and take a look at what will be 
placed into the TSDB. If we look at Hazel, you see that the metric prefix is "user.hazel.capacity".
What will be added is the count of the number of objects and the total size (or capacity) used for
those objects. So, ultimately, you will see "user.hazel.capacity.count" and "user.hazel.capacity.size"
written into the database.

### 7. Running the script automatically

It is recommended that you run the script to populate the TSDB through an automated system, such 
as cron.

A good method to do this would be to create a bash script, like the example show in this
documentation.

Then, edit the crontab and enter the bash scripta to run at the time period that you wish.

#### Crontab example

Here is an example of how to create a crontab entry for both the aggregate and datatype bash
scripts.

```shell
crontab -e
```

```shell
*/10 * * * * /home/kade/tsdb/aggregate.sh
```

In the above example, we will get information about the aggregates every 10 minutes.

