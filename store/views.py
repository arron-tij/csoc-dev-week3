from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import datetime
# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name='store/book_detail.html'
    context={
        'book':Book.objects.get(pk=bid), # set this to an instance of the required book
        'num_available':None, # set this 1 if any copy of this book is available, otherwise 0
    }
    # START YOUR CODE HERE
    try:
        instnc=Book.objects.get(pk=bid)
        BookCopy.objects.get(book=instnc)
        context['num_available'] = 0
    except:
        context['num_available'] = 1
    return render(request, template_name, context=context)


def bookListView(request):
    template_name='store/book_list.html'
    context={
        'books':None, # set here the list of required books upon filtering using the GET parameters
    }    
    get_data=request.GET
    # START YOUR CODE HERE
    books=Book.objects.all()
    try:
        querytitle = get_data['title']
        books = Book.objects.filter(title__icontains=querytitle)
    except:
        pass  
    try:
        queryauthor = get_data['author']
        books = Book.objects.filter(author__icontains=queryauthor)
    except:
        pass  
    try:
        querygenre = get_data['genre']
        books = Book.objects.filter(genre__icontains=querygenre)
    except:
        pass      
    
    context['books']=books
    return render(request,template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name='store/loaned_books.html'
    context={
        'books':None,
    }
    '''
    The above key books in dictionary context should contain a list of instances of the 
    bookcopy model. Only those books should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    
    context['books']=BookCopy.objects.filter(borrower=request.user)
    
    return render(request,template_name,context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    response_data={
        'message':None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    book_id = request.POST['bid'] # get the book id from post data
    instnc=Book.objects.get(pk=book_id)
    try:
        BookCopy.objects.get(book=instnc)
        response_data['message'] = 0
    except: 
        BookCopy.objects.create(book=instnc, borrow_date=datetime.datetime.now(),borrower=request.user)
        response_data['message'] = 1

    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    response_data={
        'message':None,
    }
    book_id=request.POST['bid']
    instnc=Book.objects.get(pk=book_id)
    try:
        BookCopy.objects.get(book=instnc).delete()
        response_data['message']=1;
    except:
        response_data['message']=0

    return JsonResponse(response_data)


@csrf_exempt
@login_required
def rateBook(request):
    response_data={
        'message':None,
    }
    book_id=request.POST['bid']
    rating=request.POST['rating']
    instnc=Book.objects.get(pk=book_id)
    try:        
        instnc.total_rating = instnc.total_rating + int(rating)        
        instnc.total_users = instnc.total_users + int(1)
        instnc.rating = instnc.total_rating/instnc.total_users
        instnc.save()
        response_data['message'] = 1
    except:
        response_data['message'] = "failure"
    return JsonResponse(response_data)






