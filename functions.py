# Structure trading pair groups
def structure_trading_pairs(pairs, limit):
    triangular_pairs_list = []
    remove_duplicates_list = []
    pairs_list = pairs[:limit]

    # Loop through each coin to find potential matches
    for pair_a in pairs_list:
        # Get first pair A
        a_base = pair_a['token0']['symbol']
        a_quote = pair_a['token1']['symbol']
        a_pair = a_base + '_' + a_quote
        a_token_0_id = pair_a['token0']['id']
        a_token_1_id = pair_a['token1']['id']
        a_contract = pair_a['id']
        a_token_0_decimals = pair_a['token0']['decimals']
        a_token_1_decimals = pair_a['token1']['decimals']
        a_token_0_price = pair_a['token0Price']
        a_token_1_price = pair_a['token1Price']

        # Put A into box for checking at B
        a_pair_box = [a_base, a_quote]

        # Get second pair B
        for pair_b in pairs_list:
            b_base = pair_b['token0']['symbol']
            b_quote = pair_b['token1']['symbol']
            b_pair = b_base + '_' + b_quote
            b_token_0_id = pair_b['token0']['id']
            b_token_1_id = pair_b['token1']['id']
            b_contract = pair_b['id']
            b_token_0_decimals = pair_b['token0']['decimals']
            b_token_1_decimals = pair_b['token1']['decimals']
            b_token_0_price = pair_b['token0Price']
            b_token_1_price = pair_b['token1Price']

            # For third pair C
            if a_pair != b_pair:
                if b_base in a_pair_box or b_quote in a_pair_box:

                    # Get third pair C
                    for pair_c in pairs_list:
                        c_base = pair_c['token0']['symbol']
                        c_quote = pair_c['token1']['symbol']
                        c_pair = c_base + '_' + c_quote
                        c_token_0_id = pair_c['token0']['id']
                        c_token_1_id = pair_c['token1']['id']
                        c_contract = pair_c['id']
                        c_token_0_decimals = pair_c['token0']['decimals']
                        c_token_1_decimals = pair_c['token1']['decimals']
                        c_token_0_price = pair_c['token0Price']
                        c_token_1_price = pair_c['token1Price']

                        # Count number of C items
                        if c_pair != a_pair and c_pair != b_pair:
                            combine_all = [a_pair, b_pair, c_pair]
                            pair_box = [a_base, a_quote, b_base, b_quote, c_base, c_quote]

                            counts_c_base = 0
                            for i in pair_box:
                                if i == c_base:
                                    counts_c_base += 1

                            counts_c_quote = 0
                            for i in pair_box:
                                if i == c_quote:
                                    counts_c_quote += 1

                            if counts_c_base == 2 and counts_c_quote == 2 and c_base != c_quote:
                                combined = a_pair + ',' + b_pair + ',' + c_pair
                                unique_string = ''.join(sorted(combined))

                                # Output pairs
                                if unique_string not in remove_duplicates_list:
                                    output_dictionary = {
                                        'a_pair': a_pair,
                                        'a_base': a_base,
                                        'a_quote': a_quote,
                                        'b_pair': b_pair,
                                        'b_base': b_base,
                                        'b_quote': b_quote,
                                        'c_pair': c_pair,
                                        'c_base': c_base,
                                        'c_quote': c_quote,
                                        'combined': combined,
                                        'a_token_0_id': a_token_0_id,
                                        'b_token_0_id': b_token_0_id,
                                        'c_token_0_id': c_token_0_id,
                                        'a_token_1_id': a_token_1_id,
                                        'b_token_1_id': b_token_1_id,
                                        'c_token_1_id': c_token_1_id,
                                        'a_contract': a_contract,
                                        'b_contract': b_contract,
                                        'c_contract': c_contract,
                                        'a_token_0_decimals': a_token_0_decimals,
                                        'b_token_0_decimals': b_token_0_decimals,
                                        'c_token_0_decimals': c_token_0_decimals,
                                        'a_token_1_decimals': a_token_1_decimals,
                                        'b_token_1_decimals': b_token_1_decimals,
                                        'c_token_1_decimals': c_token_1_decimals,
                                        'a_token_0_price': a_token_0_price,
                                        'a_token_1_price': a_token_1_price,
                                        'b_token_0_price': b_token_0_price,
                                        'b_token_1_price': b_token_1_price,
                                        'c_token_0_price': c_token_0_price,
                                        'c_token_1_price': c_token_1_price,
                                    }
                                    triangular_pairs_list.append(output_dictionary)
                                    remove_duplicates_list.append(unique_string)

    return triangular_pairs_list

