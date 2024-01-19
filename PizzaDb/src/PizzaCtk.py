from PizzaDb import PizzaDb
from PizzaGuiCtk import PizzaGuiCtk

def main():
    db = PizzaDb(init=False, dbName='PizzaDb.csv')
    app = PizzaGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()
    