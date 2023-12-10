import pandas as pd

def read_data(rows):

    books_file_path = "./data/Books.csv"
    ratings_file_path = "./data/Ratings.csv"

    # Read RATING and BOOK CSV files into a DataFrames
    df = pd.read_csv(ratings_file_path)
    books_df = pd.read_csv(books_file_path)

   # Filter rows with non-zero ratings and select the first 20 rows
    result_subset = df[df['Book-Rating'] > 0].head(rows)

    # Filter rows from 'Books.csv' where 'ISBN' matches those in the result_subset
    matching_books = books_df[books_df['ISBN'].isin(result_subset['ISBN'])]

    matching_books['Available'] = True

    # print(f"Data retrieved: {matching_books}")
    # print(f"Length: {len(matching_books)}")

    # Display the resulting DataFrame
    return matching_books

    # Display the resulting DataFrame
    # return result_subset
        