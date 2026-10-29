from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BookPage


# ======================================================
# BOOK LIST
# ======================================================

def book_list(request):
    books = Book.objects.all().order_by("-created_at")

    if not books.exists():
        return redirect("Layout_Master:maintenance")

    # Check permission once
    can_manage = False

    if request.user.is_authenticated:
        if (
            request.user.is_superuser or
            request.user.groups.filter(name__in=["IT", "HR"]).exists()
        ):
            can_manage = True

    return render(
        request,
        "aura_books/book_list.html",
        {
            "books": books,
            "total_books": books.count(),
            "can_manage": can_manage,   # 🔥 pass to template
        }
    )



# ======================================================
# BOOK READER (UPDATED - NO MORE PAIRED PAGES)
# ======================================================
def book_reader(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # 🔥 IMPORTANT: Get all pages normally
    pages = book.pages.all().order_by("page_order")

    context = {
        "book": book,
        "pages": pages,   # ✅ send pages directly

        # Covers (optional, keep if you need them)
        "front_cover": book.front_cover_image,
        "front_inside_cover_image": book.front_inside_cover_image,
        "front_inside_cover_text": book.front_inside_cover_text,

        "back_cover": book.back_cover_image,
        "back_inside_cover_image": book.back_inside_cover_image,
        "back_inside_cover_text": book.back_inside_cover_text,
    }

    return render(request, "aura_books/book_reader.html", context)


# ======================================================
# CREATE BOOK
# ======================================================
def create_book(request):
    if request.method == "POST":

        # ---- Create Book ----
        book = Book.objects.create(
            title=request.POST.get("title"),
            author=request.POST.get("author"),
            year=request.POST.get("year"),

            front_cover_image=request.FILES.get("front_cover_image"),
            front_inside_cover_text=request.POST.get("front_inside_cover_text"),

            back_cover_image=request.FILES.get("back_cover_image"),
            back_inside_cover_text=request.POST.get("back_inside_cover_text"),
        )

        # ---- Get page data safely ----
        page_orders = request.POST.getlist("page_order[]")
        headings = request.POST.getlist("heading[]")
        paragraphs = request.POST.getlist("paragraph[]")

        # 🔥 Create pages
        for index, page_order in enumerate(page_orders):

            BookPage.objects.create(
                book=book,
                page_order=page_order,

                heading=headings[index] if index < len(headings) else "",
                paragraph=paragraphs[index] if index < len(paragraphs) else "",
            )

        return redirect("aura_books:book_list")

    return render(request, "aura_books/create_book.html")


from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def delete_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    # Permission check
    if not (
        request.user.is_superuser or
        request.user.groups.filter(name__in=["IT", "HR"]).exists()
    ):
        return redirect("aura_books:book_list")

    book.delete()
    messages.success(request, "Book deleted successfully.")

    return redirect("aura_books:book_list")

@login_required
def edit_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if not (
        request.user.is_superuser or
        request.user.groups.filter(name__in=["IT", "HR"]).exists()
    ):
        return redirect("aura_books:book_list")

    pages = book.pages.all().order_by("page_order")

    if request.method == "POST":

        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.year = request.POST.get("year")

        if request.FILES.get("front_cover_image"):
            book.front_cover_image = request.FILES.get("front_cover_image")

        if request.FILES.get("back_cover_image"):
            book.back_cover_image = request.FILES.get("back_cover_image")

        book.save()

        # Clear old pages
        book.pages.all().delete()

        page_orders = request.POST.getlist("page_order[]")
        headings = request.POST.getlist("heading[]")
        paragraphs = request.POST.getlist("paragraph[]")

        for i in range(len(page_orders)):
            BookPage.objects.create(
                book=book,
                page_order=page_orders[i],
                heading=headings[i],
                paragraph=paragraphs[i],
            )

        messages.success(request, "Book updated successfully.")
        return redirect("aura_books:book_list")

    return render(request, "aura_books/edit_book.html", {
        "book": book,
        "pages": pages,
    })
