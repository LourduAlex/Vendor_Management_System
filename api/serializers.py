from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    class Meta:
        model = PurchaseOrder
        fields = ['id','vendor_name','order_date', 'delivery_date',
                   'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']
        
class HistoricalPerformanceSerializer(serializers.ModelSerializer):
        class Meta:
            model = HistoricalPerformance
            fields = '__all__'