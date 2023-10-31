# SN74/54x6969
**32KB RAM with EEPROM CONSTANTS**

## Description
When it comes to choosing the right microcontroller for your project, there are numerous options available on the market. One of the most popular choices is the 6969 
chip, which comes with a wealth of features that can make your project run more smoothly.

One of the standout features of the 6969 chip is its internal RAM capacity of 32K, which provides ample memory for storing and retrieving data quickly and 
efficiently. Additionally, this chip offers the option to connect an external EEPROM, allowing you to store even more data and easily access it when needed.

However, one of the most impressive aspects of the 6969 chip is its internal storage of constants, which can greatly streamline your code and ensure that critical 
variables are always accessible without needing to be updated or modified. This feature allows for more efficient use of your time and resources, as you won't have to
spend time searching for or updating these variables throughout the project lifecycle.

It is worth noting that the 6969 chip does not allow for direct modification of external EEPROM data, but the internal storage of constants provides an invaluable 
resource that can significantly enhance your project's performance and productivity. Overall, the 6969 chip is a versatile piece of hardware that is well-worth 
considering when looking to optimize your project's efficiency and functionality.

## Technical specification
Guaranteed operating ranges
Symbol|Parameter|Type|Min|Normal|Max|Unit
---|---|:---:|:---:|:---:|:---:|:---:
VCC|Supply voltage|54|4.5|5.0|5.5|V
VCC|Supply voltage|74|4.75|5.0|5.25|V
TA|Operating ambient temperature range|54|-55|25|125|°C
TA|Operating ambient temperature range|74|0|25|70|°C
IOH|Output current - High|54, 74|||-0.4|mA
IOL|Output current - Low|54|||4.0|mA
IOL|Output current - Low|74|||8.0|mA

DC Characteristics over temperating temperature range (unless otherwise specified)
Symbol|Parameter|Type|Lim Min|Normal|Lim Max|Unit|Test conditions
---|---|:---:|:---:|:---:|:---:|:---:|---
VIH|Input HIGH voltage||2.0|||V|Guaranteed input HIGH voltage for all inputs
VIL|Input LOW voltage|54|||0.7|V|Guaranteed input LOW voltage for alla inputs
VIL|Input LOW voltage|74|||0.8|V|Guaranteed input LOW voltage for alla inputs
VIK|Input clamp diode voltage|||-0.65|-1.5|V|VCC=MIN, IIN=-18mA
VOH|Output HIGH voltage|54|2.5|3.5||V|VCC = MIN, IOH = MAX, VIN = VIH or VIL per Truth Table
VOH|Output HIGH voltage|74|2.7|3.5||V|VCC = MIN, IOH = MAX, VIN = VIH or VIL per Truth Table
VOL|Output LOW voltage|54, 74||0.25|0.4|V|IOL = 4.0 mA
VOL|Output LOW voltage|74||0.35|0.5|V|IOL = 8.0 mA
IIH|Input HIGH current||||20|μA|VCC = MAX, VIN = 2.7 V
IIL|Input LOW current||||-0.4|mA|VCC = MAX, VIN = 0.4 V
IOS|Short circuit current||-20||-100|mA|VCC=MAX
ICC|Power supply current (output HIGH)||||6.2|mA|VCC=MAX
ICC|Power supply current (output LOW)||||9.8|mA|VCC=MAX

## Pinout
Pin name|Function|Note
---|---|---
clk|The clock signal used to synchronize the operation of the device. This signal is used to control the timing and execution of operations within the device|
data_in(8)|The input data signal for an 8-bit data transfer, which is used to read data from an external EEPROM.
addr(32)|The address signal for a 32-bit address space, which is used as an output signal to indicate the location in memory of an external EEPROM that the device is accessing.
rw|The read/write signal, which is used to indicate whether the device is reading from or writing to the external EEPROM. This signal is used to determine the  direction of data transfer and the operation that the device performs on the EEPROM. When the value of this signal is LOW, it indicates that the device is reading data from the EEPROM, and when the value is HIGH, it indicates that the device is writing data to the EEPROM.
op(32)|The operation signal for a 32-bit operation space, which specifies the specific operation that the device is performing on data. The first 4 bits of this  signal represent the opcode, which determines the type of operation to be performed. The next 8 bits represent the address of the register. The remaining 20 bits represent the value of the register.
data_out(8)|The output data signal for an 8-bit data transfer. This  signal carries the data that has been processed by the device and is avaiable to read.
status|A status signal that indicates the current state of the device and any errors or exceptions that have occurred during operation. The value of this signal can be either LOW, which indicates that the operation was successful and there were no errors, or HIGH, which indicates that an error has occurred during operation.
avb|The availability bit, which indicates when the data is available on the signal for use by other processes or devices. This signal can be used to synchronize data  transfers between different components of a system and ensure that data is transferred in a timely and efficient manner.

## OPCODES
Command|OPCODE format|Info|Stable
---|---|---|:---:
Reserved|0000|Reserved for future use|Yes
Get constant values|0001|This command sends the names of constants stored in the internal memory section dedicated to constants (96B) one byte at a time|Yes
Empty cells|0010|This command erases the contents of cells located at addresses specified in bytes 25 to 18|Yes
Flush of cache|0011|This command clear the cache memory|Partially
Enable status pin|0100|This command enables the behavior of the status pin|Partially
Disable status pin|0101|This command disables the behavior of the status pin|Partially
Integrity check|0110|This command check if the RAM integrity is OK|Partially
Set value in ram|0111|This command set the given value into the given RAM address|No
Get value in ram|1000|This command return the value located in the given address|No
Copy value|1001|This command copy value from one address to another|No
Is empty?|1010|This command checks if the given address ha value of none|No
Enable data watcher|1011|This command enables the data watcher technology|Partially
Read from external EEPROM|1100|This command reads byte from the external EEPROM. To do this is necessary to define the byte target address into the bits from 18 to 0|Yes
Disable data watcher|1101|This command disables the data watcher|Partially
Get value of data watcher|1110|This command returns the value from data watcher|No
Reserved|1111|Reserved for future use|Yes

## Disclaimer & legal notice
It is important to note that the design of the 6969 chip is still in an experimental phase and may be subject to changes. This document is strictly confidential and 
is only intended for internal use by HWLabs&Co. The information contained within this document is the property of both HWLabs&Co. and the SRDNLen prototype, and any 
unauthorized dissemination or sharing of this information is strictly prohibited.
