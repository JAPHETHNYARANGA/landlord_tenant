from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework.exceptions import AuthenticationFailed
from .models import Admin, Tenant, Landlord, User
from .serializers import AdminSerializer, LandlordSerializer, TenantSerializer, UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.models import Token
import logging

# Get the custom user model
User = get_user_model()

logger = logging.getLogger(__name__)

@api_view(['POST'])
def login_view(request):
    """
    API endpoint to obtain a token for a user.
    """
    serializer = AuthTokenSerializer(data=request.data, context={'request': request})

    try:
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise AuthenticationFailed('Wrong Credentials')
                
                # Create or get the token
                token, created = Token.objects.get_or_create(user=user)
                
                # Prepare the response
                response_data = {
                    'data': token.key,
                    'isSuccessful': True,
                    'user': {
                        'email': user.email,
                        'role': user.role
                    }
                }
                return Response(response_data)
            except User.DoesNotExist:
                raise AuthenticationFailed('User with this email does not exist')
    except AuthenticationFailed as e:
        return Response({'isSuccessful': False, 'data': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'isSuccessful': False, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Admin Views
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_admin(request):
    serializer = AdminSerializer(data=request.data)
    
    if serializer.is_valid():
        user_data = serializer.validated_data.get('user', {})
        email = user_data.get('email')

        if not email:
            return Response({'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email, role='ADMIN').exists():
            return Response({'message': 'Admin with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
            send_invite_email(email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_admins(request):
    admins = User.objects.filter(role='ADMIN').order_by('id')
    serializer = UserSerializer(admins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_admin(request, admin_id):
    try:
        admin = User.objects.get(pk=admin_id, role='ADMIN')
    except User.DoesNotExist:
        return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdminSerializer(admin, data=request.data, partial=True)
    
    if serializer.is_valid():
        email = serializer.validated_data.get('email', admin.email)
        if User.objects.exclude(pk=admin.pk).filter(email=email, role='ADMIN').exists():
            return Response({'error': 'Admin with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_admin(request, admin_id):
    try:
        admin = User.objects.get(pk=admin_id, role='ADMIN')
        admin.delete()
        return Response({'message': 'Admin deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'Admin not found.'}, status=status.HTTP_404_NOT_FOUND)


# Tenant Views
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_tenant(request):
    serializer = TenantSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['user']['email']
        government_id = serializer.validated_data.get('government_id')
        house_number = serializer.validated_data.get('house_number')

        # Check if a Tenant with the same email already exists
        if User.objects.filter(email=email, role='TENANT').exists():
            return Response({'error': 'Tenant with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a Tenant with the same government_id already exists
        if Tenant.objects.filter(government_id=government_id).exists():
            return Response({'error': 'Tenant with this government ID already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a Tenant with the same house_number already exists
        if Tenant.objects.filter(house_number=house_number).exists():
            return Response({'error': 'Tenant with this house number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the tenant and send an email
        serializer.save()
        send_tenant_email(email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_tenants(request):
    tenants = Tenant.objects.all().order_by('user__id')
    serializer = TenantSerializer(tenants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
            if email and User.objects.exclude(pk=tenant.user.pk).filter(email=email, role='TENANT').exists():
                return Response({'error': 'Tenant with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_tenant(request, tenant_id):
    try:
        tenant = Tenant.objects.get(pk=tenant_id)
        tenant.delete()
        return Response({'message': 'Tenant deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Tenant.DoesNotExist:
        return Response({'error': 'Tenant not found.'}, status=status.HTTP_404_NOT_FOUND)


# Landlord Views
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_landlord(request):
    serializer = LandlordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['user']['email']
        government_id = serializer.validated_data.get('government_id')

        # Check if a Landlord with the same email already exists
        if User.objects.filter(email=email, role='LANDLORD').exists():
            return Response({'error': 'Landlord with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a Landlord with the same government_id already exists
        if Landlord.objects.filter(government_id=government_id).exists():
            return Response({'error': 'Landlord with this government ID already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the new Landlord
        serializer.save()
        send_landlord_email(email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_landlords(request):
    landlords = Landlord.objects.all().order_by('user__id')
    serializer = LandlordSerializer(landlords, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
            if email and User.objects.exclude(pk=landlord.user.pk).filter(email=email, role='LANDLORD').exists():
                return Response({'error': 'Landlord with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_landlord(request, landlord_id):
    try:
        landlord = Landlord.objects.get(pk=landlord_id)
        landlord.delete()
        return Response({'message': 'Landlord deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Landlord.DoesNotExist:
        return Response({'error': 'Landlord not found.'}, status=status.HTTP_404_NOT_FOUND)


# Helper functions for sending emails
def send_invite_email(email):
    subject = 'Welcome to Our Platform'
    message = 'Hello,\n\nYou have been added to our platform as an admin. Please log in to complete your profile.\n\nThank you!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
        logger.info(f'Invite email sent to {email}')
    except Exception as e:
        logger.error(f'Error sending email: {e}')


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
