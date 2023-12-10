
import datetime
import random as r
import pandas as pd

def get_book_from_list_by_identifier(identifier:str,list,value):
   result = []

   if identifier == 'ISBN':
      for book in list:
         if book.get(identifier) == int(value):
           return book

   for book in list:
         if book.get(identifier) == value:
            result.append(book)
   return result

def rent_book(bookDict,dt_all_books,dt_rented_books):

   #Create new timestamp
   date = datetime.datetime.now()

   # Format as "YYYY-MM-DD"
   formatted_date = date.strftime('%Y-%m-%d')
   # bookDict.update(Date = formatted_date)

   #Create tag for rented state NOT FREE
   bookDict.update(Available = False)

#    print(bookDict)

   #Update Availability on Book.csv
   dt_all_books.loc[dt_all_books.ISBN == bookDict.get('ISBN'),'Available'] = False

   #Add new row data on RentedBooks.csv
   new_data = [r.randint(1, 1000),bookDict.get('ISBN'),formatted_date,0]

   if not any(dt_rented_books.ISBN == bookDict.get('ISBN')):
      dt_rented_books.loc[len(dt_rented_books)] = new_data
   # else:
   #    #update the row because data already exists for this book
   #    dt_rented_books.loc[dt_rented_books.ISBN == bookDict.get('ISBN'),'Available'] = False

   # Write the DataFrame to a CSV file
   dt_rented_books.to_csv('./data/RentedBooks.csv', index=False)

   print(dt_rented_books)

def return_book(book,all_books_df,all_rented_df):
   rented_date = book.get('Date')              #get rented date 

   date = datetime.datetime.now()      
   end_date = date.strftime('%Y-%m-%d')

   #2.Calculate rental fee based on rented days
   rental_fee = calculate_rental_fee(rented_date,end_date)


   #Store fee for later use
   old_rental_fee = book.get('RentalFee')
   old_rental_fee += rental_fee
   all_rented_df.loc[all_rented_df.ISBN == book.get('ISBN'),'RentalFee'] = old_rental_fee

   #Update Availability to True on Book.csv
   all_books_df.loc[all_books_df.ISBN == book.get('ISBN'),'Available'] = True

   # Write the DataFrame to a CSV file
   all_rented_df.to_csv('./data/RentedBooks.csv', index=False)
   all_books_df.to_csv('./data/Books.csv', index=False)

   return rental_fee


def days_between(d1, d2):
   dt0 = pd.to_datetime(d1, format = '%Y-%m-%d')
   dt1 = pd.to_datetime(d2, format = '%Y-%m-%d')
   return (dt1 - dt0).days

def calculate_rental_fee(start,end):
   
   print(start,end)

   days = days_between(start,end)
   print(days)

   if days <= 3:
      return days*1
   else:
      return 3*1 + (days-3)*0.5

def calculate_total_rental_fee(rented_book_list):
   return rented_book_list['RentalFee'].sum()

def is_available_for_rent(id,all_books):
   for book in all_books:
      if book.get('ISBN') == id and book.get('Available') == True:
         return book
   return False

def get_book_list_by_range(data,start,end):
   list = []
   for book in data:
      if book.get('Date') >=start and book.get('Date') <=end:
         list.append(book)
   return list