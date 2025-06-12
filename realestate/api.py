from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .ml_model import price_predictor, rent_predictor
from .models import PredictionHistory
from .serializers import PredictionHistorySerializer
import logging
import io
import matplotlib.pyplot as plt
import base64
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.http import JsonResponse

from datetime import timedelta
from .models import Sale
from django.db.models import Avg, Count
logger = logging.getLogger(__name__)



def generate_price_trend_image(start_date, end_date):
    sales = Sale.objects.filter(date__range=(start_date, end_date))
    if not sales.exists():
        return None
    sales_by_date = sales.values('date').annotate(avg_price=Avg('price')).order_by('date')

    dates = [s['date'] for s in sales_by_date]
    avg_prices = [s['avg_price'] for s in sales_by_date]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, avg_prices, marker='o')
    plt.title('Средняя цена по дате')
    plt.xlabel('Дата')
    plt.ylabel('Средняя цена')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def generate_sales_volume_image(start_date, end_date):
    sales = Sale.objects.filter(date__range=(start_date, end_date))
    sales_by_date = sales.values('date').annotate(sales_volume=Count('id')).order_by('date')

    dates = [s['date'] for s in sales_by_date]
    volumes = [s['sales_volume'] for s in sales_by_date]

    plt.figure(figsize=(8, 4))
    plt.bar(dates, volumes, color='purple')
    plt.title('Объем продаж по дате')
    plt.xlabel('Дата')
    plt.ylabel('Количество продаж')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def generate_popularity_by_region_image(start_date, end_date):
    sales = Sale.objects.filter(date__range=(start_date, end_date))
    popularity_by_region = sales.values('region').annotate(sales_count=Count('id')).order_by('-sales_count')

    regions = [p['region'] for p in popularity_by_region]
    counts = [p['sales_count'] for p in popularity_by_region]

    plt.figure(figsize=(8, 4))
    plt.barh(regions, counts, color='orange')
    plt.title('Популярность районов')
    plt.xlabel('Количество продаж')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def market_trends_api(request):
    end_date_str = request.GET.get('end_date')
    start_date_str = request.GET.get('start_date')

    if end_date_str:
        end_date = parse_date(end_date_str)
    else:
        end_date = timezone.now().date()

    if start_date_str:
        start_date = parse_date(start_date_str)
    else:
        start_date = end_date - timedelta(days=30)

    sales = Sale.objects.filter(date__range=(start_date, end_date))

    if not sales.exists():
        return JsonResponse({'error': 'No data found for given dates'}, status=400)

    price_trend = list(
        sales.values('date').annotate(avg_price=Avg('price')).order_by('date')
    )
    sales_volume = list(
        sales.values('date').annotate(sales_volume=Count('id')).order_by('date')
    )
    popularity_region = list(
        sales.values('region').annotate(sales_count=Count('id')).order_by('-sales_count')
    )

    return JsonResponse({
        'priceTrend': price_trend,
        'salesVolume': sales_volume,
        'popularityRegion': popularity_region,
    })


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class PredictPriceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(f"User making prediction: {user}")
        data = request.data

        try:
            area = float(data.get('sqft', 0))
            bedrooms = int(data.get('bedrooms', 0))
            bathrooms = int(data.get('bathrooms', 0))
            floors = int(data.get('floors', 0))
            has_pool = bool(data.get('has_pool', False))
            property_type = data.get('property_type', 'Apartment')  # translated default
            region = data.get('region', 'Bishkek')  # translated default

            # Validate inputs: no zero values allowed for numeric features
            if any(val == 0 for val in [area, bedrooms, bathrooms, floors]):
                return Response({'error': 'Invalid input, some fields are zero or missing.'}, status=400)
            ALLOWED_PROPERTY_TYPES = ['Apartment', 'House', 'Cottage', 'Villa']
            ALLOWED_REGIONS = ['Bishkek', 'Osh', 'Chuy Region', 'Issyk-Kul Region', 'Batken Region', 'Talas Region',
                               'Jalal-Abad Region']

            if property_type not in ALLOWED_PROPERTY_TYPES:
                return Response({'error': f"Invalid property type: {property_type}"}, status=400)

            if region not in ALLOWED_REGIONS:
                return Response({'error': f"Invalid region: {region}"}, status=400)

            price = price_predictor.predict_price(area, bedrooms, bathrooms, floors, has_pool, property_type, region)
            price_usd = price / 89  # convert from local currency to USD

            # Save the prediction history
            PredictionHistory.objects.create(
                user=user,
                prediction_type='price',
                sqft=area,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                floors=floors,
                has_pool=has_pool,
                property_type=property_type,
                region=region,
                predicted_value=price_usd
            )

            return Response({'price': price_usd}, status=200)

        except Exception as e:
            logger.error(f"PredictPriceView error: {str(e)}")
            return Response({'error': str(e)}, status=400)


class PredictRentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        try:
            area = float(data.get('sqft', 0))
            bedrooms = int(data.get('bedrooms', 0))
            bathrooms = int(data.get('bathrooms', 0))
            floors = int(data.get('floors', 0))
            has_pool = bool(data.get('has_pool', False))
            property_type = data.get('property_type', 'Квартира')
            region = data.get('region', 'Бишкек')

            if any(val == 0 for val in [area, bedrooms, bathrooms, floors]):
                return Response({'error': 'Invalid input, some fields are zero or missing.'}, status=400)

            rent = rent_predictor.predict_rent(area, bedrooms, bathrooms, floors, has_pool, property_type, region)
            rent_usd = rent / 89

            PredictionHistory.objects.create(
                user=user,
                prediction_type='rent',
                sqft=area,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                floors=floors,
                has_pool=has_pool,
                property_type=property_type,
                region=region,
                predicted_value=rent_usd
            )

            return Response({'rent': rent_usd}, status=200)

        except Exception as e:
            logger.error("PredictRentView error: %s", str(e))
            return Response({'error': str(e)}, status=400)



class PredictionGraphDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, prediction_id):
        user = request.user
        try:
            prediction = PredictionHistory.objects.get(id=prediction_id, user=user)
        except PredictionHistory.DoesNotExist:
            return Response({'error': 'Prediction not found'}, status=404)

        # Используем поля из prediction для генерации данных для графика
        area_base = prediction.sqft
        bedrooms = prediction.bedrooms
        bathrooms = prediction.bathrooms
        floors = prediction.floors
        has_pool = prediction.has_pool
        property_type = prediction.property_type
        region = prediction.region
        prediction_type = prediction.prediction_type  # 'price' или 'rent'

        # Генерируем диапазон площадей около area_base, например +-50 м² с шагом 10
        areas = list(range(max(10, int(area_base - 50)), int(area_base + 51), 10))

        from .ml_model.price_predictor import predict_price
        from .ml_model.rent_predictor import predict_rent
        results = []
        for a in areas:
            if prediction_type == 'price':
                predicted_value = predict_price(a, bedrooms, bathrooms, floors, has_pool, property_type, region)
            else:
                predicted_value = predict_rent(a, bedrooms, bathrooms, floors, has_pool, property_type, region)

            results.append({'area': a, 'predicted_value': predicted_value})

        return Response({
            'prediction_id': prediction_id,
            'data': results,
            'prediction_type': prediction_type
        })
class PredictionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            history = PredictionHistory.objects.filter(user=user).order_by('-created_at')
            serializer = PredictionHistorySerializer(history, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            logger.error("PredictionHistoryView error: %s", str(e))
            return Response({'error': str(e)}, status=500)
