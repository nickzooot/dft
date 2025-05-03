// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title PoetryNFT
 * @dev A contract for publishing poetry as NFTs on the Ethereum blockchain
 */
contract PoetryNFT is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    // Mapping from token ID to poetry text
    mapping(uint256 => string) private _poetryTexts;
    
    // Event emitted when a new poem is published
    event PoemPublished(uint256 tokenId, address author, string poemTitle);
    
    constructor() ERC721("PoetryNFT", "POEM") {}
    
    /**
     * @dev Publishes a poem as an NFT and returns it to the author
     * @param author Address of the poem's author
     * @param poemTitle Title of the poem
     * @param poemText Full text of the poem
     * @param metadataURI URI to the poem's metadata (JSON)
     * @return The ID of the newly minted NFT
     */
    function publishPoem(
        address author,
        string memory poemTitle,
        string memory poemText,
        string memory metadataURI
    ) public returns (uint256) {
        require(bytes(poemText).length > 0, "Poem text cannot be empty");
        
        _tokenIds.increment();
        uint256 newItemId = _tokenIds.current();
        
        // Mint the NFT
        _safeMint(author, newItemId);
        
        // Set the metadata URI
        _setTokenURI(newItemId, metadataURI);
        
        // Store the poem text
        _poetryTexts[newItemId] = poemText;
        
        // Emit event
        emit PoemPublished(newItemId, author, poemTitle);
        
        return newItemId;
    }
    
    /**
     * @dev Returns the poem text for a given token ID
     * @param tokenId The ID of the token
     * @return The poem text
     */
    function getPoemText(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "PoetryNFT: Poem does not exist");
        return _poetryTexts[tokenId];
    }
    
    /**
     * @dev Self-publish a poem (author is the message sender)
     * @param poemTitle Title of the poem
     * @param poemText Full text of the poem
     * @param metadataURI URI to the poem's metadata (JSON)
     * @return The ID of the newly minted NFT
     */
    function selfPublishPoem(
        string memory poemTitle,
        string memory poemText,
        string memory metadataURI
    ) public returns (uint256) {
        return publishPoem(msg.sender, poemTitle, poemText, metadataURI);
    }
} 