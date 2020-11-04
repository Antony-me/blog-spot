import urllib.request
from .models import Quote
import json


def get_quotes():

    base_url = 'http://quotes.stormconsultancy.co.uk/random.json'
    '''
    Function that gets the json response to our qoutes requests
    '''
    with urllib.request.urlopen(base_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

        quote_results = None

        if get_quotes_response:
            quote = get_quotes_response.get('quote')
            author = get_quotes_response.get('author')

            quote_results = Quote(quote,author)
    return quote_results


