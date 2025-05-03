async function main() {
  // Get the contract factory
  const PoetryNFT = await ethers.getContractFactory("PoetryNFT");

  // Deploy the contract
  const poetryNFT = await PoetryNFT.deploy();
  
  // Wait for deployment to finish
  await poetryNFT.deployed();
  
  console.log("PoetryNFT contract deployed to address:", poetryNFT.address);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  }); 