# Calculate surface arbitrage potential
def calculate_triangular_arbitrage_surface_rate(t_pair, min_rate):
    # Set variables
    min_surface_rate = min_rate
    starting_amount = 1
    surface_dictionary = {}
    pool_contract_1 = ''
    pool_contract_2 = ''
    pool_contract_3 = ''
    pool_direction_trade_1 = ''
    pool_direction_trade_2 = ''
    pool_direction_trade_3 = ''
    acquired_coin_t1 = 0
    acquired_coin_t2 = 0
    acquired_coin_t3 = 0
    calculated = False
    swap_1 = 0
    swap_2 = 0
    swap_3 = 0
    swap_1_rate = 0
    swap_2_rate = 0
    swap_3_rate = 0


    # Calculate looping through forward and reverse rates
    direction_list = ['forward', 'reverse']
    for direction in direction_list:
        # Set pair info
        a_base = t_pair['a_base']
        a_quote = t_pair['a_quote']
        b_base = t_pair['b_base']
        b_quote = t_pair['b_quote']
        c_base = t_pair['c_base']
        c_quote = t_pair['c_quote']

        # Set price info
        a_token_0_price = float(t_pair['a_token_0_price'])
        a_token_1_price = float(t_pair['a_token_1_price'])
        b_token_0_price = float(t_pair['b_token_0_price'])
        b_token_1_price = float(t_pair['b_token_1_price'])
        c_token_0_price = float(t_pair['c_token_0_price'])
        c_token_1_price = float(t_pair['c_token_1_price'])

        # Set address info
        a_contract = t_pair['a_contract']
        b_contract = t_pair['b_contract']
        c_contract = t_pair['c_contract']

        # Assume start with a_base if forward
        if direction == 'forward':
            swap_1 = a_base
            swap_2 = a_quote
            swap_1_rate = a_token_1_price
            pool_direction_trade_1 = 'base_to_quote'

        # Assume start with a_quote if reverse
        if direction == 'reverse':
            swap_1 = a_quote
            swap_2 = a_base
            swap_1_rate = a_token_0_price
            pool_direction_trade_1 = 'quote_to_base'

        # Place first trade
        pool_contract_1 = a_contract
        acquired_coin_t1 = starting_amount * swap_1_rate

        # Forward 1: check if a_quote (acquired coin) matches b_quote
        if direction == 'forward' and (a_quote == b_quote and calculated is False):
            swap_2_rate = b_token_0_price
            acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
            pool_direction_trade_2 = 'quote_to_base'
            pool_contract_2 = b_contract

            # Forward: check if b_base (acquired coin) matches c_base
            if b_base == c_base:
                swap_3 = c_base
                swap_3_rate = c_token_1_price
                pool_direction_trade_3 = 'base_to_quote'
                pool_contract_3 = c_contract

            # Forward: check if b_base (acquire coin) matches c_quote
            if b_base == c_quote:
                swap_3 = c_quote
                swap_3_rate = c_token_0_price
                pool_direction_trade_3 = 'quote_to_base'
                pool_contract_3 = c_contract

            acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
            calculated = True

        # Forward 2: check if a_quote (acquired coin) matches b_base
        if direction == 'forward' and (a_quote == b_base and calculated is False):
            swap_2_rate = b_token_1_price
            acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
            pool_direction_trade_2 = 'base_to_quote'
            pool_contract_2 = b_contract

            # Forward: check if b_base (acquired coin) matches c_base
            if b_base == c_base:
                swap_3 = c_base
                swap_3_rate = c_token_1_price
                pool_direction_trade_3 = 'base_to_quote'
                pool_contract_3 = c_contract

            # Forward: check if b_base (acquired coin) matches c_quote
            if b_base == c_quote:
                swap_3 = c_quote
                swap_3_rate = c_token_0_price
                pool_direction_trade_3 = 'quote_to_base'
                pool_contract_3 = c_contract

            acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
            calculated = True

        # Forward 3: check if a_quote (acquired coin) matches c_quote
        if direction == 'forward' and (a_quote == c_quote and calculated is False):
            swap_2_rate = c_token_0_price
            acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
            pool_direction_trade_2 = 'quote_to_base'
            pool_contract_2 = c_contract

            # Forward: check if c_base (acquired coin) matches b_base
            if c_base == b_base:
                swap_3 = b_base
                swap_3_rate = b_token_1_price
                pool_direction_trade_3 = 'base_to_quote'
                pool_contract_3 = b_contract

            # Forward: check if c_base (acquired coin) matches b_quote
            if c_base == b_quote:
                swap_3 = b_quote
                swap_3_rate = b_token_0_price
                pool_direction_trade_3 = 'quote_to_base'
                pool_contract_3 = b_contract

            acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
            calculated = True

        # Forward 4: check if a_quote (acquired coin) matches c_base
        if direction == 'forward' and (a_quote == c_base and calculated is False):
            swap_2_rate = c_token_1_price
            acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
            pool_direction_trade_2 = 'base_to_quote'
            pool_contract_2 = c_contract

            # Forward: check if c_quote (acquired coin) matches b_base
            if c_quote == b_base:
                swap_3 = b_base
                swap_3_rate = b_token_1_price
                pool_direction_trade_3 = 'base_to_quote'
                pool_contract_3 = b_contract

            # Forward: check if c_quote (acquired coin) matches b_quote
            if c_quote == b_quote:
                swap_3 = b_quote
                swap_3_rate = b_token_0_price
                pool_direction_trade_3 = 'quote_to_base'
                pool_contract_3 = b_contract

            acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
            calculated = True

        # Reverse 1: check if a_base (acquired coin) matches b_quote
        if direction == 'reverse' and (a_base == b_quote and calculated is False):
            swap_2_rate = b_token_0_price
            acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
            pool_direction_trade_2 = 'quote_to_base'
            pool_contract_2 = b_contract

            # check if b_base (acquired coin) matches c_base
            if b_base == c_base:
                swap_3 = c_base
                swap_3_rate = c_token_1_price
                pool_direction_trade_3 = 'base_to_quote'
                pool_contract_3 = c_contract

            # check if b_base (acquire coin) matches c_quote
            if b_base == c_quote:
                swap_3 = c_quote
                swap_3_rate = c_token_0_price
                pool_direction_trade_3 = 'quote_to_base'
                pool_contract_3 = c_contract

            acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
            calculated = True

        # Reverse 2: check if a_base (acquired coin) matches b_base
        if direction == 'reverse' and (a_base == b_base and calculated is False):
            swap_2_rate = b_token_1_price
            acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
            pool_direction_trade_2 = 'base_to_quote'
            pool_contract_2 = b_contract

            # check if b_quote (acquired coin) matches c_base
            if b_quote == c_base:
                swap_3 = c_base
                swap_3_rate = c_token_1_price
                pool_direction_trade_3 = 'base_to_quote'
                pool_contract_3 = c_contract

            # check if b_quote (acquired coin) matches c_quote
            if b_base == c_quote:
                swap_3 = c_quote
                swap_3_rate = c_token_0_price
                pool_direction_trade_3 = 'quote_to_base'
                pool_contract_3 = c_contract

            acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
            calculated = True

        # Reverse 3: check if a_base (acquired coin) matches c_quote
        if direction == 'reverse' and (a_base == c_quote and calculated is False):
            swap_2_rate = c_token_0_price
            acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
            pool_direction_trade_2 = 'quote_to_base'
            pool_contract_2 = c_contract

            # check if c_base (acquired coin) matches b_base
            if c_base == b_base:
                swap_3 = b_base
                swap_3_rate = b_token_1_price
                pool_direction_trade_3 = 'base_to_quote'
                pool_contract_3 = b_contract

            # check if c_base (acquired coin) matches b_quote
            if c_base == b_quote:
                swap_3 = b_quote
                swap_3_rate = b_token_0_price
                pool_direction_trade_3 = 'quote_to_base'
                pool_contract_3 = b_contract

            acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
            calculated = True

        # Reverse 4: check if a_base (acquired coin) matches c_base
        if direction == 'reverse' and (a_base == c_base and calculated is False):
            swap_2_rate = c_token_1_price
            acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
            pool_direction_trade_2 = 'base_to_quote'
            pool_contract_2 = c_contract

            # check if c_quote (acquired coin) matches b_base
            if c_quote == b_base:
                swap_3 = b_base
                swap_3_rate = b_token_1_price
                pool_direction_trade_3 = 'base_to_quote'
                pool_contract_3 = b_contract

            # check if c_quote (acquired coin) matches b_quote
            if c_quote == b_quote:
                swap_3 = b_quote
                swap_3_rate = b_token_0_price
                pool_direction_trade_3 = 'quote_to_base'
                pool_contract_3 = b_contract

            acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
            calculated = True

        # Calculate arbitrage results
        profit_loss = acquired_coin_t3 - starting_amount
        profit_loss_percentage = (profit_loss / starting_amount) * 100 if profit_loss != 0 else 0

        # Format descriptions
        trade_description_1 = f"Start with {swap_1} of {starting_amount}. Swap at {swap_1_rate} for {swap_2} " \
                              f"acquiring {acquired_coin_t1}."
        trade_description_2 = f"Swap {acquired_coin_t1} of {swap_2} at {swap_2_rate} for {swap_3} acquiring " \
                              f"{acquired_coin_t2}."
        trade_description_3 = f"Swap {acquired_coin_t2} of {swap_3} at {swap_3_rate} for {swap_1} acquiring " \
                              f"{acquired_coin_t3}."

        # Filter for significant opportunity size
        if profit_loss_percentage >= min_surface_rate:
            surface_dictionary = {
                "swap_1": swap_1,
                "swap_2": swap_2,
                "swap_3": swap_3,
                "pool_contract_1": pool_contract_1,
                "pool_contract_2": pool_contract_2,
                "pool_contract_3": pool_contract_3,
                "pool_direction_trade_1": pool_direction_trade_1,
                "pool_direction_trade_2": pool_direction_trade_2,
                "pool_direction_trade_3": pool_direction_trade_3,
                "starting_amount": starting_amount,
                "acquired_coin_t1": acquired_coin_t1,
                "acquired_coin_t2": acquired_coin_t2,
                "acquired_coin_t3": acquired_coin_t3,
                "swap_1_rate": swap_1_rate,
                "swap_2_rate": swap_2_rate,
                "swap_3_rate": swap_3_rate,
                "profit_loss": profit_loss,
                "profit_loss_percentage": profit_loss_percentage,
                "direction": direction,
                "trade_description_1": trade_description_1,
                "trade_description_2": trade_description_2,
                "trade_description_3": trade_description_3
            }
            return surface_dictionary

    return surface_dictionary
