from rest_framework.response import Response
from rest_framework import status
from .serializers import CofeeSerializer
from .models import Coffee
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import razorpay

razor_key_id = ''
razor_secret_id = ''


@api_view(['POST'])
def coffee_obj(request):
    try:
        data = request.data
        name = data.get('name')
        amount = data.get('amount')
        client = razorpay.Client(auth=(razor_key_id, razor_secret_id))
        payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'0'})
        payment_id = payment['id']
        serializer = Coffee(name=name, amount=amount, payment_id=payment_id)
        serializer.save()
        result = dict()
        result['data'] = CofeeSerializer(serializer).data
        return Response({'status':True, 'result':result, 'message':'Coffee Object created Successfully !'})
    except Exception as error:
        return Response({'status':False, 'result':dict(), 'message':'Coffee Object not created Successfully !'})

@api_view(['GET'])
def get_coffee(request, pk=None):
    if pk:
        try:
            get_obj = Coffee.objects.get(id=pk)
            serializer = CofeeSerializer(get_obj)
            result = dict()
            result['data'] = serializer.data
            return Response({"status":True, "result":result, "message":"Records Fetched Successfully !"})
        except Exception as error:
                return Response({"status":False, "result":serializer.errors, "message":"Records not Fetched Successfully !"})
    else:
        try:
            get_obj = Coffee.objects.all()
            serializer = CofeeSerializer(get_obj, many=True)
            result = dict()
            result['data'] = serializer.data
            return Response({"status":True, "result":result, "message":"Records Fetched Successfully !"})
        except Exception as error:
                return Response({"status":False, "result":serializer.errors, "message":"Records not Fetched Successfully !"})


@api_view(['PUT'])
def update_coffee(request,pk):
    try:
        data = request.data
        get_obj = Coffee.objects.get(id=pk)
        serializer = CofeeSerializer(get_obj, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            result = dict()
            result['data'] = serializer.data
            return Response({'status':True, 'result':result, 'message':'Coffee Object updated Successfully !'})
    except Exception as error:
        return Response({'status':False, 'result':dict(), 'message':'Coffee Object not updated Successfully !'})               