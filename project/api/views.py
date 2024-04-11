from django.shortcuts import render
from .models import *
from .permissions import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

@api_view(['GET'])
def productsView(request):
    products = Product.objects.all()
    prod_ser = ProductSer(products, many=True)
    return Response({'data':prod_ser.data})



@api_view(['POST'])
def login(request):
    user_ser = LoginSer(data=request.data)
    if user_ser.is_valid():
        try:
            user = User.objects.get(email = user_ser.validated_data['email'])
        except:
            return Response({'error:':{'code':401, 'message':'Authentication failed'}})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'data':{'user_token':token.key}})
    return Response({'error':{'code':422,'message':'Validation error', 'errors':user_ser.errors}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'data':{'message':'logout'}})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProd(request):
    prod_ser = ProductSer(data=request.data)
    if prod_ser.is_valid():
        prod_ser.save()
        return Response({'data':{'id': prod_ser.data['id'], 'message':'Product Added'}})
    return Response({'error':{'code':422, 'message':'Validation error', 'errors':prod_ser.errors}})


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def changeProduct(request,pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response({'error':{'code':403, 'message':'not found'}})
    if request.method == 'DELETE':
        product.delete()
        return Response({'data':{'message':'Product removed'}})
    elif request.method == 'PATCH':
        prod_ser = ProductSer(data=request.data, instance=product, partial=True)
        if prod_ser.is_valid():
            prod_ser.save()
            return Response({'data':prod_ser.data})
        return Response({'error':{'code':422, 'message':'Validation error', 'errors':prod_ser.errors}})


@api_view(['GET'])
@permission_classes([IsClient])
def getCarts(request):
    carts = Carts.objects.all()
    cart_ser = CartsSer(carts, many=True)
    return Response({'data':cart_ser.data})


@api_view(['DELETE', 'POST'])
@permission_classes([IsClient])
def changeCarts(request, pk):
    if request.method == 'DELETE':
        try:
            cart = Carts.objects.get(pk=pk)
        except:
            return Response({'error':{'code':403, 'message':'not found'}})
        cart.delete()
        return Response({'data':{'message':'Product removed from cart'}})
    elif request.method == 'POST':
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response({'error':{'code':403,  'message':'not found'}})
        Carts.objects.create(user=request.user, product=product)
        return Response({'data':{'message':'Product add to cart'}})


@api_view(['GET', 'POST'])
@permission_classes([IsClient])
def orderChange(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        order_ser = OrderSer(orders, many=True)
        return Response({'data':order_ser.data})
    elif request.method == 'POST':
        try:
            carts = Carts.objects.filter(user=request.user)
        except:
            return Response({'error':{"code":403, 'message':'not found'}})
        order = Order.objects.create(user=request.user, order_price=0)
        order_price = 0
        for cart in carts:
            order.product.add(cart.product)
            order_price+= cart.product.price
        order.order_price = order_price
        order.save()
        order_ser =OrderSer(order)
        return Response({'data':{'order_id':order_ser.data['id'], 'message':'order id processed'}})