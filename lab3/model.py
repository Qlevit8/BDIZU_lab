from random import randrange
import string
import random
import psycopg2 as ps
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, select, and_
from sqlalchemy.orm import relationship
from connect import Orders, Session, engine
from sqlalchemy import func
import datetime


class customer(Orders):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    customer_surname = Column(String)

    def __init__(self, customer_id, customer_name, customer_surname):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_surname = customer_surname

    def __repr__(self):
        return 'id: ' + str(self.customer_id) + \
               ' || name: ' + self.customer_name + \
               ' || surname: ' + self.customer_surname


class book(Orders):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    price = Column(Integer)

    def __init__(self, book_id, title, author, genre, price):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price

    def __repr__(self):
        return 'book_id: ' + str(self.book_id) + \
               ' || title: ' + self.title + \
               ' || author: ' + self.author + \
               ' || genre ' + self.genre + \
               ' || price: ' + str(self.price)


class discount_card(Orders):
    __tablename__ = 'discount_card'
    discount_card_id = Column(Integer, primary_key=True)
    date_of_expiring = Column(Date)
    percentage = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))

    def __init__(self, discount_card_id, date_of_expiring, percentage, customer_id):
        self.discount_card_id = discount_card_id
        self.date_of_expiring = date_of_expiring
        self.percentage = percentage
        self.customer_id = customer_id

    def __repr__(self):
        return 'discount_card_id: ' + str(self.discount_card_id) + \
               ' || date_of_expiring: ' + str(self.date_of_expiring) + \
               ' || percentage: ' + str(self.percentage) + \
               ' || customer_id: ' + str(self.customer_id)


class order(Orders):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True)
    date = Column(Date)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    discount_card_id = Column(Integer, ForeignKey('discount_card.discount_card_id'))

    def __init__(self, order_id, date, customer_id, discount_card_id):
        self.order_id = order_id
        self.date = date
        self.customer_id = customer_id
        self.discount_card_id = discount_card_id

    def __repr__(self):
        return 'order_id: ' + str(self.order_id) + \
               ' || date: ' + str(self.date) + \
               ' || customer_id: ' + str(self.customer_id) + \
               ' || discount_card_id: ' + str(self.discount_card_id)


class book_order(Orders):
    __tablename__ = 'book_order'
    book_order_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.book_id'))
    order_id = Column(Integer, ForeignKey('order.order_id'))

    def __init__(self, book_order_id, book_id, order_id):
        self.book_order_id = book_order_id
        self.book_id = book_id
        self.order_id = order_id

    def __repr__(self):
        return 'book_order_id: ' + str(self.book_order_id) + \
               ' || book_id: ' + str(self.book_id) + \
               ' || order_id: ' + str(self.order_id)


