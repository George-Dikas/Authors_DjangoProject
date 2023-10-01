from django.urls import path
from . import views

urlpatterns = [
    path("authors_list/", views.AuthorsListView.as_view(), name='authors-list'),
    path("create_author/", views.CreateAuthorView.as_view(), name='create-author'),
    path("update_author/<int:author_id>", views.UpdateAuthorView.as_view(), name='update-author'),
    path("delete_author/<int:author_id>", views.DeleteAuthorView.as_view(), name='delete-author'),
    path("create_book/", views.CreateBookView.as_view(), name='create-book'),
    path("update_book/<int:book_id>", views.UpdateBookView.as_view(), name='update-book'),
    path("delete_book/<int:book_id>", views.DeleteBookView.as_view(), name='delete-book'),
    path("search_results/", views.SearchResultsView.as_view(), name='search-results')
]
