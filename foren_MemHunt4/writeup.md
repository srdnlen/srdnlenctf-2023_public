## MemHunt 4

We have a dump of a RAM and we have to find what has happened. 
This challenge can be solved both using volatility 2 and volatility 3

### Solution
In the description we know that everything went black with white strings again. But from the process tree and from the decoded powershell script, we know that there is a file called scvhost.exe running. This a new "vulnerability" some malware are using. The legitimate process is called svchost.exe which manages every service in Windows. Some new threats are changing the order of c and v in the name of their malware to not be "easily" decoded.

We can analyse first the scvhost.exe memory by dumping it:

Volatility2 command:
```
python2 vol.py -f memdump.mem --profile=Win10x64_19041 memdump -p 1596 -D .
```

Volatility3 command:
```
python3 vol.py -f memdump.mem windows.memmap.Memmap --pid 1596 --dump
```
First we try if the flag is clearly written in the process memory area with

```
strings 1596.dmp | grep "srdnlen"
```

Here is the last flag: **_srdnlen{RealMlwr_IncidentResponse}_**
