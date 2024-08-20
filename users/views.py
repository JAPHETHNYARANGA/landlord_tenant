from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from  .models import Admin,Tenant,Landlord
from .serializers  import AdminSerializer,LandlordSerializer,TenantSerializer
from django.core.mail import send_mail
from django.conf import settings
















@api_view(['POST'])
def create_admin(request):




 
  name =  request.data.get('name')
  email  = request.data.get('email')




  #checks if the an admin  with same username or email already exists
  if  Admin.objects.filter(name=name).exists():
     return Response({'message':'Admin with this name already exists.'})
 
  if  Admin.objects.filter(email=email).exists():
     return Response({'message': 'Admin with this email alreadry exists.'})
  #proceed with creation if no conflicts
  if request.method  == 'POST':
      serializer = AdminSerializer(data=request.data)
      if serializer.is_valid():
       serializer.save()
      send_invite_email(serializer.data['email'])
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def send_invite_email(email):
  subject = 'Welcome to Our Platform'
  message = (
      'Hello,\n\n'
      'You have been added to our platform as an admin. '
      'Please log in to complete your profile.\n\nThank you'
  )
  email_from = settings.EMAIL_HOST_USER
  recipient_list = [email]
   # Use the send_mail function from Django's email module
  send_mail(subject, message, email_from, recipient_list)






def  send_email(email):
  subject =  'Welcome to out platform'
  message = f'Hello,\n\n you haveb been added as a Tenant'
  email_from  = settings.EMAIL_HOST_USER
  recipient_list = ['email']
  send_mail(subject,message,email_from,recipient_list)
 








@api_view(['POST'])
def create_tenant(request):
   serializer = TenantSerializer(data=request.data)
   if serializer.is_valid():
       # Checks if the tenant already exists
       if Tenant.objects.filter(email=serializer.validated_data['email']).exists():
           return Response({'error': 'Tenant with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
      
       # Saving the tenant
       tenant = serializer.save()


       # Sending email
       subject = 'Tenant Registration Successful'
       message = f"Hello {tenant.name},\n\nYou have been successfully registered as a tenant.\n\nThank you!"
       from_email = settings.EMAIL_HOST_USER
       recipient_list = [tenant.email]


       try:
           send_mail(subject, message, from_email, recipient_list)
       except Exception as e:
           return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


       return Response(serializer.data, status=status.HTTP_201_CREATED)
   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
 




@api_view(['PUT'])
def update_tenant(request,tenant_id):
   try:
     #checks if the  tenant exists
      tenant  = Tenant.objects.get(pk=tenant_id)
   except Tenant.DoesNotExist:
      return Response({'error':'Tenant not found'}, status=status.HTTP_404_NOT_FOUND)


   #initialises serializer  with existing tenant and  new data from request
   serializer  =  TenantSerializer(tenant, data=request.data, partial=True)


   if serializer.is_valid():
   #checks if the  new email is alread used  by another tenant
       email = serializer.validated_data.get('email', tenant.email)
       if Tenant.objects.exclude(pk=tenant_id).filter(email=email).exists():
           return Response({'error':'Tenant with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
      


       #saving the  updated data
       serializer.save()
       return Response(serializer.data, status=status.HTTP_200_OK)
   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








@api_view(['DELETE'])
def  delete_tenant(request, tenant_id):
   try :
       #Retrieving  the tenant to be deleted
       tenant  = Tenant.objects.get(pk=tenant_id)
   except Tenant.DoesNotExist:
      return Response({'error':'Tenant not found.'}, status=status.HTTP_404_NOT_FOUND)
   #Deleting  the tenant
  
   tenant.delete()
  
   return Response({'message':'Tenant deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)






@api_view(['GET'])
def list_tenants(request):
   #Retrieving all tenants
   tenants =  Tenant.objects.all().order_by('tenant_id')
   #serializing the tenant data
   serializer = TenantSerializer(tenants, many=True)
   return Response(serializer.data, status=status.HTTP_200_OK)








#function to create landlord
@api_view(['POST'])
def create_landlord(request):
   # Creating an instance of landlord
   serializer = LandlordSerializer(data=request.data)
  
   if serializer.is_valid():
       # Case-insensitive check if another landlord exists with the same email
       if Landlord.objects.filter(email__iexact=serializer.validated_data['email']).exists():
           return Response({'error': 'Landlord with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
      
       # Save the landlord
       landlord = serializer.save()
      
       # Sending the email
       subject = 'Landlord registered successfully'
       message = f"Hello {landlord.name},\n\nYou have been successfully registered as a landlord.\n\nThank you!"
       from_email = settings.EMAIL_HOST_USER
       recipient_list = [landlord.email]
      
       try:
           send_mail(subject, message, from_email, recipient_list)
       except Exception as e:
           return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
       return Response(serializer.data, status=status.HTTP_201_CREATED)
  
   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#function to list all landlords available
@api_view(['GET'])
def  list_landlord(request):
   #retrieving all landlords
   landlords  = Landlord.objects.all().order_by('landlord_id')
  
   serializer  = LandlordSerializer(landlords, many=True)
   return Response(serializer.data, status=status.HTTP_200_OK)




#function to update landlord details
@api_view(['PUT'])
def update_landlord(request, landlord_id):
   try:
       # Check if the landlord exists
       landlord = Landlord.objects.get(pk=landlord_id)
   except Landlord.DoesNotExist:
       return Response({'error': 'Landlord does not exist'}, status=status.HTTP_404_NOT_FOUND)


   # Display the current landlord data
   # current_data = LandlordSerializer(landlord).data
   # print("Current Data: ", current_data)  # This will print the current data to the console/server logs.


   # Creates an instance of landlord serializer and passes requested data as JSON
   serializer = LandlordSerializer(landlord, data=request.data, partial=True)


   if serializer.is_valid():
       # Check if the email is being updated and if it already exists in another landlord
       email = serializer.validated_data.get('email', landlord.email)
       if Landlord.objects.exclude(pk=landlord_id).filter(email=email).exists():
           return Response({'error': 'Landlord with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)


       # Saving the updated data
       serializer.save()


       return Response(serializer.data, status=status.HTTP_200_OK)


   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






#function to delete landlord
@api_view(['DELETE'])
def  delete_landlord(request,landlord_id):
   try:
       #retrieving the landlord to be deleted
       landlord = Landlord.objects.get(pk=landlord_id)
   except Landlord.DoesNotExist:
       return Response({'error':'landlord  not found'}, status=status.HTTP_400_BAD_REQUEST)
      
       #deleting the landlord
   landlord.delete()
   return Response({'message':'landlord deleted successfully'},status=status.HTTP_204_NO_CONTENT)


      
