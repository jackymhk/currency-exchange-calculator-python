from tkinter.tix import INTEGER
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup

class ConverterViews(APIView):
    def get(self, request):
        try:
            fromCcy = request.query_params.get("from")
            toCcy = request.query_params.get("to")
            amount = request.query_params.get("amount")
            rate = None

            # Check parameter
            missingParams = []
            if fromCcy is None:
                missingParams.append("from")
            if toCcy is None:
                missingParams.append("to")
            if amount is None:
                missingParams.append("amount")

            if len(missingParams) > 0:
                return Response({"error": "Missing parameters: {MISSING_PARAM}".format(MISSING_PARAM=", ".join(missingParams))}, status=status.HTTP_400_BAD_REQUEST)

            try:
                amount = float(amount)
            except ValueError:
                return Response({"error": "amount should be number"}, status=status.HTTP_400_BAD_REQUEST)

            url = "https://finance.yahoo.com/quote/{FROM}{TO}=X".format(FROM=fromCcy, TO=toCcy)
            page = requests.get(url, headers={'USER-AGENT': "Mozilla/5.0"})

            soup = BeautifulSoup(page.content, "html.parser")
            finStreamerElements = soup.find_all(
                'fin-streamer', 
                attrs = {
                    "data-field": "regularMarketPrice", 
                    "data-test": "qsp-price"
                }
            )

            for finStreamerElement in finStreamerElements:
                rate = float(finStreamerElement.attrs['value'])

            if rate is None:
                return Response({"error": "Unknown Currency"}, status=status.HTTP_400_BAD_REQUEST)
            
            convertedAmount = amount * rate

            result = {
                "from": fromCcy,
                "to": toCcy,
                "rate": rate,
                "amount": convertedAmount
            }

            return Response(result, status=status.HTTP_200_OK)

        except:
            return Response({"error": "error"}, status=status.HTTP_500_BAD_REQUEST)