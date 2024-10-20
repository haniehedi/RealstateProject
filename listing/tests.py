from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Property, Agent


class PropertyViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='agentuser', password='password')
        self.agent = Agent.objects.create(user=self.user, phone='1234567890')
        self.property1 = Property.objects.create(
            title='Luxury Apartment',
            description='A luxury apartment in the city center',
            price=250000,
            address='123 Main St',
            city='New York',
            agent=self.agent
        )
        self.property2 = Property.objects.create(
            title='Cozy Cottage',
            description='A cozy cottage in the countryside',
            price=150000,
            address='456 Elm St',
            city='Los Angeles',
            agent=self.agent
        )

    def test_list_properties(self):
        url = reverse('listing:properties-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_properties_by_city(self):
        url = reverse('listing:properties-list') + '?city=New%20York'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Luxury Apartment')

    def test_filter_properties_by_price_range(self):
        url = reverse('listing:properties-list') + '?min_price=100000&max_price=200000'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Cozy Cottage')

    def test_order_properties_by_price(self):
        url = reverse('listing:properties-list') + '?ordering=price'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Cozy Cottage')

    def test_create_property(self):
        url = reverse('listing:properties-list')
        data = {
            'title': 'Modern House',
            'description': 'A modern house with a garden',
            'price': 300000,
            'address': '789 Pine St',
            'city': 'San Francisco',
            'agent': self.agent.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 3)

    def test_update_property(self):
        url = reverse('listing:properties-detail', kwargs={'pk': self.property1.pk})
        data = {
            'title': 'Updated Luxury Apartment',
            'description': 'An updated luxury apartment in the city center',
            'price': 260000,
            'address': '123 Main St',
            'city': 'New York',
            'agent': self.agent.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.property1.refresh_from_db()
        self.assertEqual(self.property1.title, 'Updated Luxury Apartment')

    def test_delete_property(self):
        url = reverse('listing:properties-detail', kwargs={'pk': self.property1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.count(), 1)


class AgentViewSetTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='john', password='password1')
        self.agent1 = Agent.objects.create(user=self.user1, phone='1234567890')

        self.user2 = User.objects.create_user(username='jane', password='password2')
        self.agent2 = Agent.objects.create(user=self.user2, phone='0987654321')

    def test_list_agents(self):
        url = reverse('listing:agents-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_agent(self):
        url = reverse('listing:agents-list')
        data = {
            'user': {
                'username': 'alice',
                'password': 'password3',
                'email': 'alice@example.com'
            },
            'phone': '1122334455'
        }
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_agent(self):
        url = reverse('listing:agents-detail', kwargs={'pk': self.agent1.pk})
        data = {
            'phone': '1112223333'
        }

