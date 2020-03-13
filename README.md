This program is meant to be an advanced version of the known snapchat filter where there are random images spinning on top of people's heads. The main improvement is that you can not only select the images you want to chose from and the quote, as you can play it for more than people SIMULTANEOUSLY.

This repository is meant to be easily customizable. Any person is able to create their own filter by creating a folder with the images they want within a folder with 1, 2, ... based on the number of people they are meant to be used (apart from when backwardCompatible flag is enabled). And that's pretty much it.

The usage can be seen below:

<img width="1111" alt="Captura de ecrã 2020-03-11, às 00 06 08" src="https://user-images.githubusercontent.com/25267873/76369663-2c3b0e00-632c-11ea-83d6-4bc3f8965281.png">

Note: After each run, the settings are print in order to understand what configuration is being used.

Some examples of runs are:
./didiFilter.py --locationFolder=memes/ --query='Which meme am I?' --initialTime=30 --finalTime=50 -b --maxPeople=3

./didiFilter.py --locationFolder=pokemons/ --query="Who's this pokemon?" --width=250 --height=150 --maxPeople=1

./didiFilter.py --locationFolder=dragonBall/ --query='What DBZ character am I?' --maxPeople=2

Hope you have fun with it! Would be keen to see what have you used this for


Things to do:
 - fix error with -b flag
 - record a video
 - take a picture 
 - probably add both these to a folder? like results/pictures and results/videos ?
