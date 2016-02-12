#!/bin/bash

while read word excess_data || [[ -n $p ]]; do 
	echo $word
	wget -q -O - "$@" http://www.merriam-webster.com/dictionary/$word | grep '<p class="definition-inner-item"' | 
		grep '<em>' | 
		grep -v "primary-content" | 
		awk '{gsub("<em>", "");print}' |
		awk '{gsub("</em>", "");print}' |
		awk '{gsub("<li>", "");print}' |
		awk '{gsub("</li>", "");print}' |
		awk '{gsub("&lt;", "");print}' |
		awk '{gsub("</p>", "");print}' |
		awk '{gsub("</ol>", "");print}' |
		awk '{gsub("<br />", "");print}' |
		awk '{gsub("<p", "");print}' |
		sed 's#class="definition-inner-item">#BEGIN #g' |
		tr BEGIN '\n' | 
		sed  '/^$/d'
done <$1


