from rest_framework import status 
from .models   import Booking
from .serializers import BookingSerializer
from rest_framework.decorators  import api_view
from rest_framework.response import Response






@api_view(['POST'])
def creating_booking(request):
    # Creating an instance of Booking and passing new data to it
    serializer = BookingSerializer(data=request.data)

    if serializer.is_valid():
        validated_data = serializer.validated_data

        # Checking for existing bookings with the same details
        existing_bookings = Booking.objects.filter(
            property_id=validated_data['property_id'],
            booking_date=validated_data['booking_date'],
            status=validated_data['status'],
        ).exists()

        # If a duplicate exists, throw an error
        if existing_bookings:
            return Response({"error": "Booking with these details already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Saving the new booking if no duplicates are found
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # If the data is not valid, return an error response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


@api_view(['GET'])
def list_bookings(request):
    bookings  = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)




@api_view(['PUT'])
def update_bookings(request, booking_id):
    #Finding the ticket in the database
    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except Booking.DoesNotExist:
        #if the  booking does not exists run an error
        return Response({"error":"Booking not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Determining if the request is partial (PATCH) or full (PUT)
    partial  = request.method == "PATCH"
    # Pass the existing booking and new data to the serializer
    serializer  = BookingSerializer(booking, data=request.data,partial=partial)
    #checking id the provided data is valid
    if serializer.is_valid():
        #save the new data
        serializer.save()
        #Respond with  the updated booking and  a success message
        return Response({"message":"booking updated successfully"},status=status.HTTP_200_OK)
    




@api_view(['DELETE'])
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        booking.delete()
        return Response({"message":"Booking deleted succcessfully"}, status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({"error":"Booking not found"},status=status.HTTP_204_NO_CONTENT)


     