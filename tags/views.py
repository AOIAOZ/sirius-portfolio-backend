from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Tag
from .serializers import TagSerializer


class TagListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [(IsAdminUser())]

    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        tags = serializer.validated_data

        return Response({
            'tags': tags,
            'count': len(tags)
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()

        limit = request.query_params.get('limit', '10')   # ?limit=20
        if not limit.isdigit():
            limit = 10
        limit = int(limit)

        offset = request.query_params.get('offset', '0')    # ?offset=5
        if not offset.isdigit():
            offset = 0
        offset = int(offset)

        tags = tags[offset:offset + limit]

        serializer = TagSerializer(tags, many=True)
        return Response({
            'tags': serializer.data,
            'count': tags.count(),
            'limit': limit,
            'offset': offset
        })

    def delete(self, request, *args, **kwargs):
        values = request.data.get('values', [])
        if not values:
            return Response(
                {'error': 'At least one value must be provided in "values" array'},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_count = Tag.objects.filter(value__in=values).delete()[0]

        return Response({
            'message': f'Successfully deleted {deleted_count} tag(s)',
            'deleted_count': deleted_count,
            'values': values
        }, status=status.HTTP_200_OK)
