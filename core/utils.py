def avg_price(books):
    if books.count() == 0:
        return 0

    else:
        sum = 0
        for book in books:
            sum = sum + book.price

        return round(sum/books.count(), 2)