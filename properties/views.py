from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer


@api_view(['POST'])
def create_property(request):

    property_name = request.data.get('name')
    rooms = request.data.get('rooms')

    #checks if  a property with same name and room exits


    if Property.objects.filter(name=property_name, rooms=rooms).exists():
       return Response(
           {"error":"A property with this name and number of rooms already exists"},
           status=status.HTTP_400_BAD_REQUEST
       )
    #if there is no duplicates, proceed with serialization and saving
    serializer  = PropertySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      

@api_view(['GET'])
def list_property(request):
    tenants = Property.objects.all().order_by('id')
    serializer = PropertySerializer(tenants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['DELETE'])
def delete_property(request,id):
    try:
        property = Property.objects.get(pk=id)
        property.delete()
        return Response({'message': 'Property deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Property.DoesNotExist:
        return Response({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)



   

@api_view(['PUT'])
def update_property(request,id):
    try:
    #  Retrieving the property instance  by ID
        property_instance = Property.objects.get(id=id)
    except Property.DoesNotExist:
        #initializing the serializer with existing instance and new data
        return Response({'error':'Property not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PropertySerializer(property_instance, data=request.data)

    if serializer.is_valid():
        #Saving the updated property
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        