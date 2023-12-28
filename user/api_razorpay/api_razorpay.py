from rest_framework.views import APIView
from rest_framework import status
from .api_serializer import CreateOrderSerializer
from rest_framework.response import Response
from user.api_razorpay.razorpay.main import RazorpayClient
from vendor.models import *
from accounts.models import *
from user.models import *
from user.api_razorpay.api_serializer import *


rz_client = RazorpayClient()

class CreateCarOrderAPIView(APIView):
    def post(self, request, *args, **kwargs):
        car_id = self.kwargs.get('carId')
        pickup_date = self.kwargs.get('pickupDate').strip()
        return_date = self.kwargs.get('returnDate').strip()
        user_id = self.kwargs.get('userId')

        try:
            car = CarHandling.objects.get(id=car_id)
            customuser_obj=UserAccount.objects.get(id=user_id)
            user_profile=UserProfile.objects.get(user=customuser_obj)

            overlapping_bookings = Booking.objects.filter(
                car=car,
                return_date__gt=pickup_date,
                pickup_date__lt=return_date
            )

            if overlapping_bookings.exists():
                return Response({"message": "No cars available for the selected dates"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                create_order_serializer = CreateOrderSerializer(data=request.data)

                if create_order_serializer.is_valid():
                    amount = create_order_serializer.validated_data.get("amount")
                    currency = create_order_serializer.validated_data.get("currency")

                    order_response = rz_client.create_order(
                        amount=amount,
                        currency=currency
                    )
                    print(order_response,"response_order")

                    response = {
                        "status_code": status.HTTP_201_CREATED,
                        "message": "order_created",
                        "data": order_response
                    }
                else:
                    response = {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "bad request",
                        "error": create_order_serializer.errors
                    }

                return Response(response)

        except Exception as e:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CreateCarBookingAPIView(APIView):
    def post(self, request, *args, **kwargs):
        car_id = self.kwargs.get('carId')
        pickup_date = self.kwargs.get('pickupDate').strip()
        return_date = self.kwargs.get('returnDate').strip()
        user_id = self.kwargs.get('userId')

        car = CarHandling.objects.get(id=car_id)
        customuser_obj=UserAccount.objects.get(id=user_id)
        user_profile=UserProfile.objects.get(user=customuser_obj)

        pickup=pickup_date.split('-')
        print("pickup::",pickup[2])

        day_return=return_date.split('-')
        print("day_return:",day_return[2])

        no_ofdays=int(day_return[2])-int(pickup[2])+1
        print("no_ofdays::",no_ofdays)

        
        data = request.data
        print(data,"__data___")

        razorpay_order_id = data.get("order_id")
        razorpay_payment_id = data.get("payment_id")
        razorpay_signature = data.get("signature")

        data = {
            "order_id":razorpay_order_id,
            "payment_id":razorpay_payment_id,
            "signature":razorpay_signature,
            }
        
        print("data_02", data)

        create_order_serializer = TransactioncharcheckSerializer(data=data)

        if create_order_serializer.is_valid():
            print(data,"data_inside_serailizer")
            
            is_status = rz_client.verify_payment(
                razorpay_order_id,
                razorpay_payment_id,
                razorpay_signature,
            )

            if is_status:
                total_amount = car.price
                booking_obj = Booking.objects.create(
                    car=car,
                    user=user_profile,
                    pickup_date=pickup_date,
                    return_date=return_date,
                    total_amount=total_amount,
                )

                Transcation.objects.create(
                    booking=booking_obj,
                    user=user_profile,
                    partner=car.vendor.user.vendor_profile,
                    partner_share=0.7 * float(total_amount),
                    company_share=0.3 * float(total_amount),
                    signature=razorpay_signature,
                    payment_id=razorpay_payment_id,
                    order_id=razorpay_order_id,
                )

                response = {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "Order created successfully",
                }
            else:
                response = {"status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Payment verification failed",
                }

            return Response(response)

        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Bad request",
                "error": create_order_serializer.errors
            }
            return Response(response)
