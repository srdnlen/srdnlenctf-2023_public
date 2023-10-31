Koenigsberg - Rev

The function checking the flag has 1000 labels. 
1000 flags have to be set in order to pass the check. This needs to happen in max 1000 steps. 
Each label sets its own flag only when another flag is set. Therefore, there is an order in which these labels have to be traversed.

One node jumps to the next by selecting a certain label from a jump table, depending on the current node and one character of the flag. 
Even knowing the desired destination, there may be multiple valid characters for the individual node. But the 1000 nodes work on the flag in modulo of its length and there's only one character that passes all checks on all the related nodes.

Here's a more technical description of the problem.

```
FLAG_LEN = 69, ctr = 0
int visited[1000] = {0}
ADDR jump_table[16000] = ... // BIG initialization. if you're curious about how this code was generated, check `src/jump_gen.py`
``` 


Each step increases `ctr` by 1. If this counter passes 1000, you lose. 

If the node at step `ctr` has been visited, you lose.

`visited[node num] = visited[some other node, specific to the current node]`. 

All this means is if we want to visit all 1000 nodes in exactly 1000 steps, we will have to visit them in an order where the new node at step N contains a node already visited on the right side of this assignment. We start with node 0.
If you imagine the nodes visited so far as the domain, and the nodes that can be visited as the function, you can expand the closure starting from {0} one step at a time to all nodes. 

the character at flag[ctr%FLAG_LEN] is xored with another value specific to the node, then this is applied as an offset to `jump_table[(node num*16 + off)%16000]`.

Given a potential flag, the character at position `i` is correct if the nodes at all steps where `ctr%69 == i` ALL address the correct destination. 
As mentioned before, individual nodes might have multiple offsets which connect to the same destination node. 
If this happens to be the expected destination (and it does happen in a few of the first 69 nodes), you will need to enumerate the possible destinations and filter them for the next pass on that character until you have only one option.

Certain decompilers get really confused by the partially overlapping jump table, the indirect jumps from within a regular function and the inline assembly required to do so.
But overall, each node has the same structure, and besides some strange modular math optimization, the code is very readable.
By analyzing the bytecode, we can, in order:

1) Extract the order in which the nodes need to be visited. This is because each label hardcodes the node number (but they're lined up in order), the "previous" node, and the unique xor byte. This information is sufficient to bruteforce character by character, if you wish.
2) Extract each node's jump table subset and filter for the intended destination. This might not be a single option!
You can skip this if you set up a GDB script to explore the options for you, or emulate the control flow in other ways.
3) Select the single character that allows ALL (input[ctr++] ^ xor byte unique to the node = offset) to select the correct destinations.

If you're planning to recompile the challenge, keep in mind the C code utilizes a few extensions unique to GCC. Compile with GCC!
The src/ folder also contains a python script which guides you through generating the necessary C code.