# Didi Filter

## About

This program is meant to be an advanced version of the known snapchat filter where there are random images spinning on top of people's heads. The main improvement is that you can not only select the images you want to choose from and the caption, but you can also play it with friends (recognizing more than 1 face at the same frame).

This repository is meant to be easily customizable. Any person is able to create their own filter by creating a folder with the images they want within a folder with 1, 2, ... based on the number of people they are meant to be used (apart from when backwardCompatible flag is enabled). And that's pretty much it.

## Install
In order to install all libraries used by this repository, you must run
```
pip install -r requirements.txt
```

## Usage

The usage can be seen below:

<img width="1113" alt="Captura de ecrã 2020-04-18, às 17 44 22" src="https://user-images.githubusercontent.com/25267873/79645318-812d3800-81a6-11ea-9a17-461165cba8f7.png">

Some examples are:
```
./didifilter.py --locationFolder=celebrities --caption='What celeb am I?' --max=2 -v --video="exampleVideo"
```

```
./didifilter.py --locationFolder=pokemons --caption="Who's this pokemon?" --width=250 --height=150 --max=1 -p
```

## Example
```
./didifilter.py --location=memes --caption='Which meme am I?' --initial=30 --final=50 -b --max=3
```

![](example.gif)

<img width="1145" alt="didifilterPic" src="https://user-images.githubusercontent.com/25267873/79651993-74f6aa00-81a9-11ea-8081-2abb7051d833.png">


# Extra

The good thing about this is that you can customize the final outcome. Here's me pranking my girlfriend with psyduck when the query was: "What celebrity am I?"

![](meg_psyduck.gif)


## Support <a name="Support"></a>

If you like this project, feel free to buy me a coffee!

<a href="https://www.buymeacoffee.com/didierlopes" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-yellow.png" alt="Buy Me A Coffee" height="41" width="174"></a>
