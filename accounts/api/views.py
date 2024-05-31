from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from accounts.models import OneTimePassword
from .serializers import (JobSeekerRegisterSerializer,
                          EmployerRegisterSerializer,
                          VerifySerializer,
                          JobSeekerLoginSerializer,
                          EmployerLoginSerializer,
                          LogoutUserSerializer,
                          ForgotPasswordRequestSerializer,
                          SetNewPasswordSerializer,
                          ChangePasswordSerializer)
from accounts.utils import send_otp_code

from django.contrib.auth import get_user_model
User = get_user_model()


class JobSeekerRegisterAPIView(GenericAPIView):
    serializer_class = JobSeekerRegisterSerializer

    def post(self, request):
        user = request.data
        serializer=self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data=serializer.data
            return Response({
                'data':user_data,
                'message':'You registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerRegisterAPIView(GenericAPIView):
    serializer_class = EmployerRegisterSerializer

    def post(self, request):
        user = request.data
        serializer=self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data=serializer.data
            send_otp_code(user_data['phone_number'], request)
            return Response({
                'data':user_data,
                'message':'thanks for signing up a passcode has be sent to verify your phone number'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmployerPhoneNumber(GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request):
        try:
            passcode = request.data.get('otp')
            user_pass_obj=OneTimePassword.objects.get(otp=passcode)
            user=user_pass_obj.user
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({
                    'message':'account phone_number verified successfully'}, status=status.HTTP_200_OK)
            return Response({'error':'passcode is invalid user is already verified'}, status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({'errot':'passcode not provided'}, status=status.HTTP_400_BAD_REQUEST)


class JobSeekerLoginAPIView(GenericAPIView):
    serializer_class = JobSeekerLoginSerializer
  
    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployerLoginAPIView(GenericAPIView):
    serializer_class = EmployerLoginSerializer
  
    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    

class LogoutAPIView(GenericAPIView):
    serializer_class=LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'You logged out'}, status=status.HTTP_204_NO_CONTENT)


class ForgotPasswordRequestAPIView(GenericAPIView):
    serializer_class = ForgotPasswordRequestSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)
    

class PasswordResetConfirmAPIView(GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'credentials is valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':"password reset is successfully"}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            if not user.check_password(validated_data.get('current_password')):
                return Response({'error':'Current password is not correct'}, status=status.HTTP_400_BAD_REQUEST)
            elif user.check_password(validated_data.get('new_password')):
                return Response({'error':'You must set a new password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(validated_data.get('new_password'))
            user.save()
            return Response({'message':'password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
