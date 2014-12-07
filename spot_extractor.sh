#!/bin/bash
cd /home/spider_user/spider_alert/
pattern="DX de"
script -q -c '(/spider/src/client db0sbx)' >&1 |  while read line;
do
  if [[ "$line" == *$pattern* ]]
  then
    ./SpiderAlert.py -m \""${line%?}"\" >/dev/null;
  fi
done