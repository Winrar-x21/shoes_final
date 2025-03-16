class Address:
    def __init__(self, label, address):
        self.label = label
        self.address = address

    
    def to_dict(self):
        return dict(label=self.label, address=self.address)
    

    @classmethod
    def from_dict(cls, config):
        return Address(label=config['label'], 
                            address=config['address'])
        