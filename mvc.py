import backend
import mvc_exception as mvc_exc
import time
import shelve
import datetime

class Model(object):
	def __init__(self, application_book):
		self._book_type= 'product'
		self.create_books(application_book)
		
	@property
	def book_type(self):
		return self._book_type
		
	@book_type.setter
	def book_type(self, new_book_type):
		self._book_type = new_book_type
	
	def create_book(self, title, author, date_published, number_of_pages, type_book):
		backend.create_book(title, author, date_published, number_of_pages, type_book)
		
	def create_books(self, books):
		backend.create_books(books)
		
	def report_book(self):
		return backend.report_book(title)
		
	def search_book(self, title):
		return backend.search_book()
		
	def update_book(self, title, author, date_published, number_of_pages, type_book):
		backend.update(title, author, date_published, number_of_pages, type_book)
		
	def delete_book(self, title):
		backend.delete(title)
		
class View(object):

    @staticmethod
    def show_bullet_point_list(book_type, books):
        print('--- {} LIST ---'.format(book_type.upper()))
        for book in books:
            print('* {}'.format(book))

    @staticmethod
    def show_number_point_list(book_type, books):
        print('--- {} LIST ---'.format(book_type.upper()))
        for i, book in enumerate(books):
            print('{}. {}'.format(i+1, book))

    @staticmethod
    def show_book(book_type, book, book_info):
        print('//////////////////////////////////////////////////////////////')
        print('Good news, we have some {}!'.format(book.upper()))
        print('{} INFO: {}'.format(book_type.upper(), book_info))
        print('//////////////////////////////////////////////////////////////')

    @staticmethod
    def display_missing_book_error(book, err):
        print('**************************************************************')
        print('We are sorry, we have no {}!'.format(book.upper()))
        print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_book_already_stored_error(book, book_type, err):
        print('**************************************************************')
        print('Hey! We already have {} in our {} list!'
              .format(book.upper(), book_type))
        print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_book_not_yet_stored_error(book, book_type, err):
        print('**************************************************************')
        print('We don\'t have any {} in our {} list. Please insert it first!'
              .format(book.upper(), book_type))
        print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_book_stored(book, book_type):
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('Hooray! We have just added some {} to our {} list!'
              .format(book.upper(), book_type))
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    @staticmethod
    def display_change_book_type(older, newer):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('Change book type from "{}" to "{}"'.format(older, newer))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    @staticmethod
    def display_book_updated(book, o_price, o_quantity, n_price, n_quantity):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('Change {} price: {} --> {}'
              .format(book, o_price, n_price))
        print('Change {} quantity: {} --> {}'
              .format(book, o_quantity, n_quantity))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    @staticmethod
    def display_book_deletion(title):
        print('--------------------------------------------------------------')
        print('We have just removed {} from our list'.format(title))
        print('--------------------------------------------------------------')
		
class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_books(self, bullet_points=False):
        books = self.model.report_books()
        book_type = self.model.book_type
        if bullet_points:
            self.view.show_bullet_point_list(book_type, books)
        else:
            self.view.show_number_point_list(book_type, books)

    def show_book(self, book_title):
        try:
            book = self.model.search_book(book_title)
            book_type = self.model.book_type
            self.view.show_book(book_type, book_name, book)
        except mvc_exc.bookNotStored as e:
            self.view.display_missing_book_error(book_name, e)

    def insert_book(self, title, author, date_published, number_of_pages, type_book):
        assert price > 0, 'price must be greater than 0'
        assert quantity >= 0, 'quantity must be greater than or equal to 0'
        book_type = self.model.book_type
        try:
            self.model.create_book(title, author, date_published, number_of_pages, type_book)
            self.view.display_book_stored(title, book_type)
        except mvc_exc.bookAlreadyStored as e:
            self.view.display_book_already_stored_error(title, book_type, e)

    def update_book(self, title, author, date_published, number_of_pages, type_book):
        assert price > 0, 'price must be greater than 0'
        assert quantity >= 0, 'quantity must be greater than or equal to 0'
        book_type = self.model.book_type

        try:
            older = self.model.search_book(title)
            self.model.update_book(title, price, quantity)
            self.view.display_book_updated(title, older['price'], older['quantity'], price, quantity)
        except mvc_exc.bookNotStored as e:
            self.view.display_book_not_yet_stored_error(title, book_type, e)
            # if the book is not yet stored and we performed an update, we have
            # 2 options: do nothing or call insert_book to add it.
            # self.insert_book(title, price, quantity)

    def update_book_type(self, new_book_type):
        old_book_type = self.model.book_type
        self.model.book_type = new_book_type
        self.view.display_change_book_type(old_book_type, new_book_type)

    def delete_book(self, title):
        book_type = self.model.book_type
        try:
            self.model.delete_book(title)
            self.view.display_book_deletion(title)
        except mvc_exc.bookNotStored as e:
            self.view.display_book_not_yet_stored_error(title, book_type, e)
