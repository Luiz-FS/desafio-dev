from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from cnab.settings import PROCESS_AREA
from core import models, serializers
from core.utils import send_to_worker

class FileAPIView(generics.ListCreateAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def create(self, request, *args, **kwargs):
        """
        Method to read the file received by the request, save
        to the shared volume and send message to the worker queue.

        Parameters
        ----------
        request : rest_framework.request.Request
            Request object

        Returns
        -------
        rest_framework.response.Response
            api response object
        """
        file = request.stream.FILES.get("file")

        if not file:
            return Response(
                data={"msg": "The file field is required!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        local_filepath = f"{PROCESS_AREA}/{file.name}"
        file_obj = models.File.objects.create(filepath=file.name)

        with open(local_filepath, 'wb') as f:
            f.write(file.read())

        send_to_worker(data={
            "file_id": str(file_obj.id),
            "filepath": file_obj.filepath
        })

        return Response(data={}, status=status.HTTP_201_CREATED)


class CNABDocumentationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.CNABDocumentation.objects.all()
    serializer_class = serializers.CNABDocumentationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'



class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
