from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Orders
from .serializers import OrderSerializer
from django.core.files.base import ContentFile
import qrcode
import io
from rest_framework.permissions import IsAuthenticated

class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Save the order with the authenticated user
            order = serializer.save(user=request.user)

            # Generate QR code
            qr_data = serializer.validated_data['data']  # Use provided order data for QR code generation
            qr_code_image = qrcode.make(qr_data)
            
            # Save QR code to ImageField
            buffer = io.BytesIO()
            qr_code_image.save(buffer, format="PNG")
            qr_code_file = ContentFile(buffer.getvalue(), name=f"qr_code_{order.id}.png")
            order.qr_code = qr_code_file
            order.save()

            return Response({
                'message': 'Order created successfully.',
                'order': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)