## What do you need to create an NFT
- **owner.address**, msg.sender
- **tokenId**, generated unique id for the nft 
- **uri**, a link to the picture or other resources out of the contract
- an attribute dictionary, or **mapping**, to store the attribute of the nft
## SimpleCollectible.sol
- createCollectible(tokenURI)
- _safeMint(msg.sender, newTokenId)
- _setTokenURI(newTokenId, tokenURI)
### deploy_and_create.py
- SimpleCollectible.deploy
- SimpleCollectible.createCollectible(uri, )
- brownie run scripts/deploy_and_create.py --network rinkeby
### Test
- assert simple_collectible.ownerOf(0) == get_account()
- ownerOf(tokenId) get owner of tokenId nft
## Advanced Collectible
- advancedCoolectible.sol
### IPFS
- how to upload to ipfs
- how decentralized
### how to generate random nft
- inherit VRFConsumerBase
- need 2 functions: requestRandomness get the number
- fullfillRandomness do some function after get the number
- that is, set a random type from predefined nft types
- and set the uri associated with the type
### Functions 
- tokenCounter how many token has been created
- Verify contract to use functions on etherscan
### Events
- topic0: hash of the signature of the event
- topic1,2... the parameters of the function
- get event from transaction by brownie
- format: tx.events[eventname][eventVariable]
### Testing
### URI
need to find a way to host metadata and images

### Using IPFS

A sample metadata
```
{
    "name": "PUG",
    "description": "An adorable PUG pup!",
    "image": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "attributes": [
        {
            "trait_type": "cuteness",
            "value": 100
        }
    ]
}
```

- upload file to ipfs, get uri, save onchain. 
- ipfs init
- ipfs daemon. start the daemon service
- post request to /api/v0/add to add a file to ipfs
- curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add   USE curl to post a file onto ipfs network
- 
  
## Resources
- ERC721 Standard: https://eips.ethereum.org/EIPS/eip-721   
- OpenZeppelin ERC721 contract source code: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol
- dungen and dragon nft example https://github.com/PatrickAlphaC/dungeons-and-dragons-nft
- VRFConsumerBase code: https://github.com/smartcontractkit/chainlink-brownie-contracts/blob/main/contracts/src/v0.6/VRFConsumerBase.sol
- IPFS docs https://docs.ipfs.io/reference/http/api/#getting-started 