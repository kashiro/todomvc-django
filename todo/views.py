from django.views.generic import TemplateView
from django.shortcuts import redirect
import json

from todo.models import Todo
from todo.forms import TodoForm


class Home(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        return self.render_to_response(self.get_context_data(request))

    def _post(self, request):
        form = TodoForm(request.POST, instance=Todo())
        if form.is_valid():
            # get data from form
            # form.cleaned_data.get('title')
            form.save()
        #else:
            # print(form.errors)

    def _update(self, data):
        todo = Todo.get_todos(data.get('id'))
        data.update({'completed': json.loads(data.get('completed'))})
        form = TodoForm(data, instance=todo)
        if form.is_valid():
            form.save()

    def _toggle_all_completed(self, toggle_all):
        toggle_all = json.loads(toggle_all)
        Todo.all_update_completed(toggle_all)

    def _delete(self, todo_ids):
        todos = Todo.get_todos(todo_ids)
        if todos:
            todos.delete()

    def post(self, request, *args):
        method = request.POST.get('method', '')
        todo_ids = request.POST.getlist('id', None)
        toggle_all = request.POST.get('toggle_all', '')

        if method == 'post':
            self._post(request)
        elif method == 'put':
            if toggle_all == 'true' or toggle_all == 'false':
                self._toggle_all_completed(toggle_all)
            else:
                self._update(request.POST.dict())
        elif method == 'delete':
            self._delete(todo_ids)

        return redirect('todo:home')

    def get_context_data(self, request):
        todos = Todo.objects.all().order_by('id')
        return {'todos': todos, 'filter': request.GET.get('filter', ''), 'all_completed': Todo.is_all_completed()}
