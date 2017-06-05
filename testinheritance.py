class Parent():
    
    def PrintName(self):
        print(self.__class__.__name__)
    
class Child1(Parent):
    
    def __init__(self):
        self.PrintName()
        


class Child2(Parent):
    
    def __init__(self):
        self.PrintName()
        
c1 = Child1()
c2 = Child2()
        