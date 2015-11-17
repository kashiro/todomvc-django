from django.db import models


class Todo(models.Model):
    '''Todo model'''
    #title = models.CharField('title', max_length=255, blank=False)
    title = models.CharField('title', max_length=255)
    completed = models.BooleanField('completed', default=False)

    @classmethod
    def create(cls, title, completed=False):
        todo = cls(title=title, completed=completed)
        return todo

    @classmethod
    def is_all_completed(cls):
        todos = cls.objects.all()
        return todos.filter(completed=True).count() == todos.count()

    @classmethod
    def all_update_completed(cls, completed):
        todos = cls.objects.all()
        for todo in todos:
            todo.completed = completed
            todo.save()

    @classmethod
    def delete(cls, todo_id=None):
        todos = cls.get_todos(todo_id)
        if todos:
            todos.delete()

    @classmethod
    def get_todos(cls, todo_ids=None):
        todos = None
        if type(todo_ids) == int or type(todo_ids) == str:
            todo_ids = str(todo_ids)
            try:
                todos = Todo.objects.get(pk=todo_ids)
            except Todo.DoesNotExist:
                pass
            return todos

        try:
            todos = cls.objects.all() if not todo_ids else Todo.objects.filter(pk__in=todo_ids)
        except Todo.DoesNotExist:
            pass
        return todos
