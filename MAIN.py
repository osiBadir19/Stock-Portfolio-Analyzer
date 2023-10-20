import yfinance
from requests.exceptions import HTTPError


class StockPortfolioAnalyzer:
    def __init__(self, portfolio: list):
        # [ (ticker, shares, price), .... ]
        self.portfolio = portfolio

    def __str__(self):
        if len(self.portfolio) >= 1:
            return ''.join([f"Stock: {stock_name}"
                            f"\nNumber of Shares: {number_of_share}"
                            f"\nStock Price: {stock_price}"
                            f"\n-------------------------------\n"
                            for stock_name, number_of_share, stock_price in self.portfolio])

        else:
            return "empty Portfolio"

    def __delitem__(self, stock_name: str):
        self.portfolio = [stock for stock in self.portfolio if stock[0] != stock_name]

    def __setitem__(self, stock_name, stock_details):
        #check if the stock exists in the portfolio
        for index, (ticker, shares, prices) in enumerate(self.portfolio):
            if ticker == stock_name:
            # update the stock details in the portfolio
                self.portfolio[index] = (stock_name, *stock_details)
                break

            else:
                self.portfolio.append((stock_name, *stock_details))



    def calculate_value_of_portfolio(self):
        """
        a function to calculate the value of portfolio given current market prices
        :return: a list containing current portfolio values
        """
        current_value = [round(self.gather_stock_price(ticker[0]))*ticker[1] for ticker in self.portfolio]
        return current_value



    def total_profit_or_loss(self):
        """
        A function that calculates the profit or loss for the stocks in the portfolio
        :return:  PnL
        """
        PnL_stocks = [round(self.gather_stock_price(ticker[0])*ticker[1] - ticker[1]*ticker[2])
               for ticker in self.portfolio]

        Pnl_portfolio = sum(PnL_stocks)
        return f"Stocks individual PnL: {PnL_stocks}\nTotal Portfolio PnL: ${Pnl_portfolio}"


    @staticmethod
    def gather_stock_price(stock_name: str):
        """
        :param stock_name: name of stock you need its price
        :return: Price of stock
        """
        try:
            ticker = yfinance.Ticker(stock_name)
            close_price = ticker.history()['Close'].iloc[-1]
            return round(close_price, 2)

        except HTTPError:
            print(f"Netowrk error while fetching price of {stock_name}")

        except KeyError:
            print(f"Data for {stock_name} not found. error in stock name")

        except Exception as e:
            print(f"Error fetching price for {stock_name}")
            return None



    def sector_matching(self):
        """
        :return: match the stocks in portfolio with U.S. economic sectors
        """
        for stock_name, *others in self.portfolio:
            match stock_name:
                case 'AAPL' | 'MSFT' | 'QQQ':
                    print(f"{stock_name} is part of Technology Sector")

                case 'F'| 'GM'| 'LI':
                    print(f"{stock_name} is part of Automobile Sector")

                case 'BA'| 'NOC'| 'GD':
                    print(f"{stock_name} is part of Defense and Airspace Sector")

                case _:
                    print(f"{stock_name} Sector couldn't be unidentified")




    def sort(self, method='ascending'):
        """
        :param method: method of sorting (default is ascending)
        :return: Nothing. it just sorts the main Portfolio
        """
        if method.lower() != 'ascending':
            raise ValueError("Invalid Sorting Method")
        else:
            stock_values = self.calculate_value_of_portfolio()
            self.portfolio = sorted(self.portfolio, key=lambda x: stock_values[self.portfolio.index(x)])
            return None



# TODO: Example Usage
portfolio_data_1 = [
    ('AAPL', 50, 130.00),  # 50 shares of Apple purchased at $130.00 each
    ('MSFT', 30, 200.00),  # 30 shares of Microsoft purchased at $200.00 each
    ('AMZN', 10, 3100.00)  # 10 shares of Amazon purchased at $3100.00 each
]
portfolio_1 = StockPortfolioAnalyzer(portfolio_data_1)
print(portfolio_1)
portfolio_1['AAPL'] = (12, 136.00)
print(f"New: \n{portfolio_1}")


