from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Admin, Tenant, Landlord, User
# from .serializers import AuthTokenSerializer
# from rest_framework.exceptions import AuthenticationFailed
from .serializers import AdminSerializer, LandlordSerializer, TenantSerializer, UserSerializer
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@csrf_exempt
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    logger.debug(f'Received login request with email: {email}')

    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        logger.warning(f'Invalid credentials for email: {email}')
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def login_view(request):
#     """
#     API endpoint to obtain a token for a user.
#     """
#     if request.method == 'POST':
#         serializer = AuthTokenSerializer(data=request.data, context={'request': request})
#         try:
#             if serializer.is_valid(raise_exception=True):
#                 email = serializer.validated_data.get('email')
#                 password = serializer.validated_data.get('password')

#                 try:
#                     user = User.objects.get(email=email)
#                     if not user.check_password(password):
#                         raise AuthenticationFailed('Wrong Credentials')
#                 except User.DoesNotExist:
#                     raise AuthenticationFailed('User with this email does not exist')

#                 token, created = Token.objects.get_or_create(user=user)
#                 return Response({'data': token.key, 'isSuccessful': True})
#         except AuthenticationFailed as e:
#             return Response({'isSuccessful': False, 'data': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             return Response({'isSuccessful': False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'isSuccessful': False, 'data': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['POST'])
def create_admin(request):
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        if User.objects.filter(email=email, role='admin').exists():
            return Response({'message': 'Admin with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(role='admin', is_staff=True)  # Ensure role is set to 'admin'
        send_invite_email(email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_invite_email(email):
    subject = 'Welcome to Our Platform'
    message = 'Hello,\n\nYou have been added to our platform as an admin. Please log in to complete your profile.\n\nThank you'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
        logger.info(f'Invite email sent to {email}')
    except Exception as e:
        logger.error(f'Error sending email: {e}')

@api_view(['GET'])
def list_admins(request):
    admins = User.objects.filter(role='admin')
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_admin(request, admin_id):
    try:
        admin = User.objects.get(pk=admin_id, role='admin')
    except User.DoesNotExist:
        return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdminSerializer(admin, data=request.data, partial=True)
    
    if serializer.is_valid():
        email = serializer.validated_data.get('email', admin.email)  # Use existing email if not provided
        if User.objects.exclude(pk=admin.pk).filter(email=email, role='admin').exists():
            return Response({'error': 'Admin with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_admin(request, admin_id):
    try:
        admin = User.objects.get(pk=admin_id)
        admin.delete()
        return Response({'message': 'Admin deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'Admin not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_tenant(request):
    serializer = TenantSerializer(data=request.data)
    if serializer.is_valid():
        user_data = serializer.validated_data['user']
        user_email = user_data.get('email')
        
        if User.objects.filter(email=user_email, role='tenant').exists():
            return Response({'error': 'Tenant with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        send_tenant_email(user_email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_tenant_email(email):
    subject = 'Tenant Registration Successful'
    message = 'Hello,\n\nYou have been successfully registered as a tenant.\n\nThank you!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
        logger.info(f'Tenant registration email sent to {email}')
    except Exception as e:
        logger.error(f'Error sending email: {e}')

@api_view(['PUT'])
def update_tenant(request, tenant_id):
    try:
        tenant = Tenant.objects.get(pk=tenant_id)
    except Tenant.DoesNotExist:
        return Response({'error': 'Tenant not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TenantSerializer(tenant, data=request.data, partial=True)
    if serializer.is_valid():
        user_data = request.data.get('user', None)
        if user_data:
            email = user_data.get('email')
            if email:
                if User.objects.exclude(pk=tenant.user.pk).filter(email=email, role='tenant').exists():
                    return Response({'error': 'Tenant with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_tenant(request, tenant_id):
    try:
        tenant = Tenant.objects.get(pk=tenant_id)
        tenant.delete()
        return Response({'message': 'Tenant deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Tenant.DoesNotExist:
        return Response({'error': 'Tenant not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_tenants(request):
    try:
        tenants = Tenant.objects.all().order_by('user_id')
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_landlord(request):
    serializer = LandlordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['user']['email']
        if User.objects.filter(email=email, role='landlord').exists():
            return Response({'error': 'Landlord with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        send_landlord_email(email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_landlord_email(email):
    subject = 'Landlord Registration Successful'
    message = 'Hello,\n\nYou have been successfully registered as a landlord.\n\nThank you!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
        logger.info(f'Landlord registration email sent to {email}')
    except Exception as e:
        logger.error(f'Error sending email: {e}')

@api_view(['GET'])
def list_landlords(request):
    landlords = Landlord.objects.all().order_by('user__id')
    serializer = LandlordSerializer(landlords, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_landlord(request, landlord_id):
    try:
        landlord = Landlord.objects.get(pk=landlord_id)
    except Landlord.DoesNotExist:
        return Response({'error': 'Landlord not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LandlordSerializer(landlord, data=request.data, partial=True)
    if serializer.is_valid():
        user_data = request.data.get('user', None)
        if user_data:
            email = user_data.get('email')
            if email:
                if User.objects.exclude(pk=landlord.user.pk).filter(email=email, role='landlord').exists():
                    return Response({'error': 'Landlord with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        updated_landlord = serializer.save()

        if user_data:
            user_serializer = UserSerializer(updated_landlord.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_landlord(request, landlord_id):
    try:
        landlord = Landlord.objects.get(pk=landlord_id)
        landlord.delete()
        return Response({'message': 'Landlord deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Landlord.DoesNotExist:
        return Response({'error': 'Landlord not found.'}, status=status.HTTP_404_NOT_FOUND)
