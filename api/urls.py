from django.urls import path
from .views import VendorView, VendorListView, VendorDetailView, VendorUpdateView, DeleteVendorView
from .views import PurchaseOrderView, PurchaseOrderDetailView, PurchaseOrderListView, PurchaseOrderUpdateView, DeletePurchaseOrderView
from .views import VendorperformanceView,  AcknowledgePurchaseOrderView

urlpatterns = [
       
                #_________VENDOR MODEL API'S__________#

    path('vendor/', VendorView.as_view(), name='Vendor'),
    path('vendors/', VendorListView.as_view(), name='Vendors'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='VendorDetail'),
    path('vendor_update/<int:id>/', VendorUpdateView.as_view(), name='vendor_update'),
    path('vendors/<int:id>/', DeleteVendorView.as_view(), name='delete_vendor'),

    path('purchase_order/',PurchaseOrderView.as_view(), name='purchase_order'),
    path('purchase_order/<int:pk>/', PurchaseOrderDetailView.as_view(), name='PurchaseOrderDetail'),
    path('purchase_orders/',PurchaseOrderListView.as_view(), name='PurchaseOrderList'),
    path('purchase_orders_update/<int:id>/',PurchaseOrderUpdateView.as_view(), name='PurchaseOrderUpdate'),
    path('purchase_order/<int:id>/', DeletePurchaseOrderView.as_view(), name='Delete PurchaseOrder'),

    path('purchase_orders/<int:vendor_id>/performance',VendorperformanceView.as_view(), name='Vendorperformance'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),
    
]  