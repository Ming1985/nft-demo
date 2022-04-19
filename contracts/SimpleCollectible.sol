// SPDX=License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    constructor() public ERC721("Dogie", "DOG") {
        // count the mint number
        tokenCounter = 0;
    }

    // assigning a new token id to a new owner
    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        // set newTokenId equals to current token counter
        uint256 newTokenId = tokenCounter;

        // use _safeMint to avoid override same tokenId.
        // safeMint( owner address, tokenId)
        _safeMint(msg.sender, newTokenId);

        // set URI
        // URI is where the picture is stored

        _setTokenURI(newTokenId, tokenURI);

        // token counter +1 to avoid overlap mint
        tokenCounter = tokenCounter + 1;

        return newTokenId;
    }
}
