from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AgentApplication
from .serializers import AgentApplicationSerializer, AgentApplicationSerializer
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import AgencyCompany, Advantage, Review
from .serializers import AgencySerializer, AdvantageSerializer, ReviewSerializer
class AgencyListView(generics.ListAPIView):
    queryset = AgencyCompany.objects.all()
    serializer_class = AgencySerializer

class AdvantageListView(generics.ListAPIView):
    queryset = Advantage.objects.all()
    serializer_class = AdvantageSerializer

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ApplyAgentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, 'agentapplication'):
            return Response({"detail": "Вы уже подали заявку."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AgentApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"detail": "Заявка успешно отправлена."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgentStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        app = getattr(request.user, 'agentapplication', None)
        if not app:
            return Response({"detail": "Вы не подавали заявку."}, status=404)
        serializer = AgentApplicationSerializer(app)
        return Response(serializer.data)

class AdminAgentApplicationsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        apps = AgentApplication.objects.filter(status='pending')
        serializer = AgentApplicationSerializer(apps, many=True)
        return Response(serializer.data)

class ApproveAgentApplicationView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        app = get_object_or_404(AgentApplication, pk=pk)
        app.status = 'approved'
        app.save()
        app.user.is_agent = True
        app.user.save()
        return Response({"detail": "Заявка одобрена."})

class RejectAgentApplicationView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        app = get_object_or_404(AgentApplication, pk=pk)
        app.status = 'rejected'
        app.save()
        return Response({"detail": "Заявка отклонена."})
