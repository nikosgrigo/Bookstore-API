from flask import Flask,request,Response
import csv,json,datetime
import pandas as pd

app = Flask(__name__)

def read_file(path):
    with open(path, mode = 'r')as file:
        data = csv.DictReader(file)
        # for lines in data:
        #     print(lines)
        return list(data)
    

def write_file(path,row):
   with open(path, mode = 'a', newline='') as f:
      writer = csv.writer(f, delimiter=',')
      writer.writerow(row)


all_books_info = read_file('./data/Books.csv')
all_rating_info = read_file('./data/Ratings.csv')
all_rented_books = read_file('./data/RentedBooks.csv')

# print(all_rating_info)

def get_book_from_list_by_identifier(identifier:str,list,value):
   result = []

   if identifier == 'ISBN':
      for book in list:
         if book.get(identifier) == value:
            result.append(book)
            break

   for book in list:
         if book.get(identifier) == value:
            result.append(book)
   return result


def days_between(d1, d2):
   dt0 = pd.to_datetime(d1, format = '%Y-%m-%d')
   dt1 = pd.to_datetime(d2, format = '%Y-%m-%d')
   return (dt1 - dt0).days


def calculate_rental_fee(start,end):

   days = days_between(start,end)
   print(days)
   
   if days <= 3:
      return days*1
   else:
      return 3*1 + (days-3)*0.5


def send_response(response_data,status:str,status_code:int):
   if status == 'success' and not type(response_data) == str:
      return Response(json.dumps({"data":response_data,"status":status,"status code":status_code}), content_type='application/json', status=status_code)
   else:
      return Response(json.dumps({"message":response_data,"status":status,"status code":status_code}), content_type='application/json', status=status_code)


#-------------BUG--------------
def get_all_books_from_list():
   
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

def is_book_rented(list):
   filename = './data/RentedBooks.csv'
   flag = False

   with open(filename, 'r') as csvfile:
      datareader = csv.reader(csvfile)
      next(datareader, None)     #skip first line - columns
      for row in datareader:
         if list[0] == row[0]:      #check if book is already inside the rented Books and flag column is True
            flag = True
            break
   return flag

def rent_book(data):

   #Create new timestamp
   date = datetime.datetime.now()
   # Format as "YYYY-MM-DD"
   formatted_date = date.strftime('%Y-%m-%d')

   # flag = True
   # data.append(flag)

   #Add new column-field for date
   data.append(formatted_date)

   #Add new row to file or DB
   write_file("./data/RentedBooks.csv",data)

def calculate_total_rental_fee(rented_book_list):
   return sum(calculate_rental_fee(int(rental['Days'])) for rental in rented_book_list)

def get_book_list_by_range(data,start,end):
   list = []
   for book in data:
      if book.get('Date') >=start and book.get('Date') <=end:
         list.append(book)
   return list


books = get_all_books_from_list()

# Retrieve a list of all available books
@app.route('/books',methods = ['GET'])
def get_all_books():
   return send_response(books,"success",200)


# Retrieve a list of available books based on a specified category.
@app.route('/books/author/<author>',methods = ['GET'])
def get_all_books_by_author(author):
   data = get_book_from_list_by_identifier('Book-Author',books,author)
   if data:
      return send_response(data,"success",200)
   return send_response("Books not found","error",404)
   
               
# Retrieve detailed information about a specific book.
@app.route('/book/<id>',methods = ['GET'])
def get_all_books_by_id(id):
   data = get_book_from_list_by_identifier('ISBN',books,id)
   if data:
      return send_response(data,"success",200)         
   return send_response("Books not found","error",404)


# Retrieve a list of available books that was released by a specific publisher
@app.route('/books/publisher/<publisher>',methods = ['GET'])
def get_all_books_by_publisher(publisher):
   data = get_book_from_list_by_identifier('Publisher',books,publisher)
   if data:
      return send_response(data,"success",200)
   return send_response("Books not found","error",404)


#Retrieve a list of available books that was released on a specific year or between certain dates (e.g., from 2000 to 2005)
@app.route('/books/date/<date>',methods = ['GET'])
def get_all_books_by_date(date):
   date = str(date)
   data = get_book_from_list_by_identifier('Year-Of-Publication',books,date)
   if data:
      return send_response(data,"success",200)
   return send_response("Books not found","error",404)



#Rent a book, making it unavailable for others to rent.
@app.route('/rent/<id>',methods = ['POST'])
def set_book_as_rented(id):
   #1.find book
         result = {}
         for book in books:
            if book.get("ISBN") == id:
               #2.retrieve book from the general book list
               result = book
               break
         #create a list only with values 
         data = []
         for value in result.values():
            data.append(value)
         if data:   
            #check if book is already rented
            if is_book_rented(data):
               return send_response("Book not available for rent","error",400)
            else:
               #3.add book on another file or table

               rent_book(data)
               return send_response("Book rented successfully","success",200)
   

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
         rented_date = data[-1]              #get rented date 
         date = datetime.datetime.now()      #return book now so create a new date
         end_date = date.strftime('%Y-%m-%d')

        #2.Calculate rental fee based on rented days
         rental_fee = calculate_rental_fee(rented_date,end_date)

         #Change flag=False to make book avaliable for others

         #3.Return response with the rental fee
         return Response(json.dumps({"status":"success","status code":200,"message": "Book returned successfully", "rental_fee": rental_fee}), content_type='application/json', status=200)
      return Response(json.dumps({"status":"error","status code":400,"message": "Book not found or not currently rented"}), content_type='application/json', status=400)


# Retrieve a list of books that were rented within a specified date range.
@app.route('/rentals',methods = ['GET'])
def get_all_rented_books_for_period():
      start_date = request.args.get('start') #(i.e. ?start=YYYY-MM-DD)
      end_date = request.args.get('end')     #(i.e. &end=YYYY-MM-DD)
      if start_date is None and end_date is None:     #(+check if start date is smaller than end date)
         print("Argument not provided")
         return send_response("Arguments not found","error",404)
      else:
         data = get_book_list_by_range(all_rented_books,start_date,end_date)
         return send_response(data,"success",200) 


#Calculate and retrieve the total revenue generated by book rentals within a specified date range.
@app.route('/revenue',methods = ['GET'])
def get_total_revenue():
      start_date = request.args.get('start') #(i.e. ?start=YYYY-MM-DD)
      end_date = request.args.get('end')     #(i.e. &end=YYYY-MM-DD)
      if start_date is None and end_date is None:     #(+check if start date is smaller than end date)
         print("Argument not provided")
         return send_response("Arguments not found","error",404)
      else:
         books_rented_within_range = get_book_list_by_range(all_rented_books,start_date,end_date)
         # print(books_rented_within_range)
         data = calculate_total_rental_fee(books_rented_within_range)
         return send_response(data,"success",200) 
      

if __name__ == '__main__':
   #Read all nessecary files and keep into a dictionary (better than list)

   app.run(debug=True)

