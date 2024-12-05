import binascii

class Barcode:
    def __init__(self, barcode: int, name: str, shugar: int, fats: int, squirrels: int, carbohydrates: int) -> None:
        self.barcode = barcode
        self.name = binascii.unhexlify(name).decode()
        self.shugar = shugar
        self.fats = fats
        self.squirrels = squirrels
        self.carbohydrates = carbohydrates
    

    def get_json(self) -> dict:
        result = {
                'statusCode': 200,
                'body': {
                    'barcode': self.barcode,
                    'name': self.name,
                    'shugar': self.shugar,
                    'fats': self.fats,
                    'squirrels': self.squirrels,
                    'carbohydrates': self.carbohydrates
                }
            }
        return result

    
