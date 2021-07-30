from django.shortcuts import render, get_object_or_404
from profiles.models import Profile
from django.http import JsonResponse, HttpResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView, DetailView, TemplateView
from .forms import ReportForm
#Для создания PDF
from django.template.loader import get_template
import pdfkit
#Для работы с CSV
from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer
import csv
from django.utils.dateparse import parse_date

#Для разграничения прав (авторизация пользователя)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/detail.html'

#Работа с DropZone
class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/from_file.html'

@login_required
def csv_upload_view(request):
    print('Был загружен файл с данными')

    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name = csv_file_name)

        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()   #Пропускаем первую строку, т.к в ней содержатся названия колонок
                for row in reader:
                    #Получаем данные из строки
                    transaction_id = row[1]
                    product = row[2]
                    quantity = int(row[3])
                    customer = row[4]
                    date = parse_date(row[5])

                    #Выясняем, есть ли у нас такой продукт, если есть - получаем его объект
                    try:
                        product_obj = Product.objects.get(name__iexact=product) #Берём без учета регистра
                    except Product.DoesNotExist:
                        product_obj = None
                    #А тут мы получаем объекты продукта, покупателя, продавца и создаём корзину продажи(или берём существующую)
                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)

                        sale_obj, _ = Sale.objects.get_or_create(
                            transaction_id=transaction_id,
                            customer = customer_obj,
                            salesman = salesman_obj,
                            created = date
                            )
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
                return JsonResponse({'ex': False})
        else:
            return JsonResponse({'ex': True})        
                
                
    return HttpResponse()
#Конец работы с DropZone

@login_required
def create_report_view(request):
    form = ReportForm(request.POST or None)
    if request.is_ajax():
        #name = request.POST.get('name')
        #remarks = request.POST.get('remarks')
        
        image = request.POST.get('image')
        img = get_report_image(image)
        author = Profile.objects.get(user=request.user)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.image = img
            instance.author = author
            instance.save()

        #Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        return JsonResponse({'msg': 'send'})
    return JsonResponse({})


#Созднаие PDF (скопировано из документации https://xhtml2pdf.readthedocs.io/en/latest/usage.html)
"""
def render_pdf_view(request):
    template_path = 'reports/pdf.html'
    context = {'hello': 'Авававпыпвыпы!'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # Если мы скачиваем файл на компьютер
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # Если мы открываем файл в браузере
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
"""
# Мой вариант создания PDF (тут работает кириллица) https://learnbatta.com/blog/django-html-to-pdf-using-pdfkit-and-wkhtmltopdf-5/
@login_required
def render_pdf_view(request, pk):
    try:
        # Тут мы рендерим шаблон данными
        template_path = 'reports/pdf.html'
        obj = get_object_or_404(Report, pk=pk)
        context = {'obj': obj}
        template = get_template(template_path)
        html = template.render(context)

        # А тут настраиваем вывод файла
        output= pdfkit.from_string(html, output_path=False)
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'filename="report.pdf"'
        response.write(output)        
    except Exception:
        return HttpResponse('У нас возникли проблемы <pre>' + html + '</pre>')
    return response