class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    def print_table(self, name):
        for i in self.session.query(globals()[name]).all():
            print(i)
        print('\n')

    def delete(self, table_name, value):
        if table_name == 'customer':
            self.session.query(customer).filter_by(customer_id=value).delete()
        elif table_name == 'book':
            self.session.query(book).filter_by(book_id=value).delete()
        elif table_name == 'order':
            self.session.query(order).filter_by(order_id=value).delete()
        elif table_name == 'discount_card':
            self.session.query(discount_card).filter_by(discount_card_id=value).delete()
        elif table_name == 'book_order':
            self.session.query(book_order).filter_by(book_order_id=value).delete()
        self.session.commit()

    def update_customer(self, customer_id, customer_name, customer_surname):
        self.session.query(customer).filter_by(customer_id=customer_id).update({customer.customer_id: customer_id,
                                                                                customer.customer_name: customer_name,
                                                                                customer.customer_surname: customer_surname})
        self.session.commit()

    def update_book(self, book_id, title, author, genre, price):
        self.session.query(book).filter_by(book_id=book_id).update({book.book_id: book_id,
                                                                    book.title: title,
                                                                    book.author: author,
                                                                    book.genre: genre,
                                                                    book.price: price})
        self.session.commit()

    def update_order(self, order_id, date, customer_id, discount_card_id):
        self.session.query(order).filter_by(order_id=order_id).update({order.order_id: order_id,
                                                                       order.date: date,
                                                                       order.customer_id: customer_id,
                                                                       order.discount_card_id: discount_card_id})
        self.session.commit()

    def update_discount_card(self, discount_card_id, date_of_expiring, percentage, customer_id):
        self.session.query(discount_card).filter_by(discount_card_id=discount_card_id).\
            update({discount_card.discount_card_id: discount_card_id,
                    discount_card.date_of_expiring: date_of_expiring,
                    discount_card.percentage: percentage,
                    discount_card.customer_id: customer_id})
        self.session.commit()

    def update_book_order(self, book_order_id, book_id, order_id):
        self.session.query(book_order).filter_by(book_order_id=book_order_id).\
            update({book_order.book_order_id: book_order_id,
                    book_order.book_id: book_id,
                    book_order.order_id: order_id})
        self.session.commit()

    def insert(self, table_name, values):
        new_val = None
        if table_name == 'customer':
            new_val = customer(customer_id=values[0], customer_name=values[1], customer_surname=values[2])
        elif table_name == 'book':
            new_val = book(book_id=values[0], title=values[1], author=values[2], genre=values[3], price=values[4])
        elif table_name == 'order':
            new_val = order(order_id=values[0], date=values[1], customer_id=values[2], discount_card_id=values[3])
        elif table_name == 'discount_card':
            new_val = discount_card(discount_card_id=values[0], date_of_expiring=values[1], percentage=values[2], customer_id=values[3])
        elif table_name == 'book_order':
            new_val = book_order(book_order_id=values[0], book_id=values[1], order_id=values[2])
        if new_val is not None:
            self.session.add(new_val)
            self.session.commit()

    def generate_random(self, table_name, times):
        if table_name == 'customer':
            score = self.session.query(func.max(customer.customer_id).label("max_score")).one().max_score
            while times > 0:
                score += 1
                times = times - 1
                self.insert('customer',
                            [score,
                             ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)),
                             ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))])
        elif table_name == 'book':
            score = self.session.query(func.max(book.book_id).label("max_score")).one().max_score
            while times > 0:
                score += 1
                times = times - 1
                self.insert('book',
                            [score,
                             ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)),
                             ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)),
                             ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)),
                             randrange(99)])
        elif table_name == 'order':
            score = self.session.query(func.max(order.order_id).label("max_score")).one().max_score
            while times > 0:
                score += 1
                times = times - 1
                self.insert('order',
                            [score,
                             datetime.date(randrange(2000, 2022), randrange(1, 12), randrange(1, 30)),
                             randrange(1, self.session.query(
                                 func.max(customer.customer_id).label("max_score")).one().max_score),
                             randrange(1, self.session.query(
                                 func.max(discount_card.discount_card_id).label("max_score")).one().max_score),
                             ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))])
        elif table_name == 'discount_card':
            score = self.session.query(func.max(discount_card.discount_card_id).label("max_score")).one().max_score
            while times > 0:
                score += 1
                times = times - 1
                self.insert('discount_card',
                            [score,
                             datetime.date(randrange(2000, 2022), randrange(1, 12), randrange(1, 30)),
                             randrange(0, 99),
                             randrange(1, self.session.query(
                                 func.max(customer.customer_id).label("max_score")).one().max_score)])
        elif table_name == 'book_order':
            score = self.session.query(func.max(book_order.book_order_id).label("max_score")).one().max_score
            while times > 0:
                score += 1
                times = times - 1
                self.insert('book_order',
                            [score,
                             randrange(1, self.session.query(
                                 func.max(book.book_id).label("max_score")).one().max_score),
                             randrange(1, self.session.query(
                                 func.max(order.order_id).label("max_score")).one().max_score)])
        self.session.commit()

    def search_for_data_two_tables(self):
        return self.session.query(order).join(customer).\
            filter(and_(order.order_id.between(0, 10),
                        customer.customer_id.between(0, 3))).all()

    def search_for_data_three_tables(self):
        return self.session.query(order).join(customer).join(book).\
            filter(and_(order.order_id.between(0, 10),
                        customer.customer_id.between(0, 3),
                        book.book_id.between(3, 5))).all()

    def search_for_data_four_tables(self):
        return self.session.query(order).join(customer).join(book).join(discount_card).\
            filter(and_(order.order_id.between(0, 10),
                        customer.customer_id.between(0, 3),
                        book.book_id.between(1, 5),
                        discount_card.discount_card.id.between(0, 7))).all()
