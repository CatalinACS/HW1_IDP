#!/bin/sh

influx -execute 'CREATE DATABASE "IoT_Devices"'
influx -execute 'ALTER RETENTION POLICY "autogen" ON "IoT_Devices" DURATION 0s'
