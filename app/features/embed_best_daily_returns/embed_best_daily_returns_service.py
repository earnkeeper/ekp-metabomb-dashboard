from datetime import datetime


class EmbedBestDailyReturnService:
    def get_documents(self, listing_documents, currency):
        listing_documents.sort(key=lambda x: x["est_payback"])

        documents = []
        for i in range(0, 3):
            document = {}
            document["hero_rarity"] = listing_documents[i]['rarity_name']
            document["display_id"] = listing_documents[i]['display_id']
            document["token_id"] = listing_documents[i]['tokenId']
            document["cost"] = listing_documents[i]['priceFiat']
            document["daily"] = listing_documents[i]['fiat_per_day']
            document["fiatSymbol"] = currency['symbol']
            document["color"] = "success" if listing_documents[i]['fiat_per_day'] > 0 else "danger"
            documents.append(document)

        return documents
