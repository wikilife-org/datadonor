# coding=utf-8

from genomics.util.genomics_service_locator import GenomicsServiceLocator


def twentythreeandme_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "twentythreeandme":
        data = kwargs.get('response')
        dd_user_id = social_user.user.id
        twentythreeandme_service = GenomicsServiceLocator.get_instane().build_service_by_name("twentythreeandme")
        twentythreeandme_service.pull_user_info(dd_user_id, {"access_token": data["access_token"]})