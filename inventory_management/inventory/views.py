from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import pytz, os
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from .forms import AddExhardForm
from .models import ProjectType, ExardProduct
import pandas as pd
from django.db.models import Sum
from plotly.offline import plot
import plotly.express as px
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import FileResponse, Http404
import json


# Create your views here.
#---- ADMIN ----#

def startup_view(request):
    return render(request, 'inventory_management/home.html')

def login_view(request):
    return render(request, 'inventory_management/login.html')

def admin_login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to custom admin dashboard
        else:
            error_message = 'Invalid credentials or not an admin user.'
    return render(request, 'inventory_management/adminLogin.html', {'error_message': error_message})

@login_required
def admin_dashboard_view(request):
    admin_name = request.user.get_full_name() or request.user.username
    # Get current time in Indian/Delhi timezone
    india_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(india_tz)
    hour = now.hour
    if hour < 12:
        greeting = 'Good morning'
    elif hour < 18:
        greeting = 'Good afternoon'
    else:
        greeting = 'Good evening'
    project_types = ProjectType.objects.all()
    return render(request, 'inventory_management/admin_dashboard.html', {
        'admin_name': admin_name,
        'greeting': greeting,
        'project_types': project_types
    })


def inventoryLogin_view(request):
    return render(request, 'inventory_management/inventoryhome.html')


#---- Xhard ----# 

def exhardForm_view(request):
    if request.method == 'POST':
        form = AddExhardForm(request.POST)
        if form.is_valid():
            exard_product = form.cleaned_data['alpha_number']
            added_quantity = form.cleaned_data['quantity']
            exard_product.quantity += added_quantity
            exard_product.save()
            return redirect('exhardForm')
    else:
        form = AddExhardForm()
    return render(request, 'inventory_management/exhardForm.html', {'form': form})



#---- Assembly ----#

def assembly_view(request):
    if request.method == 'POST':
        selected_alphas = request.POST.getlist('selected_alphas')

        for alpha in selected_alphas:
            try:
                product = ExardProduct.objects.get(alpha_number=alpha)
                withdraw_qty_str = request.POST.get(f'withdraw_qty_{alpha}', '0')
                try:
                    withdraw_qty = int(withdraw_qty_str)
                except ValueError:
                    withdraw_qty = 0

                if 0 < withdraw_qty <= product.quantity:
                    product.quantity -= withdraw_qty
                    product.save()
                else:
                    # Invalid or zero withdrawal quantity: do nothing or handle as needed
                    pass
            except ExardProduct.DoesNotExist:
                pass

        return redirect('assemblyform')

    # ... rest of your existing GET code unchanged
    excel_path = "C:/Users/navne/Desktop/legend/inventory_management/data/master_data.xlsx"
    excel_df = pd.read_excel(excel_path, usecols=['BAP', 'AlphaNumber'])

    products = ExardProduct.objects.all()
    db_df = pd.DataFrame.from_records(products.values('alpha_number', 'quantity'))
    db_df.rename(columns={'alpha_number': 'AlphaNumber', 'quantity': 'Quantity'}, inplace=True)

    merged_df = pd.merge(excel_df, db_df, on='AlphaNumber', how='left')
    merged_df['Quantity'] = merged_df['Quantity'].fillna(0)

    grouped_df = merged_df.groupby('BAP', as_index=False)['Quantity'].sum()
    grouped_df = grouped_df.sort_values(by='Quantity', ascending=False)

    fig = px.bar(
        grouped_df,
        x="BAP",
        y="Quantity",
        labels={"BAP": "BAP Number", "Quantity": "Quantity Present"},
        title="Quantity per BAP Number"
    )
    plot_div = plot(fig, output_type='div')

    bap_alpha_data = {}
    for bap, group in merged_df.groupby('BAP'):
        bap_alpha_data[bap] = group[['AlphaNumber', 'Quantity']].to_dict(orient='records')

    context = {
        'plot_div': plot_div,
        'bap_alpha_data_json': json.dumps(bap_alpha_data)
    }

    return render(request, "inventory_management/assemblyform.html", context=context)




# ---- DOWNLOAD EXCEL ----#


def download_excel(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'master_data.xlsx')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='master_data.xlsx')
    else:
        raise Http404("Excel file not found.")




#---- upload excel file ----#


# inventory/views.py
def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        # Full path where the file will be saved, replacing the old one
        destination_path = os.path.join(settings.UPLOAD_DIR, 'master_data.xlsx')

        try:
            # Ensure directory exists
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

            # Write file in chunks (safe for large files)
            with open(destination_path, 'wb+') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)

            messages.success(request, 'Excel file uploaded and replaced successfully!')
        except Exception as e:
            messages.error(request, f'Failed to upload file: {e}')
        return redirect('admin_dashboard')  # change to your dashboard URL name

    messages.error(request, 'No file selected for upload.')
    return redirect('admin_dashboard')



import os
# import pandas as pd
# from django.conf import settings
# from django.shortcuts import render
# from django.db.models import Sum
from .models import ExardProduct

def inventoryhome_view(request):
    # Calculate total parts from DB
    total_parts = ExardProduct.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    # Excel file path
    excel_path = os.path.join(settings.BASE_DIR, 'data', 'master_data.xlsx')

    # Initialize counts
    total_bap = 0
    total_alpha = 0

    try:
        # Try reading Excel file
        df = pd.read_excel(excel_path, usecols=['BAP', 'AlphaNumber'], header=0)


        # Sanitize BAP values: remove nulls and bad entries like "++", "?" etc.
        df['BAP'] = df['BAP'].astype(str).str.strip()
        df = df[df['BAP'].str.startswith('BAP')]  # Keep rows with valid BAP values

        # Count unique values
        total_bap = df['BAP'].nunique()
        total_alpha = df['AlphaNumber'].nunique()
        
      

    except Exception as e:
        print(f"Error reading Excel: {e}")  # Replace with logger in production

    # Pass values to template
    context = {
        'total_parts': total_parts,
        'total_bap': total_bap,
        'total_alpha': total_alpha,
    }
    return render(request, 'inventory_management/inventoryhome.html', context)
