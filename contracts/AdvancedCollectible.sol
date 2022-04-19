// An NFT Contract
// Where the tokenURI can be one of 3 different dogs
// Randomly selected

// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter; // plus one for each nft minted
    bytes32 public keyhash; // for vrf random generator
    uint256 public fee; // for random generate fee
    enum Breed { PUG, SHIBA_INU, ST_BERNARD } // dog type, randomly given
    mapping(uint256 => Breed) public tokenIdToBreed; // stores mapping between tokenid and breed
    mapping(bytes32 => address) public requestIdToSender; // stores which address send the random request
    // emit an event when a mapping is changed.
    // the indexed keyword is to index the event for easier search
    event requestedCollectible(bytes32 indexed requestId, address requster);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public 
    VRFConsumerBase(_vrfCoordinator, _linkToken)
    ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32){
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override{
        Breed breed = Breed(randomNumber % 3); // get random breed
        uint256 newTokenId = tokenCounter; // get token Id
        tokenIdToBreed[newTokenId] = breed; // assign the mapping
        emit breedAssigned(newTokenId, breed);
        // get the original sender, because in this function, the msg.sender is vrf coordinator, not the nft minter
        address owner = requestIdToSender[requestId]; 
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }




    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // pug, shiba inu, st bernard
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner no approved");
        _setTokenURI(tokenId, _tokenURI);
    }
}