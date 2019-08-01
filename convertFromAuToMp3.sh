for entry in *
do
	ffmpeg -i $entry ${entry/au/mp3}
done
