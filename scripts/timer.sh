#!/bin/bash

while true
do
IS_AZURE_CASB_SERVICE_ACTIVE=$(systemctl is-active azure_casb.service)
if [ "$IS_AZURE_CASB_SERVICE_ACTIVE" == "active" ];then
  sleep 5
else
  sleep 20
  systemctl restart azure_casb.service
fi

done