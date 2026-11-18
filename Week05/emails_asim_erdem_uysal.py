


class Emails(list):

    def __init__(self, data):
        self.data = self.validate(data)
        super().__init__(self.data)
       
        


    def validate(self,data):
        temiz=[]
        for i in  data:
            
            if not isinstance(i,str):
                raise ValueError
            elif i.count("@") != 1 :
                raise ValueError
            elif "." not in i.split("@")[1]  :
                raise ValueError
            else:
                if i not in temiz:
                    temiz.append(i)

            
        return temiz
            
               
    def __str__(self):
        return f"Emails: {', '.join(self.data)}"

    def __repr__(self):
        return f"Emails({self.data})"
    