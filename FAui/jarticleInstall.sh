#!/usr/bin/env bash


/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3.9
pip3 install pandas==1.4.3
pip3 install Pillow==9.0.0
pip3 install schedule==1.1.0
pip3 install FairCore==4.3.1
pip3 install FairMongo==4.3.3
pip3 install FairNLP==4.1.0
pip3 install FairWeb==4.3.3
pip3 install fairarticle>=4.3.2
pip3 install fairqt>=1.2.0
pip3 install fairresources>=4.0.5
pip3 install flask
pip3 install flask-socketio
pip3 install pyngrok
python3 -m nltk.downloader punkt
python3 -m nltk.downloader vader_lexicon
python3 jarticleRun.py