# Writeup
To solve this challenge, a VHDL file describing the behavior of an MCU within a board created to act as an ABS, a datasheet describing the behavior of a humidity sensor connected to the board was attached to provide real-time information about air humidity conditions (and thus asphalt conditions).

## Solution

To solve this challenge, it's necessary to have the datasheet and the VHDL at hand as they will need to be compared.

In fact, by scrolling through the 'architecture' section of the `SuperABS` entity, we will find several processes. One of these, `process(clk)` contains instructions to initialize the sensor. In particular, when `sensor_current_status=INITIALIZING` the MCU sets registers with values.

Okay, now we need to see what it does:
* Lines 81-92: Set the power-saving mode to off (ALWAYS ACTIVE).
* Lines 93-104: Set the sampling mode to 16-bit.

But upon closer inspection, there is a problem: in line 98, the bits for the MODE register are only 7 instead of the usual 8 as described in the datasheet.

When VHDL has fewer bits than expected, it adds the remaining bits to the left in the form of zeros. So, the pointed register will be '01001100' (ORDER) and not MODE (10001100).

This means that by setting 0x20 in the ORDER register, we are keeping it with its default value, which is big-endian. Meanwhile, the MODE will produce a value ranging from 0 to 255 (as it is set to 8 bits).

Moving on, from line 139, the MCU takes the 16 bits sent by the sensor, but it only takes the first 8, which in this case are 8 zeros.

The flag asks to describe what happens when data is requested from the sensor with 100% humidity in the air and to identify the line where the bug occurs. Knowing that the sensor has a maximum range of 90% RH, this means that values higher than 90 will still be classified as the maximum (90%); thus, making a value of `0000000011111111`.

This leads to the fact that if instead of setting the byte 0x20 to ORDER, it had been set to mode, the chip would work normally. Therefore, the line where the bug is present is line 98.

### Flag
`srdnlen{0000000011111111_98}`

## Notes
I have been informed that there are several errors in the VHDL challenge that could have/may have misled several players. I want to apologize to anyone who couldn't solve it because of these errors and thank [Hetti](https://github.com/Hetti) for pointing them out and for the friendly conversation.
