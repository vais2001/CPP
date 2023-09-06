from django.contrib import admin
from django.urls import path
from .views import GetAllDataSpecificTable, GetAllTablesNames, UpdateDataSpecificTableViaUniqueIdentification,update_entry,DeleteCaseAPI,CSVUploadView,delete_table

urlpatterns = [
    path('', GetAllTablesNames.as_view()),
    path('table/<str:table_name>/', GetAllDataSpecificTable.as_view()),
    path('update_data_unique_condition/', UpdateDataSpecificTableViaUniqueIdentification.as_view()),
    path('update_row_data',update_entry.as_view(),name='Update_entry'),
    path('delete_table',delete_table.as_view(),name='delete_table'),
    path('delete_case',DeleteCaseAPI.as_view(),name='delete_case'),
    path('csv_upload',CSVUploadView.as_view(),name='csv_upload')
]
