book = Book(title="1984", author="George Orwell", publication_year=1949) # outpus : <bound method Model.save of <Book: 1984>>

Book.objects.all() # Output: <QuerySet []>

book.title = "Nineteen Eighty-Four' # Output: nothing

book.delete() # (1, {'bookshelf.Book': 1})