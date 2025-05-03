require('dotenv').config();
const { ethers } = require("hardhat");

async function main() {
  // The address to which the contract was deployed
  const contractAddress = process.env.POETRY_NFT_ADDRESS;
  
  if (!contractAddress) {
    console.error("Please set POETRY_NFT_ADDRESS in your .env file");
    process.exit(1);
  }
  
  // Get the contract instance
  const PoetryNFT = await ethers.getContractFactory("PoetryNFT");
  const poetryNFT = await PoetryNFT.attach(contractAddress);
  
  // Example poem
  const poemTitle = "To Be, Or Not To Be";
  const poemText = `To be, or not to be: that is the question:
Whether tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles,
And by opposing end them? To die: to sleep;
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to, 'tis a consummation
Devoutly to be wish'd. To die, to sleep;
To sleep: perchance to dream: ay, there's the rub;
For in that sleep of death what dreams may come
When we have shuffled off this mortal coil,
Must give us pause: there's the respect
That makes calamity of so long life;
For who would bear the whips and scorns of time,
The oppressor's wrong, the proud man's contumely,
The pangs of despised love, the law's delay,
The insolence of office and the spurns
That patient merit of the unworthy takes,
When he himself might his quietus make
With a bare bodkin? who would fardels bear,
To grunt and sweat under a weary life,
But that the dread of something after death,
The undiscover'd country from whose bourn
No traveller returns, puzzles the will
And makes us rather bear those ills we have
Than fly to others that we know not of?
Thus conscience does make cowards of us all;
And thus the native hue of resolution
Is sicklied o'er with the pale cast of thought,
And enterprises of great pith and moment
With this regard their currents turn awry,
And lose the name of action. -Soft you now!
The fair Ophelia! Nymph, in thy orisons
Be all my sins remember'd.`;
  
  // Metadata URI (would typically point to IPFS or similar)
  const metadataURI = "ipfs://QmExample";  // Replace with actual metadata URI
  
  console.log("Publishing poem to the blockchain...");
  
  // Self-publish the poem (sender becomes the author)
  const tx = await poetryNFT.selfPublishPoem(poemTitle, poemText, metadataURI);
  
  // Wait for the transaction to be mined
  const receipt = await tx.wait();
  
  // Get the PoemPublished event
  const poemPublishedEvent = receipt.events.find(event => event.event === 'PoemPublished');
  const [tokenId, author, title] = poemPublishedEvent.args;
  
  console.log(`Successfully published poem with title: ${title}`);
  console.log(`Token ID: ${tokenId}`);
  console.log(`Author: ${author}`);
  console.log("Transaction hash:", tx.hash);

  // Retrieve the poem text from the contract to verify
  const retrievedPoemText = await poetryNFT.getPoemText(tokenId);
  console.log("\nVerifying stored poem text:");
  console.log("-------------------------");
  console.log(retrievedPoemText);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  }); 