from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .utils import get_mongodb
from .forms import QuoteForm
from .models import Author, Quote


def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    form = QuoteForm()
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, 'form': form})


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote_text = form.cleaned_data['quote']
            author_name = form.cleaned_data['author']
            author, created = Author.objects.get_or_create(fullname=author_name)
            quote = Quote.objects.create(quote=quote_text, author=author)
            return redirect('quotes:root')
    else:
        form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {'form': form})