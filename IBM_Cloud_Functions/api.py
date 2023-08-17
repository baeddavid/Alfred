#!/usr/bin/env python

import sys
import json
import os, ibm_db, ibm_db_dbi as dbi, pandas as pd
import requests

def main(params):
    ## Database credentials
    db2_dsn = 'DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={uid};PWD={pwd};SECURITY=SSL'.format(
        'bludb',
        'XXXXX.databases.appdomain.cloud',
        'XXXXX',
        uid='XXXXXXX',
        pwd='XXXXXXX'
    )

    ## Database connection string
    db2_connection = dbi.connect(db2_dsn)

    ## SQL SELECT query
    query = 'SELECT * FROM "XXXXXXXX"."BUS_SCHEDULE"'

    ## Execute sql in database
    bus_df = pd.read_sql_query(query, con=db2_connection)

    ## Defining params for sql query
    bus_route = params['bus_route']
    bus_stop = params['bus_stop'].lower()

    ## Initialize response object
    response = {}

    ## Query response
    query_df = bus_df[(bus_df.BUS_ROUTE == bus_route) & (bus_df.BUS_STOP == bus_stop)]

    ## If query returned nothing
    if query_df.shape[0] <= 0:
        response = {"Error" : "There are no records available with this data"}
    ## Query found a match
    else:
        bus_route = query_df.BUS_ROUTE.item()
        bus_stop = query_df.BUS_STOP.item()
        bus_time = query_df.SCHEDULED_ARRIVAL_TIME.item()
        return_string = "Bus " + str(bus_route) + " is scheduled to arrive at " + bus_stop + " at " + str(bus_time)
        response = {"bus_message": return_string}
    ## Return the response
    return response
