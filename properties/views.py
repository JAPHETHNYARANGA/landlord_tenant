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


   

