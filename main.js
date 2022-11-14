require('dotenv').config();
const { ethers } = require('ethers');
const provider = new ethers.providers.JsonRpcProvider(process.env.PROVIDER);

const QuoterABI = require('@uniswap/v3-periphery/artifacts/contracts/lens/Quoter.sol/Quoter.json').abi;

const getFile = filePath => {
  const fs = require('fs');
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    return data;
  } catch (error) {
    console.log(error);
    return [];
  }
};

const getPrice = async (factory, amount, tradeDirection) => {
  const ABI = [
    'function token0() external view returns (address)',
    'function token1() external view returns (address)',
    'function fee() external view returns (uint24)',
  ];
  const poolContract = new ethers.Contract(factory, ABI, provider);
  const token0Address = await poolContract.token0();
  const token1Address = await poolContract.token1();
  const fee = await poolContract.fee();
  
  const addressArray = [token0Address, token1Address];
  const tokenInfoArray = [];
  
  for (let i = 0; i < addressArray.length; i++) {
    const address = addressArray[i];
    const abi = [
      'function name() external view returns (string)',
      'function symbol() external view returns (string)',
      'function decimals() external view returns (uint)',
    ];
    const contract = new ethers.Contract(address, abi, provider);
    const symbol = await contract.symbol();
    const name = await contract.name();
    const decimals = await contract.decimals();
    tokenInfoArray.push({
      id: `token${i}`,
      name, symbol, decimals
    });
  }
  console.log(tokenInfoArray);

};

const getDepth = async (amountIn, limit) => {  
  /* get JSON surface rates */
  console.log('reading surface rate information...');
  const fileInfo = getFile('./uniswap_surface_rates.json');
  const surfaceRatesParsed = JSON.parse(fileInfo);
  const surfaceRates = surfaceRatesParsed.slice(0, limit);

  /* loop through each trade and get price information */
  for (let i = 0; i < surfaceRates.length; i++) {
    const pairContract1Address = surfaceRates[i].pool_contract_1;
    const pairContract2Address = surfaceRates[i].pool_contract_2;
    const pairContract3Address = surfaceRates[i].pool_contract_3;
    const trade1Direction = surfaceRates[i].pool_direction_trade_1;
    const trade2Direction = surfaceRates[i].pool_direction_trade_2;
    const trade3Direction = surfaceRates[i].pool_direction_trade_3;

    /* Trade 1 */
    console.log('Checking trade 1 acquired coin...');
    const acquiredCoinDetailT1 = await getPrice(pairContract1Address, amountIn, trade1Direction);

    /* Trade 2 */
    console.log('Checking trade 2 acquired coin...');

    /* Trade 3 */
    console.log('Checking trade 3 acquired coin...');

  }

  return 
};

getDepth(1, 1);

