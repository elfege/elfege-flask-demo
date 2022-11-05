from forex_python.converter import CurrencyRates, CurrencyCodes
import json
import re


class Converter:
    """
    Class that gets currency rates from forex and converts any given currency

    """

    def __init__(self, FROM, TO, amount):
        self.FROM = FROM
        self.TO = TO
        self.amount = float(amount)

    def __repr__(self):
        return f"Conversion of {self.amount} from {self.FROM} to {self.TO}"

    def convert(self):
        """
        Convert an amount in a certain currency to a desired currency

        - test that converts 1 USD to 1 USD
        >>> CurrencyRates().get_rate("USD", "USD")
        1.0

        """

        print(f"Converting {self.amount} from {self.FROM} to {self.TO}")

        return CurrencyRates().convert(self.FROM, self.TO, self.amount)

    # def currencies_list(self):
    #     return

    if __name__ == "__main__":
        import doctest
        doctest.testmod()


def codes():
    curr = CurrencyRates().get_rates("").keys()  # get a list of all currencies
    curr = list(curr)
    curr.append("EUR") # add EUR, which is missing for some reason... 
    curr.sort()
    return curr


def checkString(amount):
    """Check that the amount parameter received through the html form is a valid series of string digits
    
    >>> bool(re.match('^[\.0-9]*$', "25"))
    True
    >>> bool(re.match('^[\.0-9]*$', "25.25854")) 
    True
    >>> bool(re.match('^[\.0-9]*$', "25dfhjdf"))
    False
    >>> bool(re.match('^[\.0-9]*$', "dfkdfhe dh"))
    False
    
    """
    if re.match('^[\.0-9]*$', amount):
        return True
    else:
        return False
    
    
def all_rates():
    
    rates = CurrencyRates().get_rates("USD")
    rates = dict((k, round(rates[k],3)) for k in rates) # [round(v, 4) for v in rates.values()]
    print(f"||||||||||||||||||||{rates}")
    return rates