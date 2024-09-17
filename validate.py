class myvalidate:
    def required(self,frm):
        for f in frm:
            if f=="":
                return False
        return True


    def mustdigit(self,m):
        if(m.isdigit() and len(m)==10):
            return True
        
        return False