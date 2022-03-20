# currency-exchange-calculator-python
A simple currency exchange calculator API using Python. It scrapers live exchange rate from Yahoo Finance
* Python
* Django
* Django Rest framework
* BeautifulSoup
* Heroku

## Usage
```
/converter/?from=<From Currency>&to=<To Currency>&amount=<amount to convert>
```
Result
```
{
    "from": <From Currency>,
    "to": <To Currency>,
    "rate": <Exchange Rate>,
    "amount": <Converted Amount>
}
```
