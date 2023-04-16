import traceback
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from .forms import CustomUserCreationForm



@api_view(['POST'])
def signup_view(request):

	try:
	
		form = CustomUserCreationForm(request.data)

		if form.is_valid():

			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password')

			user = form.save()

			backend = 'django.contrib.auth.backends.ModelBackend'  # specify the authentication backend

			user.backend = backend

			login(request, user, backend=backend)

			refresh = RefreshToken.for_user(user)

		
			return Response({
                'message': 'Account created successfully',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)

		else:
		    errors = form.errors.as_json()
		    return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

	# Catch any exception that may occur and return an error response
	except Exception as e :
			error_message = str(e)
			traceback_info = traceback.format_exc() 
			return Response({'error': error_message, 'traceback': traceback_info}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login_view(request):

	if request.method == 'POST':

		username = request.data.get('username')
		password1 = request.data.get('password1')

		# Get the underlying HttpRequest instance from the DRF Request instance
		django_request = request._request

		user = authenticate(django_request, username=username, password=password1)

	if user is not None:
		login(django_request, user)
		return Response({'message': 'Successfully logged in.'}, status=status.HTTP_200_OK)
	else:
		return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response({'success': 'Successfully logged out.'})