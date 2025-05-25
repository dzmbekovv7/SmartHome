from django.urls import path
from .api import PredictPriceView, PredictRentView, PredictionHistoryView, market_trends_api,PredictionGraphDataView

urlpatterns = [
    path('predict/price/', PredictPriceView.as_view(), name='predict-price'),
    path('predict/rent/', PredictRentView.as_view(), name='predict-rent'),
    path('predict/history/', PredictionHistoryView.as_view(), name='prediction-history'),
    path('market-trends/', market_trends_api, name='market-trends-api'),
    path('predict/history/<int:prediction_id>/graph/', PredictionGraphDataView.as_view(), name='prediction-graph-data'),

]
