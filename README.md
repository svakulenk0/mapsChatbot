# Maps Chatbot

Chatbot that helps you to find routes through Google API

## Requirements

* [googlemaps](https://github.com/googlemaps/google-maps-services-python)

'''
pip install -U googlemaps
'''

## Setup

* Create settings.py and save the API_KEY in the variable there.

```
cp settings.py.template settings.py
```

* Set simlink to this folder as an [opsdroid]() skill (in ~/.local/share/opsdroid/opsdroid-modules/skill on Linux)
```
ln -sfn ~/mapsChatbot mapsChatbot
```

* Connect to [Facebook](https://github.com/opsdroid/connector-facebook)

https://www.communidata.at:5008/connector/facebook
https://mapschatbot.communidata.at/connector/facebook


## Similar projects

* [MapBot](https://github.com/vishakha-lall/MapBot)
