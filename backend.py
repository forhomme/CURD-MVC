import mvc_exception as mvc_exc
import time
import shelve
import datetime

books = list()


def create_books(app_books):
	global books
	books = app_books
	
def create_book(title, author, date_published, number_of_pages, type_book):
	global books
	result = list(filter(lambda x: x['title'] == title, books))
	if result:
		raise mvc_exc.BookAlreadyStored('"{}" already stored'.format(title))
	else:
		books.append({'title': title, 'author': author, 'date published': date_published, 'number of pages': number_of_pages, 'type book': type_book})

def search_book(title):
	global books
	my_book = list(filter(lambda x : x['title'] == title, books))
	if my_book:
		return my_book[0]
	else:
		raise mvc_exc.BookNotStored('Cannot read "{}" because book not stored'.format(title))
	
def report_book():
	global books
	return [book for book in books]
	
def update(title, author, date_published, number_of_pages, type_book):
	global books
	idxs_book = list(filter(lambda i_x: i_x[1]['title'] == title, enumerate(books)))
	if idxs_book:
		i, book_to_update = idxs_book[0][0], idxs_book[0][1]
		books[i] = {'title' : title, 'author' : author, 'date published' : date_published, 'number of pages' : number_of_pages, 'type book' : type_book}
	else:
		raise mvc_exc.BookNotStored('Cannot update "{}" because book not stored'.format(title))
		
def delete(title):
	global books
	idxs_book = list(filter(lambda i_x: i_x[1]['title'] == title, enumerate(books)))
	if idxs_book:
		i, book_to_update = idxs_book[0][0], idxs_book[0][1]
		del item[i]
	else:
		raise mvc_exc.BookNotStored('Cannot delete "{}" because book not stored'.format(title))
		
def main():
	
	#Create
	title = ''
	author = ''
	valid_date = True
	number_of_pages = ''
	type_book = ''
	while len(title) < 1:
		title = input("Enter Book Title : ")
	while len(author) < 1:
		author = input("Enter Book Author : ")
	while valid_date:
		date_published = input("Enter Book date published (DD/MM/YYYY): ")
		day,month,year = date_published.split('/')
		valid = True
		try:
			datetime.datetime.strptime(date_published, '%d/%m/%Y')
		except ValueError:
			valid = False
		if valid == True :
			valid_date = False
		else:
			valid_date = True
	while len(number_of_pages) < 1 :
		number_of_pages = input("Enter Book number of pages : ")
		if number_of_pages.isdigit():
			break
		else:
			number_of_pages = ''
	while type_book != "Novel" and type_book != "Documentary" and type_book != "Others":
		type_book = input("Enter type of Book: Novel, Documentary, or Others : ")
	create_book(title, author, date_published, number_of_pages, type_book)
	
	
	#Report
	print('Report book')
	print(report_book())
	
	
	#Update
	print('Update book')
	
	
	#Delete
	print('Delete book')
	
	print(report_book())
	
if __name__ == '__main__':
	main()