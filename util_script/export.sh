#!/bin/bash

# Variables
DB_FILE="./Data-Store.db"
EXPORT_FILE="blackbox_until_last_month.csv"

# Export data until last month with headers and handle multiline Thermal data
sqlite3 $DB_FILE <<EOF
.headers on
.mode csv
.output $EXPORT_FILE
SELECT 
  Humidity,
  IPAddress,
  ImgRef,
  Motion,
  Temperature,
  REPLACE(Thermal, CHAR(10), ' ') AS Thermal, 
  timestamp,
  flag,
  image,
  location,
  brightness
FROM 
  blackbox 
WHERE 
  timestamp < date('now', 'start of month', '-1 month');
.output stdout
EOF

# Compress exported file
gzip $EXPORT_FILE
                                                                                                                      1,1           Top
