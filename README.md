# Shithead

The card game [Shithead](https://en.wikipedia.org/wiki/Shithead_(card_game)) implemented in Python and PyGame.

![IMAGE](doc/img/screenshot.png)

## Requirements

```
sudo apt install git python-pip
```

## Installation


```
git clone https://github.com/rlefmann/Shithead.git Shithead
cd Shithead
sudo pip install .
```

## Usage

To get started, simply execute the shithead program by typing:

```
$ shithead
```

* Use the left and right arrow keys to move the cursor.
* Use the tab key to cycle through the different card collections.
* Press the space bar to select a card. You can also select multiple cards, but only if they are from the same collection (tab cycleing is blocked once a card is selected).
* Press return to play the selected cards. If you have selected the discard pile and pressed return you will take all the cards from it.
