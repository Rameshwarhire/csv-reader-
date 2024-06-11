from django.shortcuts import render,redirect
from .models import *
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Create your views here.

def home(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        histogram = readcsv(file)

        return render(request, 'histogram.html', {'histogram': histogram})

    return render(request, 'home.html')

def readcsv(file):
    df = pd.read_csv(file, delimiter=',')
    print(df.head(10))
    print(df.describe())

    mean_all = df[["Age", "ApproxHeight", "ApproxWeight", "Expense_Semester", 'Expense_Accommodation']].mean()
    print("The mean values for all columns are:")
    print(mean_all)

    filled_data = df.fillna(mean_all)
    print(filled_data.head(10))

    numeric_cols = filled_data.select_dtypes(include='number').columns

    fig, axes = plt.subplots(1, len(numeric_cols), figsize=(15, 5))
    if len(numeric_cols) == 1:
        axes = [axes]  # Make sure axes is iterable

    for i, col in enumerate(numeric_cols):
        filled_data[col].plot(kind='hist', ax=axes[i], title=f'Histogram of {col}', edgecolor='black')
    
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode('utf-8')


    


