// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

contract Counter {
    uint256 public count;

    modifier greaterThanZero() {
        require(count > 0, "count should be strictly greater than 0");
        _;
    }

    constructor() {
        count = 0;
    }

    function inc() public {
        count += 1;
    }

    function dec() public greaterThanZero {
        count -= 1;
    }

    function reset() public {
        count = 0;
    }
}
