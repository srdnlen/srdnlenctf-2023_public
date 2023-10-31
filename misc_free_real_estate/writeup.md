Free Real Estate - Misc, Blockchain

The core vulnerability in the given smart contract is a reentrancy bug caused by the `returnWallet` call.

First of all, in order to access the smart contract as a smart contract ourselves, we will need to register to the victim SC during our own constructor.
This allows us to bypass the `isNotContract` check, which tries to stop us by checking our `extcodesize(_a)`. This returns 0 if we are an account, but also if we are a smart contract in the process of completing the constructor.

Then, we can either implement `returnWallet`, or set up the `fallback()` function, in order to trigger a reentrancy into the `redeem()` function before our balance is updated.
Once we are above 100 points we have control of the contract. This is sufficient to write our text at any time.
The `Attacker` smart contract in `src/FreeRealEstate.sol` lets you set the desired number of iterations beforehand. With the default gas values on Remix, you can interate 12 or 13 times without issues.

The victim contract is not instantiated for each team individually: it could happen that multiple teams complete the challenge on the same block and the validator fails for all but one of them.
I recommend writing a function in your attacker contract to alter the ad space at any time once you've won, so you can just run the validator again.

The `FreeRealEstate.sol` file in the source code folder contains an example attacker smart contract, developed with the `fallback()` method described above.