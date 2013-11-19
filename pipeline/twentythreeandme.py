
import requests
from genomics.util.genomics_service_locator import GenomicsServiceLocator


def runkeeper_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "twentythreeandme":
        data = kwargs.get('response')
