from flask import Flask,request,Response
import csv
import json
import datetime
import time

app = Flask(__name__)

# def read_file(path,mode ='r'):
#     with open(path, mode = mode)as file:
#         data = csv.DictReader(file)
#         # for lines in data:
#         #     print(lines)
#         return list(data)
    
# def write_file(path,row,mode = 'a'):
#    with open(path, mode, newline='') as f:
#       writer = csv.writer(f, delimiter=',')
#       writer.writerow(row)

# all_books_info = read_file('./data/Books.csv','r')
# all_rating_info = read_file('./data/Ratings.csv','r')
# print(all_rating_info)

# def get_book_from_list_by_identifier(identifier:str,list,value):
#    result = []
#    for book in list:
#          if book.get(identifier) == value:
#             result.append(book)
#             if identifier == 'ISBN':
#                break
#    return result


# def calculate_rental_fee(days:str):
#    days = int(days)
#    if days <= 3:
#       return days*1
#    else:
#       return 3*1 + (days-3)*0.5


# #-------------BUG--------------
# def get_all_books_from_list():
   
#       LIMIT = 10
#       # Set length max to 500
#       isbn_with_non_zero_rating = []
#       for index,row in enumerate(all_rating_info):
#          if row['Book-Rating'] !=0:
#             isbn_with_non_zero_rating.append(row['ISBN'])
#          if index == LIMIT-1: #If you reach 500 books from DB stop
#             break
#       # print(isbn_with_non_zero_rating)

#       all_books = []
#       for el in isbn_with_non_zero_rating:
#          for book in all_books_info:
#             if el == book['ISBN']:
#                all_books.append(book)

#       # print(all_books)
#       return all_books

# Retrieve a list of all available books
@app.route('/books',methods = ['GET'])
def get_all_books():
   if request.method == 'GET':
     data = get_all_books_from_list()
     return Response(json.dumps({"data":data,"status":"success","status code":200}), content_type='application/json', status=200)

# Retrieve a list of available books based on a specified category.
@app.route('/books/author/<author>',methods = ['GET'])
def get_all_books_by_author(author):
   if request.method == 'GET':
      books = get_all_books_from_list()
      data = get_book_from_list_by_identifier('Book-Author',books,author)
      if data:
         return Response(json.dumps({"data":data,"status":"success","status code":200}), content_type='application/json', status=200)
      return Response(json.dumps({"message":'Book not found',"status":"fail","status code":404}), content_type='application/json', status=404)
               
   
# Retrieve detailed information about a specific book.
@app.route('/book/<id>',methods = ['GET'])
def get_all_books_by_id(id):
   if request.method == 'GET':
         books = get_all_books_from_list()
         data = get_book_from_list_by_identifier('ISBN',books,id)
         if data:
            return Response(json.dumps({"data":data,"status":"success","status code":200}), content_type='application/json', status=200)
         return Response(json.dumps({"message":'Book not found',"status":"fail","status code":404}), content_type='application/json', status=404)
               
# Retrieve a list of available books that was released by a specific publisher
@app.route('/books/publisher/<publisher>',methods = ['GET'])
def get_all_books_by_publisher(publisher):
   if request.method == 'GET':
         books = get_all_books_from_list()
         data = get_book_from_list_by_identifier('Publisher',books,publisher)
         if data:
            return Response(json.dumps({"data":data,"status":"success","status code":200}), content_type='application/json', status=200)
         return Response(json.dumps({"message":'Book not found',"status":"fail","status code":404}), content_type='application/json', status=404)

#Retrieve a list of available books that was released on a specific year or between certain dates (e.g., from 2000 to 2005)
@app.route('/books/date/<date>',methods = ['GET'])
def get_all_books_by_date(date):
    if request.method == 'GET':
         date = str(date)
         books = get_all_books_from_list()
         data = get_book_from_list_by_identifier('Year-Of-Publication',books,date)
         if data:
            return Response(json.dumps({"data":data,"status":"success","status code":200}), content_type='application/json', status=200)
         return Response(json.dumps({"message":'Book not found',"status":"fail","status code":404}), content_type='application/json', status=404)

