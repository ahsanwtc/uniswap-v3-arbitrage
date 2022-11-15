require('dotenv').config();
const { ethers } = require('ethers');
const provider = new ethers.providers.JsonRpcProvider(process.env.PROVIDER);
const PROFIT_THRESHOLD = 0;

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
      name, symbol, decimals, address
    });
  }

  /* token order changes depending on the trade direction i.e. base_to_quoute or quote_to_base */
  /* need to identify the correct token to input as A and B */
  let inputTokenA = '', inputDecimalsA = 0, inputTokenB = '', inputDecimalsB = 0;
  switch (tradeDirection) {
    case 'base_to_quote': {
      inputTokenA = tokenInfoArray[0].address;
      inputDecimalsA = tokenInfoArray[0].decimals;
      inputTokenB = tokenInfoArray[1].address;
      inputDecimalsB = tokenInfoArray[1].decimals;

      break;
    }
    case 'quote_to_base': {
      inputTokenA = tokenInfoArray[1].address;
      inputDecimalsA = tokenInfoArray[1].decimals;
      inputTokenB = tokenInfoArray[0].address;
      inputDecimalsB = tokenInfoArray[0].decimals;
      break;
    }
    default:
  }

  /* reformat amount in */
  if (!isNaN(amount)) { amount = amount.toString(); }
  const amountIn = ethers.utils.parseUnits(amount, inputDecimalsA).toString();

  /* get uniswap v3 Quote */
  const quoterAddress = '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6';
  const quoterContract = new ethers.Contract(quoterAddress, QuoterABI, provider);
  let quotedAmountOut = 0;

  try {
    quotedAmountOut = await quoterContract.callStatic.quoteExactInputSingle(
      inputTokenA, inputTokenB, fee, amountIn, 0
    );
  } catch (error) {
    console.log(error);
    return 0;
  }

  /* format output */
  return ethers.utils.formatUnits(quotedAmountOut, inputDecimalsB).toString();

};

const calculateArbitrage = ({ amountIn, amountOut, details }) => {
  const profitLoss = amountOut - amountIn;
  if (profitLoss > PROFIT_THRESHOLD) {
    const profitLossPercentage = (profitLoss / amountIn) * 100;
    console.log([details, { profitLossPercentage }]);
  }
};

const getDepth = async amountIn => {  
  /* get JSON surface rates */
  const fileInfo = getFile('./uniswap_surface_rates.json');
  const surfaceRatesParsed = JSON.parse(fileInfo);
  const LIMIT = surfaceRatesParsed.length;
  const surfaceRates = surfaceRatesParsed.slice(0, LIMIT);
  
  console.log('reading surface rate information...');
  console.log(`LIMIT = ${LIMIT}`);

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
    const acquiredCoinT1 = await getPrice(pairContract1Address, amountIn, trade1Direction);
    if (acquiredCoinT1 === 0) { return; }

    /* Trade 2 */
    console.log('Checking trade 2 acquired coin...');
    const acquiredCoinT2 = await getPrice(pairContract2Address, acquiredCoinT1, trade2Direction);
    if (acquiredCoinT2 === 0) { return; }

    /* Trade 3 */
    console.log('Checking trade 3 acquired coin...');
    const acquiredCoinT3 = await getPrice(pairContract3Address, acquiredCoinT2, trade3Direction);

    /* calculate and show resutlts */
    calculateArbitrage({ amountIn, amountOut: acquiredCoinT3, details: surfaceRates[i] });
  }

  return 
};

getDepth(100);

