#!/bin/bash 

for i in 1 2 3 4 5 6 7 8 9

do 
curl https://swapi.co/api/people/?format=json&page=$i > people_list$i.json
done
