from django import forms
from django.forms.widgets import NumberInput
from datetime import date
from .models import Author, Book, Category

class CreateAuthorForm(forms.ModelForm):
    birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Author
        exclude = ['created_at', 'updated_at']

    def clean_last_name(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if Author.objects.filter(first_name=first_name, last_name=last_name):
            raise forms.ValidationError(f'There is already an author called {last_name} {first_name}.')
        
        return last_name

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if birth_date >= date(2007, 1, 1):
            raise forms.ValidationError('You are too young to be an author.')
        
        return birth_date

class UpdateAuthorForm(forms.ModelForm):
    birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Author
        exclude = ['created_at', 'updated_at']

    def clean_last_name(self):
        typed_firstname = self.cleaned_data.get('first_name')
        typed_lastname = self.cleaned_data.get('last_name')
        initial_firstname = self.initial.get('first_name')
        initial_lastname = self.initial.get('last_name')

        if Author.objects.filter(first_name=typed_firstname, last_name=typed_lastname).exclude(first_name=initial_firstname, last_name=initial_lastname):
            raise forms.ValidationError(f'There is already an author called {typed_lastname} {typed_firstname}.')
        
        return typed_lastname

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if birth_date >= date(2007, 1, 1):
            raise forms.ValidationError('You are too young to be an author.')
        
        return birth_date

class CreateBookForm(forms.ModelForm):
    pub_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Book
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.order_by('last_name', 'first_name')
        self.fields['category'].queryset = Category.objects.order_by('name')

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if Book.objects.filter(title=title):
            raise forms.ValidationError(f'There is already a book with title "{title}".')
        
        return title

    def clean_pub_date(self):
        pub_date = self.cleaned_data.get('pub_date')

        if pub_date > date.today():
            raise forms.ValidationError("Date can't be greater than current date.")

        return pub_date

class UpdateBookForm(forms.ModelForm):
    pub_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Book
        exclude = ['createrd_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.order_by('last_name', 'first_name')
        self.fields['category'].queryset = Category.objects.order_by('name')

    def clean_title(self):
        typed_title = self.cleaned_data.get('title')
        initial_title = self.initial.get('title')

        if Book.objects.filter(title=typed_title).exclude(title=initial_title):
            raise forms.ValidationError(f'There is already a book with title "{typed_title}".')

        return typed_title
        
    def clean_pub_date(self):
        pub_date = self.cleaned_data.get('pub_date')

        if pub_date > date.today():
            raise forms.ValidationError("Date can't be greater than current date.")

        return pub_date
