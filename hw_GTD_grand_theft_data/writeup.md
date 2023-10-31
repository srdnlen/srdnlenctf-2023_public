# Writeup (parts 1, 2, 3)

## Part 1: Hardware

How to approach the first part of the hardware? The challenge description provides the 'netcat' command along with the address where the service is listening.

When connecting for the first time to the address, what appears is:
```plaintext
Welcome to the USB2Parallel CLI!
Checking drivers...done
Checking devices.found 1 device with serialID: YEZSEOOS
Device info:
	Chip 74x6969
	Manufacter: srdnlen
	Input alias: OP (32bit wide)
	Output alias: AVB|STATUS|DATA_OUT (8bit wide)
op[32] <= 
```
You will be asked to input a 32-bit input (or 4 bytes). Trying various inputs, you can notice that it only accepts binary inputs.

When looking at the provided datasheet as an attachment, we can see some interesting sections:
* Pinout: because you can read what each pin does;
* OPCODES: because it provides a list of accepted opcodes and how to use them;
* Disclaimer: because it gives a clue about the various opcodes.

> The clue that hides the disclaimer is the sentence: _'It is important to note that the design of the 6969 chip is still in an experimental phase and may be subject to changes.'_
> 
> It foreshadows the content of the opcode table where it indicates whether an opcode is stable or not.

The important pins in the pinout section are:
* op(32): Input pin, takes the opcode and various values.
* data_out(8): Output pin, returns the response byte when avb is 1.
* status: Output pin, set to one when there is an internal error.
* avb: Output pin, set to one when a byte is available for reading.

To understand how the integrated circuit behaves in actuality, you need to read the opcode table. Knowing that some opcodes are not stable, it's better to filter them out and focus on the stable ones. Creating a list, we have:

* Get constant values
* Empty cells
* Read from external EEPROM

Plus two reserved opcodes. Looking at the available opcode list, you can immediately eliminate the opcode to empty cells as it's of no use. The command to obtain constant names might be useful, but there is no opcode that has the capability to retrieve the values of each one. What remains is the opcode for reading from the external EEPROM.

So, by reading the opcode description _'This command reads byte from the external EEPROM. To do this, it is necessary to define the byte target address into the bits from 18 to 0'_ and by understanding how the op pins should be set, _'The operation signal for a 32-bit operation space, which specifies the specific operation that the device is performing on data. The first 4 bits of this signal represent the opcode, which determines the type of operation to be performed. The next 8 bits represent the address of the register. The remaining 20 bits represent the value of the register,'_ we have the opportunity to send the first command for testing.

> Note the fact that the values of the bits that should make up the register address are not specified. This is because the opcode acts directly.

opcode|register|value
:---:|:---:|:---:
1100|x|0 - (8*1024-1)

> The challenge description mentions an 8KB EEPROM connected to the chip.

Let's take an example by requesting byte 0 from the EEPROM:

```plaintext
Welcome to the USB2Parallel CLI!
Checking drivers...done
Checking devices.found 1 device with serialID: TABHDTZF
Device info:
	Chip 74x6969
	Manufacter: srdnlen
	Input alias: OP (32bit wide)
	Output alias: AVB|STATUS|DATA_OUT (8bit wide)
op[32] <= 11000000000000000000000000000000
avb|status|data_out[8] => 1001001001
op[32] <= 
```

The returned value is 1001001001: where the first bit is the avb pin, the second is the status bit, and the remaining 8 bits are the byte of interest.

Following this principle, it's possible to create a program that performs a dump of the entire EEPROM memory using `pwntools`.

```python
from pwn import *

# Here I configure my connection constants
host = '172.17.0.1'
port = 42069

# I create a connection object
conn = remote(host, port)
conn.recvuntil(b'op[32] <= ')

# List to store all of the bytes
resp = []

# view the notes to know why there is a try-except block
try:
    # from 0 to 8*1024-1
    for i in range(8 * 1024):
        print(f'Receiving byten {i}')
        # send the address line with the opcode
        conn.sendline(b'11' + bin(i)[2:].zfill(30).encode('ascii'))
        # It receives until it encounters another input request
        tmp = conn.recvuntil(b'op[32] <= ') # -> 'avb|status|data_out[8] => 1001001001\n'
        # splits it
        # 1. ['avb|status|data_out[8] ', '1001001001\n']
        # 2. tmp = 1001001001
        tmp = tmp.split(b'=> ')[1].split(b'\n')[0] 
        # remove the first two bits and transform the byte into chars
        tmp = tmp[2:].decode('ascii')
        resp.append(int(tmp, 2)) # converting binary string into a int value
except:
    pass

# closing connection
conn.close()

# trasforming all of the values into bytes
ba = bytes(resp)
with open('eepromdump.bin', 'wb') as file:
    file.write(ba) # and saved into a binary file

print('Done! eepromdump.bin')
```

