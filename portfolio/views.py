import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import StudentProfileSerializer, DocumentSerializer
from ml.main import recognize


class MyProfileView(generics.RetrieveUpdateAPIView):
    """
    Получение и обновление профиля ТЕКУЩЕГО пользователя.
    """
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.studentprofile


class DocumentUploadView(APIView):
    """
    Эндпоинт для загрузки документов.
    Принимает POST-запросы с multipart/form-data.
    Может опционально распознавать текст в файле.
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        document = serializer.save()

        response_data = serializer.data

        should_recognize = request.query_params.get('recognize', 'false').lower() == 'true' or \
                           request.data.get('recognize', 'false').lower() == 'true'

        if should_recognize:
            try:
                document.file.open('rb')
                image_bytes = document.file.read()
                document.file.close()

                recognized_text = asyncio.run(recognize(image_bytes=image_bytes))

                if recognized_text:
                    document.recognized_text = recognized_text
                    document.save()
                    response_data['recognized_text'] = recognized_text
                else:
                    response_data['recognition_error'] = "ML-сервис не смог обработать запрос."

            except Exception as e:
                error_message = f"Ошибка во время распознавания: {e}"
                print(error_message)
                response_data['recognition_error'] = "Произошла ошибка при вызове сервиса распознавания."

        return Response(response_data, status=status.HTTP_201_CREATED)
