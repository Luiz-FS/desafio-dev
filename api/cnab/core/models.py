import uuid
from django.db import models
from core.enumerators import TransactionType, FileStatus


type_choices = list(map(lambda type: (type.value, type.name), TransactionType.__members__.values()))
status_choices = list(map(lambda status: (status.value, status.name), FileStatus.__members__.values()))


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class CNABDocumentation(BaseModel):
    type = models.IntegerField(choices=type_choices, null=False)
    date = models.DateTimeField(null=False)
    value = models.IntegerField(null=False)
    cpf = models.CharField(max_length=11, null=False)
    card = models.CharField(max_length=12, null=False)
    store_owner = models.CharField(max_length=14, null=False)
    store_name = models.CharField(max_length=19, null=False)


class Store(BaseModel):
    name = models.CharField(max_length=19, null=False, unique=True)
    owner = models.CharField(max_length=14, null=False)
    balance = models.IntegerField(null=False, default=0)


class File(BaseModel):
    filepath = models.TextField(null=False)
    status = models.IntegerField(choices=status_choices, null=False, default=FileStatus.PENDING.value)
