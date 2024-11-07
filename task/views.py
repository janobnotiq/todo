from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import RegisterForm,CommentForm

from .models import Category, Task,Comment

def custom_page_not_found(request,exception):
    return render(request,"404.html",status=404)


@login_required  # type: ignore
def filtered_tasks(request, slug):
    category = get_object_or_404(Category, slug=slug)
    tasks = Task.objects.filter(category=category, doer=request.user)

    return render(
        request,
        "tasks.html",
        {
            "tasks": tasks,
            "category": category,
        },
    )


@login_required  # type: ignore
def mark_as_undone(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    task.is_done = False
    task.save()

    return redirect("home")


@login_required  # type: ignore
def mark_as_done(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    task.is_done = True
    task.save()

    return redirect("home")


@login_required  # type: ignore
def delete_task(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required  # type: ignore
def edit_task(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()
    categories = Category.objects.all()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    if request.method == "POST":
        try:
            changed = request.POST["changed"]
            category = request.POST["category"]
            category = get_object_or_404(Category, name=category)
        except Exception:
            return redirect("home")

        task.task = changed if len(changed) > 0 else task.task
        task.category = category
        task.save()

        return redirect("home")
    else:
        return render(
            request,
            "edit.html",
            {
                "task": task,
                "categories": categories,
            },
        )


@login_required  # type: ignore
def add_task(request):
    if request.method == "POST":
        try:
            task = request.POST["task"]
            category = request.POST["category"]
            category = get_object_or_404(Category, name=category)
            print(task, category)
        except Exception:
            return redirect("home")

        if task is not None:
            Task.objects.create(task=task, category=category, doer=request.user)

        return redirect("home")


def home(request):
    categories = Category.objects.all()
    
    try:
        tasks = Task.objects.filter(doer=request.user, is_done=False)
        done_tasks = Task.objects.filter(doer=request.user, is_done=True)
    except Exception:
        tasks = []
        done_tasks = []

    return render(
        request,
        "home.html",
        {"tasks": tasks, "categories": categories, "completed_tasks": done_tasks},
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
                        

            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )

            user.set_password(password)
            user.save()

            return redirect("login")
        else:
            messages.warning(request,"Bunday taxallusli foydalanuvchi tizimda bor!")
            form = RegisterForm
            return render(request, "register.html", {"form": form})
    else:
        form = RegisterForm

        return render(request, "register.html", {"form": form})

@login_required
def add_comment_view(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            stars = form.cleaned_data["stars"]
            author = request.user
            
            comment = Comment.objects.filter(author=author).last()
            
            if comment:
                messages.error(request,"Siz oldin fikr bildirgansiz!")
                return redirect(request.META.get('HTTP_REFERER'))
            
            Comment.objects.create(author=author,text=text,stars=stars)
            return redirect("home")
        else:
            messages.warning(request,"Nimadir xato ketdi!")
            form = CommentForm
            return render(request,"add-comment.html",{"form":form})
    else:
        form = CommentForm
        return render(request,"add-comment.html",{"form":form})
    

def comments_list_view(request):
    comments = Comment.objects.all()
    return render(request,"comments.html",{"comments":comments,"comment_count":comments.count()})

def delete_comment(request,pk):
    comment = get_object_or_404(Comment,id=pk)
    if comment.author == request.user:
        comment.delete()
    else:
        messages.error(request,"Adashib nimanidir bosib yubordingiz, shekilli😉")
        
    return redirect(request.META.get('HTTP_REFERER'))

class CommentUpdateView(LoginRequiredMixin,UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "update-comment.html"
    success_url = reverse_lazy("comments")

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)