### Note
I would like to thank [@auguzanellato](https://github.com/augustozanellato) for pointing out the fact that immediately after reaching the last 'valid' address (where actual data was stored), the server stopped responding. This caused a halt in the input flow right after dumping the program present in the EEPROM.

Immediately after receiving the ticket, the bug was fixed, ensuring that the server was dumped all the way to address 8191.

## Part 2: crypto

Now that we have the file, running a simple `file eepromdump.bin` command won't show much. But trying to open it with 'xxd' instead:

```plaintext
$ xxd -C eepromdump.bin
00000000: 497c 7a7f 3738 3739 3639 3639 3639 3639  I|z.787969696969
00000010: 3439 6539 3739 3639 3639 3639 0239 3639  49e979696969.969
00000020: 6233 3639 3339 3639 0239 1639 3539 1e39  b3693969.9.959.9
00000030: 3139 3039 3739 3639 a239 3639 3639 3639  19097969.9696969
00000040: 3639 3639 f231 3639 f231 3639 3339 3639  6969.169.1693969
00000050: 3439 3639 3739 3639 6e30 3639 3638 b639  49697969n06968.9
00000060: f231 3639 6e39 3639 6e39 3639 3039 3639  .169n969n9690969
00000070: 3739 3639 3739 3639 3639 3639 6e38 b639  796979696969n8.9
00000080: 6e38 b639 3639 3639 3039 3639 3039 3639  n8.9696909690969
00000090: 3739 3639 3aad 0239 3aad 6739 3aad 6739  7969:..9:.g9:.g9
000000a0: 3aad 6739 3aad 6739 3aad 6739 3aad 6739  :.g9:.g9:.g9:.g9
000000b0: 3aad 6739 3aad 6739 3aad 6739 3aad 6739  :.g9:.g9:.g9:.g9
000000c0: 3aad 6739 3aad 6739 3aad 6739 3aad 6739  :.g9:.g9:.g9:.g9
000000d0: 3aad 6739 3aad 6739 3aad 6739 3aad 6739  :.g9:.g9:.g9:.g9
000000e0: 3aad 6739 3aad 6739 3aad 6739 3aad 6739  :.g9:.g9:.g9:.g9
000000f0: 3aad 6739 3aad 6739 3aad 6739 271d 2987  :.g9:.g9:.g9'.).
00000100: f9d6 eed9 e886 fb86 27d9 96d9 87d9 d2d5  ........'.......
00000110: ced9 34f9 33a9 3bab 9e0c 873e efce 17d9  ..4.3.;....>....
00000120: 9edc 87d9 37f9 2bab 980c 843e d7ce 38ad  ....7.+....>..8.
00000130: 7b3a 3aad 733d 3aad 3639 aa38 cd38 5d08  {::.s=:.69.8.8].
00000140: 473c 3ec9 3eac df62 cd76 1436 0526 ff38  G<>.>..b.v.6.&.8
00000150: 3aad ac3a b165 a17b 3eac b169 ac76 3eac  :..:.e.{>..i.v>.
00000160: b562 a67d 3eac b366 ae70 3eac b364 aa76  .b.}>..f.p>..d.v
00000170: 3eac bf6b a276 3eac bb64 ab77 3eac b16b  >..k.v>..d.w>..k
00000180: a07f 3eac b969 a277 3eac bb6c a77d 3eac  ..>..i.w>..l.}>.
00000190: bd68 a57a 3eac bb69 a47b 3eac b367 a477  .h.z>..i.{>..g.w
000001a0: 3eac b56b aa73 3eac b962 a577 3eac b566  >..k.s>..b.w>..f
000001b0: ab77 3eac b165 ac7d 3eac b76b a771 3eac  .w>..e.}>..k.q>.
000001c0: b562 a677 3eac bb61 ab76 3eac bd6c a37e  .b.w>..a.v>..l.~
000001d0: 3eac bb69 ab7b 3eac b360 a57f 3eac bb6f  >..i.{>..`..>..o
000001e0: ad79 3eac b167 ad78 3eac bf63 a67a 3eac  .y>..g.x>..c.z>.
000001f0: 19ab 09ab 79ab 69ab 59ab 49ab b9ab a9ab  ....y.i.Y.I.....
00000200: 99ab 89ab f9ab e9ab d9ab c9ab 39aa 29aa  ............9.).
00000210: f9aa e9aa fb8e e88e 9eae 398f cead e886  ..........9.....
00000220: 3987 fb86 ca38 b7a9 ceb2 d9be 9a38 7267  9....8.......8rg
00000230: 6976 689a 7b9a 28b3 2bb3 7e15 3e15 3635  ivh.{.(.+.~.>.65
00000240: 6331 d9bc ceb0 d7a9 ceb2 d9be 3815 3635  c1..........8.65
00000250: c931 be35 af31 6238 9835 8925 c3d9 9923  .1.5.1b8.5.%...#
00000260: 8731 f138 8438 38ad b03a 5d38 75d9 f237  .1.8.88..:]8u..7
00000270: e725 c038 d836 c926 cab2 ddb2 2938 1c35  .%.8.6.&....)8.5
00000280: 0d25 9738 7169 6730 6aba 7dba fc38 8438  .%.8qig0j.}..8.8
00000290: 38ad b03a 0a38 62d9 5337 4725 dca5 c638  8..:.8b.S7G%...8
000002a0: dda5 c634 cca5 c634 271d 9038 e1c7 34f9  ...4...4'..8..4.
000002b0: 7966 6976 63ac 71ac d222 c332 00af 8938  yfivc.q..".2...8
000002c0: 5820 4930 5e66 4976 4e9e 599a 1db0 0ab0  X I0^fIvN.Y.....
000002d0: 1a34 0b24 f538 41c5 37af a3ac b1ac b436  .4.$.8A.7......6
000002e0: a526 9a38 7166 6976 6cba 7fba 7236 6326  .&.8qfivl...r6c&
000002f0: 7236 6326 6eb6 79b2 bdb8 aab8 7998 6e9c  r6c&n.y.....y.n.
00000300: b236 a326 9a38 59b0 4eb4 7022 6132 68ba  .6.&.8Y.N.p"a2h.
00000310: 7bba b437 a527 2238 41d9 1137 0725 7c38  {..7.'"8A..7.%|8
00000320: be35 af25 f938 c1c4 37af a3ac b1ac be34  .5.%.8..7......4
00000330: af24 aa38 1069 0730 08be 1bbe f538 be36  .$.8.i.0.....8.6
00000340: af26 be36 af26 7fb8 6cb8 b236 a326 aa38  .&.6.&..l..6.&.8
00000350: 1d66 0976 0cb2 1fb2 8138 5036 4126 9d38  .f.v.....8P6A&.8
00000360: 7834 6924 6cb6 7fb6 f338 81c5 37af a3ac  x4i$l....8..7...
00000370: b1ac 1fb4 0cb4 b436 a526 9a38 7269 6730  .......6.&.8rig0
00000380: 6ebe 79ba ac38 1436 0526 7fb0 6cb0 1236  n.y..8.6.&..l..6
00000390: 0326 f938 5bd6 49d6 38ad b03a 9f38 7036  .&.8[.I.8..:.8p6
000003a0: 6126 6e9a 79b6 1fb8 0cb8 1436 0526 0cbe  a&n.y......6.&..
000003b0: 1fbe 5db8 4ab8 41c6 34f9 5b66 4976 9d38  ..].J.A.4.[fIv.8
000003c0: 63ac 71ac 63ac 71ac 6ab6 7db6 f738 1fbc  c.q.c.q.j.}..8..
000003d0: 0cbc b422 a532 ac38 1e36 0f26 7bbc 68bc  ...".2.8.6.&{.h.
000003e0: 7236 6326 6a9a 7d9a 5bbc 48bc 7036 6126  r6c&j.}.[.H.p6a&
000003f0: 68b6 7bb6 b9b4 ae98 7e36 6f26 b998 ae9c  h.{.....~6o&....
00000400: a1c4 37af a3ac b1ac 8c38 5e22 4f32 4abe  ..7......8^"O2J.
00000410: 5dbe bf38 01c6 34f9 3b66 2976 23ac 31ac  ]..8..4.;f)v#.1.
00000420: 23ac 31ac 79b8 6ebc 3236 2326 3e20 2f30  #.1.y.n.26#&> /0
00000430: 3636 2726 bdbd aabd b637 a727 f738 5bd6  66'&.....7.'.8[.
00000440: 49d6 38ad b03a b037 a127 bbbc a8bc be36  I.8..:.7.'.....6
00000450: af26 be36 af26 be20 af30 9a38 7c66 6976  .&.6.&. .0.8|fiv
00000460: 6c9a 7f9a b237 a327 b623 a733 bdbc aabc  l....7.'.#.3....
00000470: 55d9 46d9 38ad b03a 9238 7036 6126 6abe  U.F.8..:.8p6a&j.
00000480: 7dbe 7738 be35 af25 be35 af25 b423 a533  }.w8.5.%.5.%.#.3
00000490: 19b4 0e98 01c6 34f9 1966 0976 03ac 11ac  ......4..f.v....
000004a0: b437 a527 b9b8 aebc be36 af26 be36 af26  .7.'.....6.&.6.&
000004b0: 19b8 0ebc 1e22 0f32 b437 a527 1fbc 0cbc  .....".2.7.'....
000004c0: 7bb8 68b8 1236 0326 b998 ae9c a1c4 35af  {.h..6.&......5.
000004d0: a3ac b1ac a3ac b1ac 1e22 0f32 1836 0926  .........".2.6.&
000004e0: bfb0 acb0 55d9 46d9 38ad b03a 7d98 6a98  ....U.F.8..:}.j.
000004f0: 5222 4332 5434 4524 bbb8 a8b8 be36 af26  R"C2T4E$.....6.&
00000500: be36 af26 9d38 7e36 6f26 6cbe 7fbe 7998  .6.&.8~6o&l...y.
00000510: 6e9c 7236 6326 bfb8 acb8 b222 a332 b836  n.r6c&.....".2.6
00000520: a926 9538 41c7 34f9 7b66 6976 63ac 71ac  .&.8A.4.{fivc.q.
00000530: 63ac 71ac 8a38 5236 4326 4cba 5fba 5035  c.q..8R6C&L._.P5
00000540: 4125 d034 c124 7db8 6ab8 d222 c332 f038  A%.4.$}.j..".2.8
00000550: 55d9 46d9 38ad b03a d036 c126 f338 be36  U.F.8..:.6.&.8.6
00000560: af26 8a38 5c34 4d24 5820 4930 4aba 5dba  .&.8\4M$X I0J.].
00000570: 9438 61c7 34f9 7b66 6976 63ac 71ac 63ac  .8a.4.{fivc.q.c.
00000580: 71ac 5db8 4ab8 5236 4326 7f98 6c98 5222  q.].J.R6C&..l.R"
00000590: 4332 4aba 5dba 8038 5e22 4f32 d037 c127  C2J.]..8^"O2.7.'
000005a0: f438 55d9 46d9 38ad b03a d037 c127 7fbc  .8U.F.8..:.7.'..
000005b0: 6cbc 5fb8 4cb8 70a6 5638 71a6 e635 60a6  l._.L.p.V8q..5`.
000005c0: e635 271d 5db4 4ab4 7db0 6ab0 5222 4332  .5'.].J.}.j.R"C2
000005d0: 5c34 4d24 7fb4 6cb4 5236 4326 f938 38ad  \4M$..l.R6C&.88.
000005e0: b03a 6d38 f738 01c5 37af a3ac b1ac 7bb4  .:m8.8..7.....{.
000005f0: 68b4 7e22 6f32 fc38 7bb8 68b8 b236 a326  h.~"o2.8{.h..6.&
00000600: 79b0 6eb4 b236 a326 5dbc 4abc 5ea4 9638  y.n..6.&].J.^..8
00000610: 5fa4 6634 4ea4 6634 271d 7422 6532 7a34  _.f4N.f4'.t"e2z4
00000620: 6b24 b236 a326 bc20 ad30 b8a4 9638 b9a4  k$.6.&. .0...8..
00000630: 6634 a8a4 6634 271d 3db8 2ab8 3222 2332  f4..f4'.=.*.2"#2
00000640: f238 8f38 38ad b03a 3036 2126 3a20 2b30  .8.88..:06!&: +0
00000650: 38a6 f638 39a6 a634 28a6 a634 271d de37  8..89..4(..4'..7
00000660: cf27 dfbc ccbc d823 c933 1dbc 0abc 7fb8  .'.....#.3......
00000670: 6cb8 12a6 f638 13a6 a634 02a6 a634 271d  l....8...4...4'.
00000680: de37 cf27 dc21 cd31 bdb8 aab8 5bb8 48b8  .7.'.!.1....[.H.
00000690: 38ad b03a de37 cf27 dbbc c8bc 18a7 f638  8..:.7.'.......8
000006a0: 19a7 a634 08a7 a634 271d de37 cf27 bfb0  ...4...4'..7.'..
000006b0: acb0 59b8 4ebc 38ad b03a f138 b022 a132  ..Y.N.8..:.8.".2
000006c0: be17 d9bc ceb0 07ae b6ba 5bb0 48b0 38ad  ..........[.H.8.
000006d0: 6539 1bb0 08b0 1e36 0f26 08b2 1bb2 7b98  e9.....6.&....{.
000006e0: 6898 59bc 4eb0 702e 613e 3fc9 90f4 b7d9  h.Y.N.p.a>?.....
000006f0: a6d9 1d08 073c 27c9 a6d9 b6d9 9eaf 398f  .....<'.......9.
00000700: cead e886 3987 fb86 e9a8 f9a8 29a8 39a8  ....9.......).9.
00000710: c9a9 d9a9 e9a9 f9a9 89a9 99a9 a9a9 b9a9  ................
00000720: 49a9 59a9 69a9 79a9 09a9 19a9 3eac cd38  I.Y.i.y.....>..8
00000730: 34ae 17cc b4b8 a5b8 ca38 37a9 3619 dfce  4........87.6...
00000740: a938 1b68 0730 1e2e 0f3e 4fc9 16a8 6a38  .8.h.0...>O...j8
00000750: 06a8 6b38 73db 66d9 57d9 46d9 b2d8 a7d9  ..k8s.f.W.F.....
00000760: 38ad 823a a6d9 b6d9 3eac 38ad 9839 bf12  8..:....>.8..9..
00000770: a7c9 bcda a7d9 38ad d43a c2f6 16a8 6a38  ......8..:....j8
00000780: 06a8 6b38 75d8 66d9 57d9 46d9 b6d9 a7d9  ..k8u.f.W.F.....
00000790: 38ad 823a d1f6 b9dd a7d9 38ad d43a d4f6  8..:......8..:..
000007a0: a1c2 3117 20cd 36ad 31e9 41c4 3fe9 38ad  ..1. .6.1.A.?.8.
000007b0: 963a 31c5 33e9 08cd a6ac b7ac a976 3eac  .:1.3........v>.
000007c0: 46ac 57ac 4976 3eac d836 c926 33a9 c2a8  F.W.Iv>..6.&3...
000007d0: d614 3fad 9c22 8d22 67d8 31f9 9c26 8d26  ..?.."."g.1..&.&
000007e0: 902e 813e 26c9 9022 8132 be26 af26 6cac  ...>&..".2.&.&l.
000007f0: 9fce b6ac a6ac 8a38 fb38 3eac 86d9 96d9  .......8.8>.....
00000800: dcd2 c5d9 3aad 223d 7a38 4d38 5c38 bf38  ....:."=z8M8\8.8
00000810: ef38 25af baa8 e6d9 f6d9 b7c6 21f9 fa2c  .8%.........!..,
00000820: eb3c 97c9 6238 9835 8925 3df9 ee38 2eaf  .<..b8.5.%=..8..
00000830: dba8 caa8 8e38 e238 bba8 7b38 3fac bf12  .....8.8..{8?...
00000840: 1fcd bc2d ad3d a7ce 17af dff6 f838 fb8e  ...-.=.......8..
00000850: e88e dad9 3aad 063d 39aa 29aa f9aa e9aa  ....:..=9.).....
00000860: d6a8 6c38 c6a8 6d38 15b8 26d9 36d9 17c4  ..l8..m8..&.6...
00000870: 38f9 39d6 29d6 fe38 e9a8 f9a8 29a8 39a8  8.9.)..8....).9.
00000880: 3eac 3fac bf12 27c9 39d6 29d6 f838 da38  >.?...'.9.)..8.8
00000890: bfa8 56a8 6c38 46a8 6d38 ed38 2eaf dba8  ..V.l8F.m8.8....
000008a0: caa8 b728 d8f6 bcd9 3fac bf12 17ca d7f6  ...(....?.......
000008b0: 19ab 09ab 79ab 69ab 59ab 49ab b9ab a9ab  ....y.i.Y.I.....
000008c0: 99ab 89ab f9ab e9ab d9ab c9ab 39aa 29aa  ............9.).
000008d0: f9aa e9aa fb8e e88e fc22 ed32 398f cead  .........".29...
000008e0: e886 3987 fb86 3fad 1cb1 0fb1 7eb1 69bd  ..9...?.....~.i.
000008f0: 58bd 4bbd babd adbd 9cbd 8fbd febd e9b9  X.K.............
00000900: d8b9 cbb9 3ab8 2db8 9cb8 8fb8 f836 e724  ....:.-......6.$
00000910: 398f cead e886 3987 fb86 db38 3eac cead  9.....9....8>...
00000920: c9f6 bb39 bc39 b139 b239 b739 4839 4d39  ...9.9.9.9.9H9M9
00000930: 4e39 4339 4439 5939 5a39 5f39 5039 5639  N9C9D9Y9Z9_9P9V9
00000940: 5539 9d39 9e39 9339 9439 a939 aa39 af39  U9.9.9.9.9.9.9.9
00000950: a039 5639 a539 a639 634a 575e 5319 1816  .9V9.9.9cJW^S...
00000960: 5551 5755 5a19 5055 575e 3c39 4f56 434b  UQWUZ.PUW^<9OVCK
00000970: 165f 5a58 5119 5b4c 454d 165b 5319 0401  ._ZXQ.[LEM.[S...
00000980: 165a 5e58 4458 554d 534b 4519 5a56 585e  .Z^XDXUMSKE.ZVX^
00000990: 3c39 7156 164a 435b 5b50 4219 4f56 434b  <9qV.JC[[PB.OVCK
000009a0: 165f 5a58 5118 3677 5949 5319 0c11 3639  ._ZXQ.6wYIS...69
000009b0: 717a 7503 1611 7e56 5b5c 544b 534e 1678  qzu...~V[\TKSN.x
000009c0: 606b 167e 757a 1600 180d 1809 1f19 0f17  `k.~uz..........
000009d0: 0217 0639 3239 3639 1b39 3639 3739 3639  ...92969.9697969
000009e0: 776f 6439 3639 3639 36b9 3639 3638 3639  wod969696.696869
000009f0: 3631 3639 3639 3639 363d 3639 3e39 3639  616969696=69>969
00000a00: 3739 3639 3658 4254 535e 570a 0401 4639  79696XBTS^W...F9
00000a10: 3639 3639 3617 4551 454d 444d 575b 3617  69696.EQEMDMW[6.
00000a20: 5258 4258 3617 425c 4e4d 3617 544a 4539  RXBX6.B\NM6.TJE9
00000a30: 185a 5954 5b5c 584d 3617 5856 425c 185e  .ZYT[\XM6.XVB\.^
00000a40: 584c 1858 404b 185d 534f 5f5a 5350 585f  XL.X@K.]SO_ZSPX_
00000a50: 5939 3639 3639 3639 3639 3639 3639 3639  Y969696969696969
00000a60: 3639 3639 3639 3639 3639 3639 3639 3639  6969696969696969
00000a70: 3639 3639 3639 3639 3639 3639 3d39 3639  696969696969=969
00000a80: 3739 3639 3539 3639 3638 b639 6e30 3639  7969596968.9n069
00000a90: 6e39 3639 3639 3639 3639 3639 3739 3639  n969696969697969
00000aa0: 3639 3639 2739 3639 3739 3639 3039 3639  6969'96979690969
00000ab0: 3639 3639 a239 3639 f231 3639 3639 3639  6969.969.1696969
00000ac0: 3639 3639 3439 3639 3639 3639 2139 3639  696949696969!969
00000ad0: 3e39 3639 3539 3639 6e38 b639 8630 3639  >9695969n8.9.069
00000ae0: 3039 3639 3639 3639 3639 3639 3739 3639  0969696969697969
00000af0: 3639 3639 2a39 3639 3739 3639 0639 3639  6969*9697969.969
00000b00: 3639 3639 8630 3639 1239 3639 3639 3639  6969.069.9696969
00000b10: 3639 3639 3739 3639 3739 3639 1339 3639  696979697969.969
00000b20: 3139 3639 3639 3639 3639 3639 e230 3639  196969696969.069
00000b30: 7639 3639 3639 3639 3639 3639 3239 3639  v969696969692969
00000b40: 3639 3639 3739 3639 3539 3639 3639 3639  6969796959696969
00000b50: 3639 3639 2233 3639 0839 3639 3639 3639  6969"369.9696969
00000b60: 3639 3639 3739 3639 3639 3639 0000 0000  696979696969....
00000b70: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000b80: 0000 0000 0000 0000 0000 0000 0000 0000  ................
...
00001fe0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00001ff0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
```
> I omitted the many trailing 0s by cutting a part of the file that was composed only of them.

From this file, two things can be observed: the enormous quantity of zeros and the recurring number 69.
* The 0 numbers can be assumed to be empty bytes in the EEPROM (so they can be removed);
* Since 'dump' has no meaning, it can be assumed to be something encoded in some way.

So the best approach would be to take the first 4 bytes to see if there's a magic number. However, doing some research on Google, the number `497c7a7f` doesn't exist. So, it's likely encrypted in some way.

Since the number 69 is present everywhere and quite persistently, it suggests that it may be part of the encryption. Considering that many 0s can be present in a file, this provides some clues about the type of encryption that may have been used.

In fact, XORing any byte with 0 returns the same byte. With that said, we need to try and see what comes out.

```python
k = '69'.encode('ascii')
magic_num = bytearray()
for i, byte in enumerate([0x49, 0x7c, 0x7a, 0x7f]):
    tmp = byte ^ k[i % 2]
    magic_num.append(tmp)

print(magic_num) # -> bytearray(b'\x7fELF')
```

From here, it can be seen that the content of the EEPROM is a program (ELF) XORed with the key '69'.

## Part 3: rev

For this part of writeup i used "avr-objdump" and "IDA" along with "simavr" and "avr-gdb" to run and debug the binary.


Keep in mind that in atmega328p registers can only contain one byte.


[AVR Instruction Set Manual](https://ww1.microchip.com/downloads/en/devicedoc/atmel-0856-avr-instruction-set-manual.pdf)

To run and debug the binary we use
```shell
simavr -d -g -m atmega328p main.elf
```
and then we can run avr-gdb and attach to the process
```shell
avr-gdb main.elf
target remote :1234
```
The first problem we face after disassembling the binary is to find the main function,
to find it we can just look for this instruction, (this is what happens before the "setup" function)
```assembly
sbi     DDRD, DDD2    (sbi	0x0a, 2)
cbi     PORTD, PORTD2 (cbi	0x0b, 2)
```

Analysing the function we can notice that it loads something from Z+ to r0
```assembly
ld      r0, Z+
tst     r0
brne	.-6 
```
This is our input, in fact if we analyse it with avr-gdb we will notice it loading all the values from register r0 to r27, every register is one byte long,
it then checks how many bytes we loaded (the program adds 0x1 to the number of bytes)
```assembly
sbiw	r30, 0x1d (29)
breq	.+2      	
rjmp	.-2
```

It will pass the check only if we loaded 28 bytes, from this we can assume that our flag is 28 characters long, otherwise it'll end in an infinite loop.

The next task will be to analyse the function that is being called by "main", we need it to return true in order to exec "sbi     PORTD, PORTD2" instruction
```assembly
ldi     r24, 0
ldi     r25, 0
call    sub_ED
or      r24, r25
breq	.+2 
sbi     PORTD, PORTD2 (0x0b, 2)
```

After disassembling the function we will see that it consists in a really big loop that repet itself 27 times, but before analysing it, we can jump to the end of the function, there we can notice that it will return true only if r2 == 27
```assembly
loc_646:
ldi     r24, 1
ldi     r25, 0
ldi     r16, 27
cp      r2, r16
cpc     r3, r1
breq    loc_64E

ldi     r24, 0
ldi     r25, 0

loc_64E:
subi    YL, -0x68
sbci    YH, -1
in      r0, SREG
cli
out     SPH, YH
out     SREG, r0
out     SPL, YL
pop     YH
pop     YL
pop     r17
pop     r16
pop     r15
pop     r14
pop     r13
pop     r12
pop     r11
pop     r10
pop     r9
pop     r8
pop     r7
pop     r6
pop     r5
pop     r4
pop     r3
pop     r2
ret
```
In order to make this happen we need to understand what is happening on the inside of the loop
but it would require to much time for us to do that, if we go back to the loop we can see that r2 changes just one time trought the whole loop
```assembly
call    sub_5B
add     r2, r24
adc     r3, r25
```
Apparently the value of r24 depends from the result of call sub_5B.

After entering inside sub_5B we will see that the only thing it does is jumping in a table where it only does subtractions
```assembly
subi	r24, 0xC7	; 199
sbci	r25, 0x27	; 39
ret
subi	r24, 0xC7	; 199
sbci	r25, 0x4A	; 74
ret
subi	r24, 0xB3	; 179
sbci	r25, 0xE0	; 224
ret
subi	r24, 0x8D	; 141
sbci	r25, 0xFD	; 253
ret
subi	r24, 0x5B	; 91
sbci	r25, 0x75	; 117
ret
subi	r24, 0x0D	; 13
sbci	r25, 0x2D	; 45
ret
subi	r24, 0x95	; 149
sbci	r25, 0x63	; 99
ret
subi	r24, 0x6D	; 109
sbci	r25, 0x0B	; 11
ret
subi	r24, 0xE7	; 231
sbci	r25, 0x1B	; 27
ret
subi	r24, 0xA9	; 169
sbci	r25, 0x30	; 48
ret
subi	r24, 0x07	; 7
sbci	r25, 0xFA	; 250
ret
subi	r24, 0x21	; 33
sbci	r25, 0x81	; 129
ret
subi	r24, 0xB3	; 179
sbci	r25, 0x40	; 64
ret
subi	r24, 0xF5	; 245
sbci	r25, 0x98	; 152
ret
subi	r24, 0xD5	; 213
sbci	r25, 0xFC	; 252
ret
subi	r24, 0x29	; 41
sbci	r25, 0xF4	; 244
ret
subi	r24, 0xDD	; 221
sbci	r25, 0xED	; 237
ret
subi	r24, 0x27	; 39
sbci	r25, 0x66	; 102
ret
subi	r24, 0x0F	; 15
sbci	r25, 0xE4	; 228
ret
subi	r24, 0x5D	; 93
sbci	r25, 0x41	; 65
ret
subi	r24, 0x1B	; 27
sbci	r25, 0x33	; 51
ret
subi	r24, 0x0D	; 13
sbci	r25, 0x22	; 34
ret
subi	r24, 0xE5	; 229
sbci	r25, 0xE2	; 226
ret
subi	r24, 0x23	; 35
sbci	r25, 0xAC	; 172
ret
subi	r24, 0xBF	; 191
sbci	r25, 0xE3	; 227
ret
subi	r24, 0xF3	; 243
sbci	r25, 0xED	; 237
ret
```

Going back to our loop we see that the values inside r24, r25, r26 and r27 are calculated based on our input, in particular from the value "i" and "i+1".
Knowing that: r24 will be added to r0, r0 has to be 27 and that the loop repets 27 times, we can assume that, in order to find the flag, r24 has to be 1, while 25 has to be 0.
From this info we can write a script to bruteforce our input in order to make r24, r25 the right values in the moment of the subtruction.

```python
import gdb
import string


def fill(flag):
    for j in range(len(flag)):
        gdb.execute("set $r" + str(j) + " = "  + flag[j], True, True)
    
    for i in range(len(flag), 28):
        gdb.execute("set $r" + str(i) + " = "  + "0x61", True, True)


def firsts_two(char):
    firsts = ""
    for i in char:
        for j in char:
            gdb.execute("set $r0 = " + i)
            gdb.execute("set $r1 = " + j) 
            gdb.execute("c")
            

            #checking if r24 equals 1 and r25 equals 0
            #we need r24 to be 1 because it will be add to r2 
            res = check()

            if res == 2:
                print(i, j)
                firsts += i + j
                return firsts
                #checking if r24 equals 1 and r25 equals 0
            else:
                gdb.execute("monitor r")
                res = 0
                #res != 2 means that our input in not correct and we have to restart the binary
                fill("")
    

def full_flag(firsts, char):
    flag = ""
    flag += firsts
    for j in 25:
        for i in char:
            fill(flag)
            gdb.execute("c")
            res = check()
            if res == 2:
                flag += i
                break
            else:
                gdb.execute("monitor r")
                res = 0
                
    return flag
        
def check():
    for i in range(3):
        gdb.execute("ni")
        # stop before ret
    
    reg = gdb.execute("p/x $r24")
    if "0x1" in reg:
            res += 1     
    
    reg = gdb.execute("p/x $r25")
    if "0x0" in reg:
	res += 1
    return res 


def main():
    
    firsts = ""
    flag = ""
    char = string.ascii_lowercase + string.digits + "_"

    gdb.execute("br *0xcd8") # break before load instruction
    gdb.execute("br *0xd5c") # break before ijmp   
    
    fill()
    #filling our buffer with "a"
    
    firsts = ""
    firsts = firsts_two(char)
    #bruteforcing the firsts two characters of our buffer
    
    flag = full_flag(firsts, char)
    #we can keep bruteforcing one byte at a time to find the full flag
    print(flag)
                
               
if __name__ == "__main__":
    main()

```