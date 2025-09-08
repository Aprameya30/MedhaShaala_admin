from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate

class EmailTokenObtainView(ObtainAuthToken):
    """
    Custom token auth view that uses email instead of username
    """
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=400)
            
        user = authenticate(email=email, password=password)
        
        if not user:
            return Response({'error': 'Invalid credentials'}, status=400)
            
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })