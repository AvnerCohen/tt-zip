#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <filename.mp4>"
  exit 1
fi

input_video="$1"
output_video="./output/zipped_${input_video}"


echo "🏓 - Extracting Audio."
ffmpeg -i $input_video -vn -acodec pcm_s16le -ar 44100 -ac 2 ${input_video}.wav

while IFS= read -r line; do
  time_ranges+=("$line")
done < <(python ball_on_table.py "$input_video")


filter_complex=""
for i in "${!time_ranges[@]}"; do
  start=$(echo "${time_ranges[$i]}" | cut -d'-' -f1)
  end=$(echo "${time_ranges[$i]}" | cut -d'-' -f2)
  echo "${start}-${end}"
  filter_complex+="[0:v]trim=start=$start:end=$end,setpts=PTS-STARTPTS[v$i];"
  filter_complex+="[0:a]atrim=start=$start:end=$end,asetpts=PTS-STARTPTS[a$i];"
done

filter_complex+="[v0][a0]"
for i in "${!time_ranges[@]}"; do
  if [[ $i -gt 0 ]]; then
    filter_complex+="[v$i][a$i]"
  fi
done
filter_complex+="concat=n=${#time_ranges[@]}:v=1:a=1[outv][outa]"

echo "🏓 - Generating zipped video."

ffmpeg -i "$input_video" \
  -filter_complex "$filter_complex" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -crf 18 -c:a aac -b:a 128k "$output_video"

echo "🏓 - Clean up."
rm -rf "${input_video}.wav"


echo "🏓 - Done - See ${output_video}"