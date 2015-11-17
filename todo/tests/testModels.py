from django.test import TestCase
from todo.models import Todo


class TestTodo(TestCase):

    # instance method

    def test_create_instance(self):
        model = Todo(title='test title', completed=False)
        self.assertEqual(model.title,  'test title')
        self.assertFalse(model.completed)

    # class method

    def test_is_all_completed(self):
        Todo.create(title='test title').save()
        Todo.create(title='test title', completed=True).save()
        Todo.create(title='test title').save()
        self.assertFalse(Todo.is_all_completed())

        Todo.all_update_completed(True)
        self.assertTrue(Todo.is_all_completed())

        Todo.delete()

    def test_all_update_completed(self):
        Todo.create(title='test title').save()
        Todo.create(title='test title').save()
        Todo.create(title='test title').save()
        Todo.all_update_completed(True)
        self.assertEqual(
            Todo.objects.all().filter(completed=True).count(),
            Todo.objects.all().count())

    def test_delete(self):
        # delete a todo
        todo = Todo.create(title='test title')
        todo.save()
        Todo.delete(str(todo.id))
        self.assertEqual(
            Todo.objects.all().count(),
            0)

        # delete all todos
        Todo.create(title='test title').save()
        Todo.create(title='test title').save()
        Todo.create(title='test title').save()
        Todo.delete()
        self.assertEqual(
            Todo.objects.all().count(),
            0)

    def test_get_todos(self):
        # if can get todo
        todo = Todo.create(title='test title')
        todo.save()
        self.assertEqual(todo.id, Todo.get_todos(todo.id).id)
        # if can not get any todos 11111 is dummyid which dose not exist
        self.assertEqual(None, Todo.get_todos(11111))
        Todo.delete()

        # get all todos
        Todo.create(title='test title').save()
        Todo.create(title='test title').save()
        Todo.create(title='test title').save()
        todos = Todo.get_todos()
        self.assertEqual(Todo.objects.all().count(), todos.count())
