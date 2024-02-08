#!/bin/bash

artists=("Queen" "Queen" "Queen" "The Beatles" "The Beatles" "The Beatles" "The Rolling Stones" "The Rolling Stones" "The Rolling Stones")
songs=("Bohemian Rapsody" "We Will Rock You" "Radio Gaga" "Come Together" "Let it Be" "Here Comes the Sun" "Sympathy For The Devil" "Angie" "Satisfaction")

for i in "${!artists[@]}"; do
    artist="${artists[i]}"
    song="${songs[i]}"

   awslocal dynamodb put-item \
      --table-name MusicTable \
      --item '{
          "Artist": {"S": "'"$artist"'"},
          "Song": {"S": "'"$song"'"}
        }' \
      --return-consumed-capacity TOTAL
    sleep 1
done
