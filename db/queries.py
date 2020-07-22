from sqlalchemy import create_engine
from conf import DATABASE_URI
from models import Price
from sqlalchemy.orm import sessionmaker


# todo date limit
def catalog():
    goods = []
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)

    s = Session()

    for row in s.query(Price):
        #print(row.good, row.good_description, row.price)
        goods.append(row)

    return goods

if __name__ == '__main__':
    catalog()
