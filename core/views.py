from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Prefetch
from django.db.models import Q
from .models import Author, Book, Category
from .forms import CreateAuthorForm, UpdateAuthorForm, CreateBookForm, UpdateBookForm
from .utils import avg_price


class AuthorsListView(View):
    def get(self, request):
        authors = Author.objects.prefetch_related(
            Prefetch(   
                        'book_set', 
                        queryset=Book.objects.select_related('category').order_by('title')
                    )).order_by('last_name', 'first_name', 'birth_date')

        authors_data = {}

        for author in authors:
            authors_data[author] = {} 
            authors_data[author]['num_of_books'] = author.book_set.all().count()
            authors_data[author]['books_avg_price'] = avg_price(author.book_set.all())
            authors_data[author]['books'] = author.book_set.all()
            
        return render(request, 'core/authors_list.html', {'authors_data': authors_data})
        

class CreateAuthorView(View):
    def rendered_data(self, form):
        return {
                    'page_title': 'Create Author', 
                    'legend_tag': 'Create Author',
                    'form': form
                }

    def get(self, request):
        return render(request, 'core/author_form.html', self.rendered_data(CreateAuthorForm()))

    def post(self, request):
        form = CreateAuthorForm(request.POST)

        if form.is_valid():
            author = form.save()
            messages.success(request, f'A new author with fullname "{author.last_name} {author.first_name}" was created!')
            return redirect('authors-list')

        else: 
            messages.error(request,'Something went wrong, please try agaain.')
            return render(request, 'core/author_form.html', self.rendered_data(form))


class UpdateAuthorView(View):
    def choose_author(self, author_id):
        return Author.objects.prefetch_related(
                                                Prefetch(   
                                                            'book_set',
                                                            queryset = Book.objects.select_related('category').order_by('title')
                                                )).get(id=author_id) 
        
    def rendered_data(self, form, author):
        return {
                    'page_title': 'Update Author', 
                    'legend_tag': 'Update Author',
                    'form': form,
                    'author_id': author.id,
                    'delete_modal_title': 'Delete Author',
                    'delete_modal_message': f'Are you sure you want to delete {author} and his/her books?',
                    'num_of_books': author.book_set.all().count(),
                    'books_avg_price': avg_price(author.book_set.all()),
                    'author_books': author.book_set.all()
                }

    def get(self, request, author_id): 
        try:
            author = self.choose_author(author_id)
            
        except Author.DoesNotExist:
            messages.error(request, f'There is no any author with id: {author_id}.')
            return redirect('authors-list')

        else:
            particular_author_data = {
                                        'first_name': author.first_name, 
                                        'last_name': author.last_name, 
                                        'birth_date': author.birth_date, 
                                        'description': author.description
                                                                            }
            
            initial_form = UpdateAuthorForm(initial=particular_author_data)
            return render(request, 'core/author_form.html', self.rendered_data(initial_form, author))
            
    def post(self, request, author_id):
        author = self.choose_author(author_id)
        form = UpdateAuthorForm(request.POST, instance=author)
        
        if form.is_valid():
            form.save()
            if form.has_changed():
                messages.success(request, f'{author.last_name} {author.first_name} was updated succesfully!')

            else:
                messages.warning(request, f'{author.last_name} {author.first_name} was not updated.')
            
            return redirect('authors-list')

        else:
            messages.error(request, 'Somethong went wrong, please try again.') 
            return render(request, 'core/author_form.html', self.rendered_data(form, author))


class DeleteAuthorView(View):
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            
        except Author.DoesNotExist:
            messages.error(request, f'There is no any author with id: {author_id}.')
            return redirect('authors-list')

        else:
            messages.success(request, f'Author with fullname {author.last_name} {author.first_name} was deleted.')
            author.delete()
            return redirect('authors-list')

class CreateBookView(View):
    def rendered_data(self, form):
        return {
                    'page_title': 'Create Book', 
                    'legend_tag': 'Create Book',
                    'form': form
                }
    
    def get(self, request):
        return render(request, 'core/book_form.html', self.rendered_data(CreateBookForm()))

    def post(self, request):
        form = CreateBookForm(request.POST)

        if form.is_valid():
            book = form.save()
            messages.success(request, f'A new book with title "{book.title}" was created!')
            return redirect('authors-list')

        else:
            messages.error(request, 'Somethong went wrong, please try again.')
            return render(request , 'core/book_form.html', self.rendered_data(form))


