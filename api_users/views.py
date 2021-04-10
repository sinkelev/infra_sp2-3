from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from api_users.models import User
from api_users.permissions import IsSuperUser
from api_users.serializers import UserSerializer
from api_yamdb.settings import EMAIL_HOST_USER


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return JsonResponse(serializer.data)
        if request.method == 'PATCH':
            user = get_object_or_404(User, username=self.request.user)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            return JsonResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = email.split('@')[0]
        user, created = User.objects.get_or_create(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        message = 'Ваш код подтверждения: ' + confirmation_code

        send_mail('Код подтверждения', message,
                  EMAIL_HOST_USER, [email], fail_silently=False)
        return JsonResponse({'email': email})


@api_view(['POST'])
@permission_classes([AllowAny])
def send_token(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = email.split('@')[0]
        user = get_object_or_404(User, username=username)
        confirmation_code = request.POST['confirmation_code']
        refresh = RefreshToken.for_user(user)
        token = refresh.access_token
        flag = default_token_generator.check_token(user, confirmation_code)
        if flag:
            user.save()
            return JsonResponse({'token': str(token)})
        return JsonResponse({'status': False}, status=400)
