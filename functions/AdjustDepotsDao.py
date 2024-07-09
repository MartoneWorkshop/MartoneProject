


class Deposito:
    def __init__(self, codDep, name_dep, date_created, date_update):
        self.id = None
        self.codDep = codDep
        self.name_dep = name_dep
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Deposito[{self.codDep}, {self.name_dep}, {self.date_created}, {self.date_update}]'
