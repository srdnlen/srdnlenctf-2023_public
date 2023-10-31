# srdnlenctf 2023

## MemHunt 1

We have a dump of a RAM and we have to find what has happened. 
This challenge can be solved both using volatility 2 and volatility 3

### Solution

If we use Volatility 2 the first thing is find the profile. We use "imageinfo" command and we get Win10x64_19041. It is important to get the profile because we need to use it for every plugin in Volatility2.
To better understand and reconstruct the incident, we can use pstree command for Volatility2 and windows.pstree.PsTree for Volatility3.
We get different processes but we have a very interesting tree:

Here is the output from Volatility2
```
.. 0xffffbf080cebb080:explorer.exe                   4536   4476     60      0 2023-10-25 07:43:30 UTC+0000
... 0xffffbf080d9a9080:ida64.exe                     6752   4536      5      0 2023-10-25 07:43:52 UTC+0000
... 0xffffbf080d8e70c0:POWERPNT.EXE                  6308   4536     35      0 2023-10-25 07:44:47 UTC+0000
.... 0xffffbf080ae9d300:powershell.exe               2744   6308     25      0 2023-10-25 07:45:09 UTC+0000
..... 0xffffbf080ce0d080:scvhost.exe                 1596   2744      4      0 2023-10-25 07:45:36 UTC+0000
...... 0xffffbf080d039080:conhost.exe                2136   1596      7      0 2023-10-25 07:45:36 UTC+0000
..... 0xffffbf080a9df0c0:conhost.exe                 2668   2744      8      0 2023-10-25 07:45:09 UTC+0000
.... 0xffffbf080d351080:ai.exe                       3732   6308     12      0 2023-10-25 07:44:50 UTC+0000
... 0xffffbf080d7da340:msedge.exe                    5584   4536     61      0 2023-10-25 07:43:44 UTC+0000
```

Here is the output from Volatility3
```
** 4536 4476    explorer.exe    0xbf080cebb080  60      -       1       False   2023-10-25 07:43:30.000000      N/A
*** 6752        4536    ida64.exe       0xbf080d9a9080  5       -       1       False   2023-10-25 07:43:52.000000      N/A
*** 6308        4536    POWERPNT.EXE    0xbf080d8e70c0  35      -       1       True    2023-10-25 07:44:47.000000      N/A
**** 2744       6308    powershell.exe  0xbf080ae9d300  25      -       1       True    2023-10-25 07:45:09.000000      N/A
***** 2668      2744    conhost.exe     0xbf080a9df0c0  8       -       1       False   2023-10-25 07:45:09.000000      N/A
***** 1596      2744    scvhost.exe     0xbf080ce0d080  4       -       1       False   2023-10-25 07:45:36.000000      N/A
****** 2136     1596    conhost.exe     0xbf080d039080  7       -       1       False   2023-10-25 07:45:36.000000      N/A
**** 3732       6308    ai.exe  0xbf080d351080  12      -       1       False   2023-10-25 07:44:50.000000      N/A
```

We see that a PowerPoint has been opened with explorer.exe (process to manage folders in Windows) and this PowerPoint generates a powershell process which makes a connection (conhost.exe) and this one runs a process called scvhost.exe which makes another connection (conhost.exe).

As the challenge asks to find what has been written in the PowerPoint, we can dump the memory of POWERPNT.EXE process

Volatility2 command to dump the process memory:

``` 
python2 vol.py -f memdump.mem --profile=Win10x64_19041 memdump -p 6308 -D .
```

But the memory could also be dumped with the following volatility3 command:

```
python3 vol.py -f memdump.mem windows.memmap.Memmap --pid 6308 --dump
```

When we dump the memory of a process, the dump has specific syntax and for example in PowerPoint the data in a slide is written in a json format. We can make strings from the saved dump and look for the json or grep for "slides" with option -A (which means after each found occurence) and a specific number of lines such as 10. Otherwise we can hope that the written element is something related to srdnlen and hence make a grep about "srdnlen".
We find the flag: **_srdnlen{w3lc0m3_T0:IncidentResponse}_** inside a json data

``` json
{"slides":[{"id":"<pc:sldMkLst xmlns:pc=\"http://schemas.microsoft.com/office/powerpoint/2013/main/command\" xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" xmlns:ac=\"http://schemas.microsoft.com/office/drawing/2013/main/command\"><pc:docMk/><pc:sldMk cId=\"2855356155\" sldId=\"256\"/></pc:sldMkLst>","mk":{"sId":256,"cId":2855356155},"drawingElems":[{"id":"<ac:txBodyMkLst xmlns:pc=\"http://schemas.microsoft.com/office/powerpoint/2013/main/command\" xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" xmlns:ac=\"http://schemas.microsoft.com/office/drawing/2013/main/command\"><pc:docMk/><pc:sldMk cId=\"2855356155\" sldId=\"256\"/><ac:spMk id=\"3\" creationId=\"{BD672C7B-0385-C842-B228-5890252993AB}\"/></ac:txBodyMkLst>","mk":{"id":3,"cId":"{BD672C7B-0385-C842-B228-5890252993AB}","type":"shape"},"textTile":{"elements":[{"text":"srdnlen{w3lc0m3_T0:IncidentResponse}\r","languageId":"it-IT","spans":[{"languageId":"en-GB","start":36,"length":1,"doNotProcess":false}]}]}}]}]}
```
