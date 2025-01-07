class CoinFinder:
    def __init__(self, coins):
        self.exact_match_index = {}

        # Preprocess the dataset
        for coin in coins:
            for key in [coin["symbol"].lower(), coin["slug"].lower()]:
                # Add or replace only if the new coin has a better rank
                if (
                    key not in self.exact_match_index
                    or coin["rank"] < self.exact_match_index[key]["rank"]
                ):
                    self.exact_match_index[key] = coin

    def find_coin(self, user_input):
        query = user_input.strip().lower()

        # Check for exact matches in the index
        return self.exact_match_index.get(query, None)
