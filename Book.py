
import File as f
import datetime
import csv

class Book():

    #-------------BUG--------------
    def get_all_books_from_list():

        all_books_info = f.read_file('./data/Books.csv','r')
        all_rating_info = f.read_file('./data/Ratings.csv','r')
   
        LIMIT = 10
        # Set length max to 500
        isbn_with_non_zero_rating = []
        for index,row in enumerate(all_rating_info):
            if row['Book-Rating'] !=0:
                isbn_with_non_zero_rating.append(row['ISBN'])
            if index == LIMIT-1: #If you reach 500 books from DB stop
                break
        # print(isbn_with_non_zero_rating)

        all_books = []
        for el in isbn_with_non_zero_rating:
            for book in all_books_info:
                if el == book['ISBN']:
                    all_books.append(book)

        # print(all_books)
        return all_books
    
    def get_book_from_list_by_identifier(identifier:str,list,value):
        result = []
        for book in list:
            if book.get(identifier) == value:
                result.append(book)
                if identifier == 'ISBN':
                    break
        return result
                
    def get_book_list_by_range(data,start,end):
        list = []
        for book in data:
            if book.get('Date') >=start and book.get('Date') <=end:
                list.append(book)
        return list

    def is_book_rented(list):
        filename = './data/RentedBooks.csv'
        flag = False

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            next(datareader, None)     #skip first line - columns
            for row in datareader:
                if list[0] == row[0]:      #check if book is already inside the rented Books
                    flag = True
                    break
        return flag
    
    def rent_book(data,days):
        #Add new column-field for days
        data.append(days)

        #Create new timestamp
        date = datetime.datetime.now()
        # Format as "YYYY-MM-DD"
        formatted_date = date.strftime('%Y-%m-%d')

        #Add new column-field for date
        data.append(formatted_date)

        #Add new row to file or DB
        f.write_file("./data/RentedBooks.csv",data)


    def calculate_rental_fee(days:str):
        days = int(days)
        if days <= 3:
            return days*1
        else:
            return 3*1 + (days-3)*0.5