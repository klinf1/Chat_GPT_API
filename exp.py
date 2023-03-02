class A:
    instances = []

    def __init__(self, id) -> None:
        self.id = id
        self.__class__.instances.append(self.id)

    @classmethod
    def printInstances(cls):
        for instance in cls.instances:
            print(instance)

    def __str__(self):
        return str(self.id)

    def __repr__(self) -> str:
        return str(self.id)
    
    def delete_instance(self):
        self.__class__.instances.remove(self.id)


a = A(1)
b = A(2)



def another_check(number: int):


    if  number in A.instances:
        print(f'this exists already, see {A.instances}, {number}')
        newer_instance = A(number)
        print(f'{A.instances}, newer instance {newer_instance}')
        newer_instance.delete_instance()
        print(A.instances)
        del newer_instance

another_check(1)
