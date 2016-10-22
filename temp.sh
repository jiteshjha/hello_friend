#!/bin/bash

rawurlencode () {
	local string="${1}"
	local strlen=${#string}
	local encoded=""
	local pos c o

	for (( pos=0 ; pos<strlen ; pos++ )); do
		c=${string:$pos:1}
		case "$c" in
			[-_.~a-zA-Z0-9] ) o="${c}" ;;
			* )  printf -v o '%%%02x' "'$c"
		esac
		encoded+="${o}"
	done
	echo "${encoded}"
  REPLY="${encoded}"
}

value="$(ruby -r cgi -e 'puts CGI.escape(ARGV[0])' "$1")"

curl \
  -H 'Authorization: Bearer R5BX657LFY5MGJA7FLWDRBXM34RC56JE' \
  "https://api.wit.ai/message?v=20161022&q="$value