from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User'
        )
        self.regular_user = User.objects.create_user(
            email='user@example.com',
            password='userpassword',
            first_name='Regular',
            last_name='User'
        )
        self.teacher_user = User.objects.create_user(
            email='teacher@example.com',
            password='teacherpassword',
            first_name='Teacher',
            last_name='User',
            user_type='teacher'
        )
    
    def test_token_auth(self):
        """Test that users can obtain an auth token"""
        url = reverse('api_token_auth')
        
        # Test with valid credentials
        response = self.client.post(url, {
            'username': 'user@example.com',
            'password': 'userpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
        # Test with invalid credentials
        response = self.client.post(url, {
            'username': 'user@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_me_endpoint(self):
        """Test that users can access their own profile"""
        url = reverse('user-me')
        
        # Unauthenticated request should fail
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Authenticated request should succeed
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.regular_user.email)
    
    def test_user_permissions(self):
        """Test user permissions for different endpoints"""
        # Regular user can't create new users
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user-list')
        response = self.client.post(url, {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password_confirm': 'newpassword',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin can create new users
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password_confirm': 'newpassword',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)