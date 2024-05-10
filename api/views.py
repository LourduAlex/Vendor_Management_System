from datetime import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Avg, F
from django.utils import timezone
from .models import Vendor, PurchaseOrder, HistoricalPerformance




                                            #_________VENDOR MODEL API'S__________#

#__________CREATE VENDOR API____________#                                         

class VendorView(APIView):
    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.save()

            response_data = {
                'success': True,
                'message': "Account Created Successfully",
                'userId': instance.id,
                'name': instance.name,
                'contact_details': instance.contact_details,
                'address': instance.address,
                'vendor_code': instance.vendor_code,
                'on_time_delivery_rate': instance.on_time_delivery_rate,
                'quality_rating_avg': instance.quality_rating_avg,
                'average_response_time': instance.average_response_time,
                'fulfillment_rate': instance.fulfillment_rate

            }
            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#__________ VENDOR LIST API____________# 

class VendorListView(ListAPIView):
    queryset= Vendor.objects.all()
    serializer_class = VendorSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()  
        serializer = self.get_serializer(queryset, many=True)
        
        data = {
            'success': True,
            'message': "All Vendors are retrieved Successfully",
            'vendors_list': serializer.data  
        }
        status_code = status.HTTP_200_OK

        return Response(data, status=status_code)
    
#__________PARTICULAR VENDOR API____________# 

class VendorDetailView(APIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=self.kwargs.get(self.lookup_field))
        serializer = self.serializer_class(instance)
        data = {
            'success': True,
            'message': "Particular vendor retrieved successfully",
            'vendor': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

#__________UPDATE VENDOR API____________# 

class VendorUpdateView(APIView):
    def put(self, request, id): 
        vendor_instance = get_object_or_404(Vendor, pk=id) 
        
        data = request.data
        serializer = VendorSerializer(vendor_instance, data=data, partial=True)  
        
        if serializer.is_valid():
            serializer.save() 
            return Response({
                'success': True,
                'message': 'Particular Vendor Details updated successfully',
                'vendor': serializer.data  
            })
        
        return Response({
            'error': 'Invalid data',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
#__________DELETE VENDOR API____________# 

class DeleteVendorView(APIView):
    def delete(self, request, id):
        vendor_instance = get_object_or_404(Vendor, pk=id)
        vendor_instance.delete()
        
        return Response({
            'success': True,
            'message': 'Particular Vendor deleted successfully',
            'vendor': vendor_instance.data
        }, status=status.HTTP_204_NO_CONTENT) 
       

                                    #_________PURCHASE_ORDER MODEL API'S__________#

class PurchaseOrderView(APIView):
    def post(self, request, format=None):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.save()

            response_data = {
                'success': True,
                'message': "PurchaseOrder Created Successfully",
                'id': instance.id,
                'po_number': instance.po_number,
                'vendor': instance.vendor,
                'order_date': instance.order_date,
                'delivery_date': instance.delivery_date,
                'items': instance.items,
                'quantity': instance.quantity,
                'status': instance.status,
                'quality_rating': instance.quality_rating,
                'issue_date': instance.issue_date,
                'acknowledgment_date': instance.acknowledgment_date,

            }
            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PurchaseOrderListView(ListAPIView):
    queryset= PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()  
        serializer = self.get_serializer(queryset, many=True)
        
        data = {
            'success': True,
            'message': "All Purchase_Order are retrieved Successfully",
            'vendors_list': serializer.data  
        }
        status_code = status.HTTP_200_OK

        return Response(data, status=status_code)


class PurchaseOrderDetailView(APIView):
    queryset = PurchaseOrder.objects.all()  # Use PurchaseOrder, not Vendor
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=self.kwargs.get(self.lookup_field))
        serializer = self.serializer_class(instance)
        data = {
            'success': True,
            'message': "Particular Purchase_Order retrieved successfully",
            'purchase_order': serializer.data  # Correct key here
        }
        return Response(data, status=status.HTTP_200_OK)
    

class PurchaseOrderUpdateView(APIView):
    def put(self, request, id): 
        purchase_order_instance = get_object_or_404(Vendor, pk=id) 
        
        data = request.data
        serializer = PurchaseOrderSerializer(purchase_order_instance, data=data, partial=True)  
        
        if serializer.is_valid():
            serializer.save() 
            return Response({
                'success': True,
                'message': 'Particular Purchase Order Details updated successfully',
                'PurchaseOrder': serializer.data  
            })
        
        return Response({
            'error': 'Invalid data',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class DeletePurchaseOrderView(APIView):
    def delete(self, request, id):
        purchase_order_instance = get_object_or_404(PurchaseOrder, pk=id)

        purchase_order_instance.delete()
        
        return Response({
            'success': True,
            'message': 'Particular Purchase Order deleted successfully',
            'vendor': purchase_order_instance.data
        }, status=status.HTTP_204_NO_CONTENT) 

class VendorperformanceView(APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

        total_completed_pos = completed_pos.count()
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=F('delivery_date')).count()  
        if total_completed_pos > 0:
            on_time_delivery_rate = on_time_delivered_pos / total_completed_pos
        else:
            on_time_delivery_rate = 0.0

        historical_performance = HistoricalPerformance.objects.filter(vendor=vendor)

        quality_rating_avg = historical_performance.aggregate(Avg('quality_rating_avg'))['quality_rating_avg__avg']
        average_response_time = historical_performance.aggregate(Avg('average_response_time'))['average_response_time__avg']
        fulfillment_rate = historical_performance.aggregate(Avg('fulfillment_rate'))['fulfillment_rate__avg']

        performance_data = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate
        }

        return Response(performance_data)
    

class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, po_id):
        # Retrieve the PurchaseOrder object
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.status = 'complete'
        purchase_order.save()
      
        serializer = PurchaseOrderSerializer(purchase_order)

        return Response({"message": "Purchase order acknowledged successfully",
                         'purchase_order': serializer.data}, status=status.HTTP_200_OK)
