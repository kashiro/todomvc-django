from django.test import RequestFactory, Client
from django.test import TestCase
from todo.views import Home
from todo.models import Todo


class testView(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDonw(self):
        Todo.delete()

    def test_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'index.html')

    def test_post(self):
        self.assertEquals(Todo.objects.all().count(), 0)
        response = self.client.post('/todo/', {'method': 'post', 'title': 'test title'})
        self.assertRedirects(response, '/')
        self.assertEquals(Todo.objects.all().count(), 1)

    def test_update(self):
        # update completed
        todo = Todo.create(title="test", completed=False)
        todo.save()
        response = self.client.post('/todo/', {'method': 'put', 'title': 'updated title', 'completed': 'true', 'id': todo.id})
        self.assertRedirects(response, '/')
        todo = Todo.get_todos(todo.id)
        self.assertEquals(todo.completed, True)
        self.assertEquals(todo.title, 'updated title')

    def test_update_toggle_all(self):
        Todo.create(title="test", completed=False).save()
        Todo.create(title="test", completed=False).save()
        response = self.client.post('/todo/', {'method': 'put', 'toggle_all': 'true'})
        self.assertRedirects(response, '/')
        self.assertEqual(Todo.objects.filter(completed=True).count(), 2)

    def test_delete_all(self):
        Todo.create(title="test", completed=False).save()
        Todo.create(title="test", completed=False).save()
        response = self.client.post('/todo/', {'method': 'delete'})
        self.assertRedirects(response, '/')
        self.assertEqual(Todo.objects.all().count(), 0)

    def test_delete(self):
        todo = Todo.create(title="test", completed=False)
        todo.save()
        response = self.client.post('/todo/', {'method': 'delete', 'id': todo.id})
        self.assertRedirects(response, '/')
        self.assertEqual(Todo.get_todos(todo.id), None)

    def test_get_context_data(self):
        # get filter params
        request = RequestFactory().get('/?filter=completed')
        view = Home()
        context = view.get_context_data(request)
        self.assertEqual(context['filter'], 'completed')

        request = RequestFactory().get('/?filter=active')
        view = Home()
        context = view.get_context_data(request)
        self.assertEqual(context['filter'], 'active')

        # get todo instances
        todo = Todo.create(title='test title')
        todo.save()
        request = RequestFactory().get('/')
        view = Home()
        context = view.get_context_data(request)
        self.assertEqual(context['todos'].first().id, todo.id)

        # is_completed
        self.assertFalse(context['all_completed'])
        todo.completed = True
        todo.save()
        context = view.get_context_data(request)
        self.assertTrue(context['all_completed'])
