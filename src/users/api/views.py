from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from users.models import Profile
from .serializers import ProfileSerializer
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response

ensure_csrf = method_decorator(ensure_csrf_cookie)

class SetCSRFCookie(APIView):
    permission_classes = []
    authentication_classes = []

    @ensure_csrf
    def get(self, request):
        return Response("CSRF Cookie set")




class ProfileEditView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        object = self.queryset.filter(user=self.request.user).first()
        return object
    
    # def update(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     validated_data = serializer.validated_data
        