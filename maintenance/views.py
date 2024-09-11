from .models import MaintenanceTicket
from .serializers import MaintenanceTicketSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def create_maintenance_ticket(request):
    serializer = MaintenanceTicketSerializer(data=request.data)
    
    # Creating an instance of MaintenanceTicket and passing new data to it
    if serializer.is_valid():
        validated_data = serializer.validated_data
        
        # Checking for existing MaintenanceTicket with same details
        existing_ticket = MaintenanceTicket.objects.filter(
            tenant_id=validated_data['tenant_id'],
            property_id=validated_data['property_id'],
            issue_type=validated_data['issue_type'],
            description=validated_data['description'],
            status=validated_data['status'],
            released_date=validated_data['released_date'],
        ).exists()
        
        # If a duplicate exists, return an error
        if existing_ticket:
            return Response({"detail": "A maintenance ticket with these details already exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Saving the new MaintenanceTicket if no duplicates are found
        serializer.save()  # : Save the valid data to the DB
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # If the data is not valid, return errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_tickets(request):
    tickets = MaintenanceTicket.objects.all()
    serializer = MaintenanceTicketSerializer(tickets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_ticket(request, ticket_id):
    # Find the ticket in the database using ticket_id
    try:
        ticket = MaintenanceTicket.objects.get(ticket_id=ticket_id)
    except MaintenanceTicket.DoesNotExist:
        # If the ticket does not exist, return an error
        return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    # Determining if the request is partial (PATCH) or full (PUT)
    partial = request.method == "PATCH"

    # Pass the existing ticket and new data to the serializer
    serializer = MaintenanceTicketSerializer(ticket, data=request.data, partial=partial)

    # Check if the provided data is valid
    if serializer.is_valid():
        # Save the updated ticket to the database
        serializer.save()
        # Respond with the updated ticket data and a success message
        return Response({"message": "Ticket updated successfully.","data": serializer.data}, status=status.HTTP_200_OK)
    # If data is not valid, return an error message and details
    return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_ticket(request,ticket_id):
    try:
        ticket = MaintenanceTicket.objects.get(pk=ticket_id)
        ticket.delete()
        return Response({'message': 'Ticket deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except MaintenanceTicket.DoesNotExist:
        return Response({'error': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)
