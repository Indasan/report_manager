from django.urls import path
from .views import (
    create_report_view, 
    ReportListView, 
    ReportDetailView, 
    render_pdf_view,
    UploadTemplateView,
    csv_upload_view,
    )

app_name = 'reports'

urlpatterns = [
    path('', ReportListView.as_view(), name='main'),
    path('save/', create_report_view, name='create-report'),
    path('upload/', csv_upload_view, name='upload'),                    #Для обработки файла из DropZone
    path('from_file/', UploadTemplateView.as_view(), name='from-file'), #Для отображения DropZone
    path('<pk>/', ReportDetailView.as_view(), name='detail'),
    path('<pk>/pdf/', render_pdf_view, name='pdf'),
]