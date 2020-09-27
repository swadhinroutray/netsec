#!/bin/bash

chmod +777 SCAN.txt
sed -r 's/\x1b\[[0-9;]*m//g' SCAN.txt > SCANclean.txt
sed '/^$/d' SCANclean.txt > finalResult.txt
cat SCANclean.txt
echo "Cleaned PySSLscan output"