class UpdateBookView(View):
    def rendered_data(self, form, book):
        return  {
                    'page_title': 'Update Book', 
                    'legend_tag': 'Update Book',
                    'form': form,
                    'book': book,
                    'delete_modal_title': 'Delete Book',
                    'delete_modal_message': f'Are you sure you want to delete "{book}"?'
                }

    def get(self, request, book_id):
        try:
            book = Book.objects.select_related('author', 'category').get(id=book_id)

        except Book.DoesNotExist:
            messages.error(request, f'There is no any book with id: {book_id}.')
            return redirect('authors-list')

        else:
            particular_book_data = {
                                        'author': book.author,
                                        'title': book,
                                        'pub_date': book.pub_date,
                                        'price': book.price,
                                        'is_published': book.is_published,
                                        'category': book.category,
                                        'description': book.description
                                                                        }
                
            initial_form = UpdateBookForm(initial=particular_book_data)
            return render(request, 'core/book_form.html', self.rendered_data(initial_form, book))
          
    def post(self, request, book_id):
        book = Book.objects.select_related('author', 'category').get(id=book_id)
        form = UpdateBookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            
            if form.has_changed():
                messages.success(request, f'"{book.title}" was updated succesfully!')

            else:
                messages.warning(request, f'"{book.title}" was not updated.')
            return redirect('authors-list')

        else:
            messages.error(request, f'Something went wrong, please try again.')
            return render(request, 'core/book_form.html', self.rendered_data(form, book))


class DeleteBookView(View):
    def get(self, request, book_id):
        try: 
            book = Book.objects.get(id=book_id)

        except Book.DoesNotExist:
            messages.error(request, f'There is no any book with id: {book_id}.')
            return redirect('authors-list')

        else:
            messages.success(request, f'Book with title {book.title} was deleted.')
            book.delete()
            return redirect('authors-list')


class SearchResultsView(View):
    def get(self, request):        
        phrase = request.GET.get('search')
        phrase_split = phrase.split()
        search_choice = request.GET.get('search_choice')
        data = {}

        if search_choice == 'author':
            if phrase_split == [] or len(phrase_split) > 2: 
                data['message'] = 'Please type one or two words to search for authors.'
                authors_set = ''

            # Search with one word for author
            elif len(phrase_split) == 1: 
                authors_set = Author.objects.prefetch_related('book_set').filter(Q(last_name__icontains=phrase) | Q(first_name__icontains=phrase))
                authors_set = authors_set.order_by('last_name', 'first_name', 'birth_date') 
                 
            else:
                # Search with two words for a 'particular' author  
                situation_1 = Q(last_name__icontains=phrase_split[0]) & Q(first_name__icontains=phrase_split[1])
                situation_2 = Q(last_name__icontains=phrase_split[1]) & Q(first_name__icontains=phrase_split[0])
                authors_set = Author.objects.prefetch_related('book_set').filter(Q(situation_1) | Q(situation_2))
                
                # Search with first and second word for authors
                if not authors_set:
                    situation_1 = Q(last_name__icontains=phrase_split[0]) | Q(first_name__icontains=phrase_split[0])
                    situation_2 = Q(last_name__icontains=phrase_split[1]) | Q(first_name__icontains=phrase_split[1])
                    authors_set = Author.objects.prefetch_related('book_set').filter(Q(situation_1) | Q(situation_2))
                    authors_set = authors_set.order_by('last_name', 'first_name', 'birth_date')

            if authors_set:
                data['authors_set'] = {}

                for author in authors_set:
                    data['authors_set'][author] = {}
                    data['authors_set'][author]['num_of_books'] = author.book_set.all().count()
                    data['authors_set'][author]['books_avg_price'] = avg_price(author.book_set.all())    
            
            data['message'] = f'Results for authors after your phrase: "{phrase}"'
                
        elif len(phrase) > 0:
            books_set = Book.objects.select_related('author', 'category').filter(title__icontains=phrase).order_by('title')
        
            if books_set:
                data['books_set'] = books_set
           
            data['message'] = f'Results for books after your phrase: "{phrase}"'

        else: 
            data['message'] = 'Please type at least one word to search for books.'
            
        return render(request, 'core/search_results.html', data)
