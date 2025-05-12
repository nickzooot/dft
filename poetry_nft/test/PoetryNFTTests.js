const { expect } = require("chai");
const { ethers } = require("hardhat");

// Sample poems for testing
const SAMPLE_POEMS = [
  {
    title: "Test Poem 1",
    text: "This is a test poem 1",
    uri: "ipfs://QmTestPoem1"
  },
  {
    title: "Test Poem 2",
    text: "This is a test poem 2",
    uri: "ipfs://QmTestPoem2"
  }
];

describe("PoetryNFT", function() {
  let poetry;
  let deployer;
  let user;
  
  beforeEach(async function() {
    // Get signers
    [deployer, user] = await ethers.getSigners();
    
    // Deploy a fresh contract for each test
    const PoetryNFT = await ethers.getContractFactory("PoetryNFT");
    poetry = await PoetryNFT.deploy();
    await poetry.deployed();
    
    console.log(`Contract deployed to: ${poetry.address}`);
    console.log(`Contract owner: ${deployer.address}`);
  });
  
  describe("Basic Functionality", function() {
    it("Should have correct name and symbol", async function() {
      expect(await poetry.name()).to.equal("PoetryNFT");
      expect(await poetry.symbol()).to.equal("POEM");
    });
    
    it("Should allow publishing a poem", async function() {
      // Publish poem
      const tx = await poetry.selfPublishPoem(
        "Test Poem", 
        "This is a test poem", 
        "ipfs://test"
      );
      
      await tx.wait();
      
      // Verify poem storage
      const poemText = await poetry.getPoemText(1);
      expect(poemText).to.equal("This is a test poem");
    });
    
    it("Should reject empty poem text", async function() {
      await expect(
        poetry.selfPublishPoem("Empty", "", "ipfs://test")
      ).to.be.revertedWith("Poem text cannot be empty");
    });
  });
  
  describe("Error Handling", function() {
    it("Should fail when retrieving non-existent poem", async function() {
      await expect(
        poetry.getPoemText(999)
      ).to.be.revertedWith("PoetryNFT: Poem does not exist");
    });
  });
  
  describe("Sample Poems", function() {
    it("Should publish classic literature as NFTs", async function() {
      // Publish all sample poems
      for (let i = 0; i < SAMPLE_POEMS.length; i++) {
        const poem = SAMPLE_POEMS[i];
        
        console.log(`Publishing poem: ${poem.title}`);
        
        const tx = await poetry.selfPublishPoem(
          poem.title,
          poem.text,
          poem.uri
        );
        
        await tx.wait();
        
        // Token ID should be i+1 (since token IDs start at 1)
        const tokenId = i + 1;
        
        // Verify storage
        const storedText = await poetry.getPoemText(tokenId);
        expect(storedText).to.equal(poem.text);
        
        // Log the token details
        console.log(`Token ID ${tokenId} | Title: ${poem.title} | Owner: ${deployer.address}`);
      }
      
      // Verify token count
      await expect(poetry.ownerOf(SAMPLE_POEMS.length + 1))
        .to.be.revertedWith("ERC721: invalid token ID");
    });
  });
}); 