#!/bin/bash

value="$(ruby -r cgi -e 'puts CGI.escape(ARGV[0])' "$1")"

curl \
  -H 'Authorization: Bearer R5BX657LFY5MGJA7FLWDRBXM34RC56JE' \
  "https://api.wit.ai/message?v=20161022&q="$value

echo " "