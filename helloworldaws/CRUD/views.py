from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect, render

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'

class PostCreateView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'post_form.html', {'form': form})
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
        return render(request, 'post_form.html', {'form': form})

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'post_confirm_delete.html'

