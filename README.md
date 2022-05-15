# Text_to_speech spring project
___

Text to speech for JB Academy

## Installation
___
for LinuxOS:
```
pip install tts

pip install --upgrade numpy
   
pip install pandas
```
if you have problems installing tts, see [tts-doc](https://tts.readthedocs.io/en/latest/installation.html)

## Make samples
___

1) prepare samples with `./main.py data/<path_to_sample>` 

   you can use *.csv (for many samples) or *.txt (for one sample) files, it will be save in **samples/**

2) run tts with `./run.sh samples/<path_to_sample>`
