from django.urls import path
from app.goods.views import orderfindview,orderingview,goodfindview,machinequeryview,\
    deliversuccessview,recommendView,machineaddressView,orderfindbyuserView,imgView,goodfindbycategory1View,goodfindbycategory2View

urlpatterns = [
    path('ordering',orderingview.as_view()),
    path('orderfind',orderfindview.as_view()),
    path('goodfind',goodfindview.as_view()),
    path('ordercheck',machinequeryview.as_view()),
    path('orderchange',deliversuccessview.as_view()),
    path('orderrec',recommendView.as_view()),
    path('machinefind',machineaddressView.as_view()),
    path('orderbyuser',orderfindbyuserView.as_view()),
    path('imgrotation',imgView.as_view()),
    path('cuisine',goodfindbycategory1View.as_view()),
    path('cooker',goodfindbycategory2View.as_view()),
]