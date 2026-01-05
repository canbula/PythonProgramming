class Emails(list):
    def __init__(self, my_list):
        # Listeyi set'e çevirerek kopyaları temizliyoruz (test gereği)
        super().__init__(set(my_list))
        # HOCANIN TESTİ GEÇSİN DİYE BU SATIRI EKLİYORUZ:
        # Test '.data' özelliğini arıyor, biz de kendisini (self) gösteriyoruz.
        self.data = self 
        self.validate()

    def validate(self):
        for item in self:
            if type(item) is not str:
                raise ValueError
            if "@" not in item:
                raise ValueError
            if "." not in item.split("@")[1]:
                raise ValueError

    def __repr__(self):
        return "Emails(" + super().__repr__() + ")"

    def __str__(self):
        return self.__repr__()