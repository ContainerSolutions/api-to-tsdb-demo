#!/usr/bin/env python
# Copyright (c) 2013 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
# -----------------------------------------------------------------------------
# aggregated-time-series
#
# Routine to get a directory aggregation and populate a time series database. 
#
# Items populated:
#
# 1. A SINGLE directory aggregation. File and directory counts and sizes


'''
=== Required:

[--cluster] ip|hostname        An ip address or hostname of a node in
                               the cluster; use 'localhost' when
                               running directly on the node

[--metprefix] prefix           A name to use as the prefix for all metrics created.

=== Options:

[--username] username          Use 'username' for authentication
                                   (defaults to 'admin')
[--password] password          Use 'password' for authentication
                                   (defaults to 'admin')
[--timehost] ip|hostname       An ip address or hostname of the machine running
                               the time series database
[--rootdir] directory          The root directory to start the treewalk

'''

# Import python libraries

import sys
import time
import argparse

# We will send metrics to carbon via a plain ole socket

import socket

# Import Qumulo REST libraries

from qumulo.rest_client import RestClient

#
# Routine to return seconds since the start of computing... This is used
# by the time series database

def secs ():

    cur_secs = time.time()
    return int(cur_secs)

#
# Routine to build an entry in a dictionary
#

def dict_entry (entry, entry_time, entry_name, entry_value):

    try:
        d = list(entry[entry_name]['points'][0])
            
        d[1] += int(entry_value)
        entry[entry_name]['points'][0] = tuple(d)

    except KeyError:
        entry[entry_name] = {}

        d = entry[entry_name]
        d['name'] = entry_name
        d['points'] = [(entry_time, int(entry_value))]

#
# Main Routine

def main():
    
    # Build and get the command line

    parser = argparse.ArgumentParser (description = 'Aggregated Time Series Database')
    parser.add_argument ('--cluster', required = True, help = 'The hostname of the Qumulo cluster')
    parser.add_argument ('--metprefix', required = True, help = 'A prefix for storage of metrics in DB')
    parser.add_argument ('--username', default = "admin", help = 'Qumulo API username')
    parser.add_argument ('--password', default = "admin", help = 'Qumulo API password')
    parser.add_argument ('--timehost', default = "localhost", help = 'Time Series Database Host')
    parser.add_argument ('--rootdir', default = "/", help = 'Root directory to aggregate from')

    args = parser.parse_args()

#
# Initialize REST client to Qumulo

    try:
        rc = RestClient (args.cluster, 8000)
        rc.login (args.username, args.password)
    except:
        print "Unable to login to Qumulo API. Please check your cluster name and credentials."
        sys.exit()

# Let's open the socket to the TS DB

    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect ((args.timehost, 2003))
        print "Connected to Carbon"
    except socket.error as e:
        print "Failed to connect to Carbon at %s:%s with error %e" % (args.timehost, 2004, e)
        sys.exit()

#
# Get current seconds for timestamp

    start_sec = secs()

#
# Create the original dictionary that will hold all of our items

    entry = {}

# Get information from the aggregate on the total size of the storage, plus
# number of files and directories

    try:
        res = rc.fs.read_dir_aggregates (path = args.rootdir, recursive = False, max_entries = 10, max_depth = 1, order_by = "total_blocks")

        dict_entry (entry, start_sec, args.metprefix + '.size', res['total_capacity'])
        dict_entry (entry, start_sec, args.metprefix + '.files.count', res['total_files'])
        dict_entry (entry, start_sec, args.metprefix + '.dirs.count', res['total_directories'])
    except Exception as e:
        print "Error on read directory aggregates. Error = %s" % (e)
        sys.exit ()

#
# At this point, we have all of our data...
#
# Let's go and build a json entry to send to the TS DB

    for value in entry.values():
        metric_name = value['name']
        metric_value = value['points'][0][1]
        metric_time = value['points'][0][0]

        # Write to the TS DB

        mesg = "%s %s %s\n" % (metric_name, str(metric_value), str(metric_time))

        try:
            sock.sendall (mesg)
        except socket.error as e:
            print "Failed to send data to Carbon server: %s" % (e)
            try:
                sock.reconnect ()
            except socket.error as e:
                print "Could not reconnect to Carbon server: %s" % (e)
                sys.exit ()

#
# This is the main routine...
#

if __name__ == "__main__":
    sys.exit (main())
