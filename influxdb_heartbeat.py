#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""InfluxDB client test"""

import argparse
import commands

from influxdb import InfluxDBClient

from datetime import datetime, timedelta

def seconds_past(datetime, seconds):
    return (datetime < datetime.now() - timedelta(seconds=seconds))


def sensor_data(controller, value, tags={}):
    ident = controller
    data = {
        "measurement": str(ident),
        "time": (
            datetime.utcnow().replace(microsecond=0).isoformat() +
            "Z"),
        "tags": tags,
        "fields": {"value": value, }
    }
    return data
    
def main(host='CHANGEME', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'CHANGEME'
    password = 'CHANGEME'
    dbname = 'CHANGEME'

    client = InfluxDBClient(host, port, user, password, dbname)

    cpu_load = commands.getoutput("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'")

    #print("Querying data: " + query % cpu_load)
    #result = client.query(query)

    #print("Result: {0}".format(result))

    data = sensor_data(
                "CHANGEME",
                cpu_load,
                {"type": "cpu_load" }, )
    client.write_points([data])
    print("published to influx", data)
    
    def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='CHANGEME',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
