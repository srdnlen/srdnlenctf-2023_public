# _Foren_AudioChall SrdnlenCTF '23 WP_

###### First step: spectrum analysis
As a first step, we open the audio file with a spectrum analyzer (in this case was used sonic visualizer https://www.sonicvisualiser.org/). 

Observing the first part of the spectrum, a typical pattern of SSTV radio signals
can be recognized, with MARTIN-1 encoding.
###### Second step: decode the signal and recover the password
Once you understand what type of encoding was used you can proceed to its decoding (Most decoding tools can recognize it automatically saving you the time of the search for the type of encoding),
the signal given is in a file of WAV format so you have to find a tool that supports this type of file (for example qsstv on Linux).
Once decoded the image will show inside a string that is NOT the challenge flag but the password for the second part.

###### Third step: Extract the hidden folder
With binwalk(```binwalk -e <filename>```) we check if there is any file hidden in the .wav, after a quick check we find a file .rar , opening it we will be asked to enter the password to unlock the file "flag.png" and finally the challenge is resolved!
```
(material for further information here: https://www.sigidwiki.com/wiki/Slow-Scan_Television_(SSTV) ). 
```