# def is_book_rented(list):
#    filename = './data/RentedBooks.csv'
#    flag = False

#    with open(filename, 'r') as csvfile:
#       datareader = csv.reader(csvfile)
#       next(datareader, None)     #skip first line - columns
#       for row in datareader:
#          if list[0] == row[0]:      #check if book is already inside the rented Books
#             flag = True
#             break
#    return flag

# def rent_book(data,days):
#    #Add new column-field for days
#    data.append(days)

#    #Create new timestamp
#    date = datetime.datetime.now()
#    # Format as "YYYY-MM-DD"
#    formatted_date = date.strftime('%Y-%m-%d')

#    #Add new column-field for date
#    data.append(formatted_date)

#    #Add new row to file or DB
#    write_file("./data/RentedBooks.csv",data)

#Rent a book, making it unavailable for others to rent.
@app.route('/rent/<id>/<days>',methods = ['POST'])
def set_book_as_rented(id,days):
   #1.find book
   if request.method == 'POST':
         result = {}
         books = get_all_books_from_list()
         for book in books:
            if book.get("ISBN") == id:
               #2.retrieve book from the general book list
               result = book
               break
         #create a list only with values 
         data = []
         for value in result.values():
            data.append(value)
         if data:    # check if data != None
            # print(data)
            #check if book is already rented
            if is_book_rented(data):
               return Response(json.dumps({"message":'Book not available for rent',"status":"fail","status code":400}), content_type='application/json', status=400)
            else:
               #3.add book on another file or table
               # days = 3
               rent_book(data,days)
               return Response(json.dumps({"message": "Book rented successfully","status":"success","status code":200}), content_type='application/json', status=200)
   
# Return a rented book and calculate the rental fee based on the number of days rented.
@app.route('/return/<id>',methods = ['PUT'])
def get_rented_book(id):

   if request.method == 'PUT':
      #1.Find a rented book and return it on the client
      filename = './data/RentedBooks.csv'
      data = ""

      with open(filename, 'r') as csvfile:
         datareader = csv.reader(csvfile)
         next(datareader, None)     #skip first line - columns
         for row in datareader:
            if row[0] == id:      
               data = row
               break
      if(data):
      #2.Calculate rental fee based on rented days
         rented_days = data[-2]
         rental_fee = calculate_rental_fee(rented_days)
         #3.Return response with the rental fee
         return Response(json.dumps({"status":"success","status code":200,"message": "Book returned successfully", "rental_fee": rental_fee}), content_type='application/json', status=200)
      return Response(json.dumps({"status":"error","status code":400,"message": "Book not found or not currently rented"}), content_type='application/json', status=400)

# def get_book_list_by_range(data,start,end):
#    list = []
#    for book in data:
#       if book.get('Date') >=start and book.get('Date') <=end:
#          list.append(book)
#    return list

# Retrieve a list of books that were rented within a specified date range.
@app.route('/rentals',methods = ['GET'])
def get_all_rented_books_for_period():

   if request.method == 'GET':
      start_date = request.args.get('start') #(i.e. ?start=YYYY-MM-DD)
      end_date = request.args.get('end')     #(i.e. &end=YYYY-MM-DD)
      if start_date is None and end_date is None:     #(+check if start date is smaller than end date)
         print("Argument not provided")
         return Response(json.dumps({"message":'Arguments not found',"status":"fail","status code":404}), content_type='application/json', status=404)
      else:
         all_rented_books = read_file('./data/RentedBooks.csv','r')
         data = get_book_list_by_range(all_rented_books,start_date,end_date)
         return Response(json.dumps({"status":"success","status code":200,"data":data}), content_type='application/json', status=200)

if __name__ == '__main__':
   app.run()
