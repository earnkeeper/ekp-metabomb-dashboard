from datetime import datetime


class EmbedBoxesService:
    def get_documents(self, listing_documents, history_documents, currency):
        # pprint(listing_documents)
        floor_prices = {
            "Common Box": None,
            "Premium Box": None,
            "Ultra Box": None,
            "Bomb Box": None
        }

        avg_prices = {
            "Common Box": None,
            "Premium Box": None,
            "Ultra Box": None,
            "Bomb Box": None
        }

        count_boxes = {
            "Common Box": 0,
            "Premium Box": 0,
            "Ultra Box": 0,
            "Bomb Box": 0
        }
        perc_difference = {
            "Common Box": None,
            "Premium Box": None,
            "Ultra Box": None,
            "Bomb Box": None
        }
        
        colors = {
            "Common Box": "normal",
            "Premium Box": "normal",
            "Ultra Box": "normal",
            "Bomb Box": None
        }

        for listing in listing_documents:
            price_fiat = listing["priceFiat"]
            avg_price_fiat = listing["avgPriceFiat"]
            name = listing['name']
            count_boxes[name] += 1
            if (not floor_prices[name]) or (price_fiat < floor_prices[name]):
                floor_prices[name] = price_fiat
            if (not avg_prices[name]) and avg_price_fiat:
                avg_prices[name] = avg_price_fiat
            perc_difference[name] = None
            if floor_prices[name] and avg_prices[name]:
                perc_difference[name] = (floor_prices[name] - avg_prices[name]) / avg_prices[name] * 100

        
        def set_color(box_type):
            if perc_difference[box_type] and (perc_difference[box_type] < 0):
                colors[box_type] = "danger"
            if perc_difference[box_type] and (perc_difference[box_type] > 0):
                colors[box_type] = "success"

        set_color("Common Box")
        set_color("Premium Box")
        set_color("Ultra Box")
        set_color("Bomb Box")
        
        document = {
                "id": "0",
                "updated": datetime.now().timestamp(),
        }
        
        def set_document_box(box_id, box_type):
            document[box_id] = {
                    "name": box_type,
                    "countBoxes": count_boxes[box_type],
                    "percDiff": perc_difference[box_type],
                    "floorPrice": floor_prices[box_type],
                    "avgPrice": avg_prices[box_type],
                    "fiatSymbol": currency["symbol"],
                    "color": colors[box_type],                
            }
            
        set_document_box("common", "Common Box")
        set_document_box("premium", "Premium Box")
        set_document_box("ultra", "Ultra Box")
        set_document_box("bomb", "Bomb Box")
            
        return [document]
