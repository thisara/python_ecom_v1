
class ProductData():
    def __init__(self, code, name, stock, version):
        self.code = code
        self.name = name
        self.stock = stock
        self.version = version

class ProductOderItemData():
    def __init__(self, code, stock, orderRef, version):
        self.code = code
        self.stock = stock
        self.orderRef = orderRef
        self.version = version


