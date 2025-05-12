# Poetry NFT

A blockchain-based platform for publishing poetry as Non-Fungible Tokens (NFTs) on the Ethereum network. Each poem is stored completely on-chain and minted as an NFT that belongs to the author.

## Overview

This project demonstrates how to create, deploy, and interact with a smart contract for publishing poetry as NFTs. It leverages the ERC-721 token standard to create unique, non-fungible tokens representing individual poems. Key aspects include:

- Full on-chain storage of poetry text
- Automatic minting of NFTs to poem authors
- Verifiable ownership through the Ethereum blockchain
- Ability to retrieve poem text by token ID

## Prerequisites

- [Node.js](https://nodejs.org/) 
- An Ethereum wallet with a private key (e.g., [MetaMask](https://metamask.io/))
- [Alchemy](https://www.alchemy.com/) account for API access to Ethereum network
- Some test ETH on the Sepolia testnet (available from [Sepolia Faucet](https://sepoliafaucet.com/))

## Installation

Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd poetry_nft
npm install
```

## Configuration

1. Create a `.env` file in the project root with the following variables:

```
# Your Alchemy API URL for Sepolia testnet
API_URL=https://eth-sepolia.g.alchemy.com/v2/your-api-key

# Private key of your Ethereum wallet (without 0x prefix)
PRIVATE_KEY=your-private-key

# Address of the deployed PoetryNFT contract (fill after deployment)
POETRY_NFT_ADDRESS=
```

2. Obtain an API key from [Alchemy](https://www.alchemy.com/) for access to the Sepolia testnet
3. Ensure your wallet has test ETH (from [Sepolia Faucet](https://sepoliafaucet.com/))

## Deployment

Deploy the PoetryNFT contract to the Sepolia testnet:

```bash
npx hardhat run scripts/deploy-poetry.js --network sepolia
```

When deployment completes, you'll see the contract address in the console. Copy this address and add it to your `.env` file as `POETRY_NFT_ADDRESS`.

## Usage

### Publishing a Poem

Use the provided script to publish a poem as an NFT:

```bash
npx hardhat run scripts/publish-poem.js --network sepolia
```

The script will:
1. Connect to your deployed contract
2. Mint an NFT with the poem content
3. Assign ownership to your address (the transaction sender)
4. Print the token ID, transaction hash, and verification of the stored poem

### Customizing Poems

To publish your own poem, modify the `publish-poem.js` script:

1. Open `scripts/publish-poem.js`
2. Change the `poemTitle` and `poemText` variables with your content
3. For production use, update the `metadataURI` to point to proper metadata 

## Smart Contract Architecture


### Key Contract Components

#### State Variables
- `_tokenIds`: Counter for tracking token IDs
- `_poetryTexts`: Mapping from token IDs to poem text

#### Events
- `PoemPublished(uint256 tokenId, address author, string poemTitle)`: Emitted when a new poem is published

#### Functions

- `publishPoem(address author, string memory poemTitle, string memory poemText, string memory metadataURI)`: 
  - Publishes a poem and mints an NFT to the specified author
  - Parameters:
    - `author`: Ethereum address of the poem's author
    - `poemTitle`: Title of the poem
    - `poemText`: Full text content of the poem
    - `metadataURI`: URI pointing to the poem's metadata (JSON)
  - Returns: The ID of the newly minted NFT

- `selfPublishPoem(string memory poemTitle, string memory poemText, string memory metadataURI)`:
  - Convenience function for authors to publish their own poems
  - Parameters: Same as `publishPoem` except author (uses `msg.sender`)
  - Returns: The ID of the newly minted NFT

- `getPoemText(uint256 tokenId)`:
  - Retrieves the poem text for a given token ID
  - Parameters:
    - `tokenId`: The ID of the token
  - Returns: The poem text as a string



## Testing

The project includes comprehensive tests to verify the functionality of the PoetryNFT contract:

```bash

# Run PoetryNFT tests
npx hardhat test test/PoetryNFTTests.js
```

The PoetryNFTTests.js file contains tests that:

1. Verify basic contract functionality (name, symbol)
2. Test publishing poems and storing them on-chain
3. Check error handling for invalid inputs
4. Publish sample test poems and verify their storage
5. Log contract deployment addresses for reference



Sample output:
```
Contract deployed to: 0x18F857Fb529CA521f1Dab6477FC3E1d54feC813E
Contract owner: 0x724e3A05511dBe20e59Af9ef7561993Bff6DA209
Publishing poem: Test Poem 1
Token ID 1 | Title: Test Poem 1 | Owner: 0x724e3A05511dBe20e59Af9ef7561993Bff6DA209
```



