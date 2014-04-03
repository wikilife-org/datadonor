# coding=utf-8


SERVICES = {
    "runkeeper": "physical.services.runkeeper_service.RunkeeperService",
    "bodymedia": "physical.services.bodymedia_service.BodymediaService",
    "fitbit": "physical.services.fitbit_service.FitbitService"
}


class PhysicalServiceBuilderException(Exception):
    pass


class PhysicalServiceBuilder(object):

    _wl_srv_bldr = None

    def __init__(self, wl_srv_bldr):
        self._wl_srv_bldr = wl_srv_bldr

    def build_service_by_name(self, service_name):
        user_client = self._wl_srv_bldr.build_user_client()
        logs_client = self._wl_srv_bldr.build_logs_client()
        stats_client = self._wl_srv_bldr.build_stats_client()

        if not service_name in SERVICES:
            raise PhysicalServiceBuilderException("Unknow service name '%s'" %service_name)

        class_fullname = SERVICES[service_name] 
        clazz = self._get_class(class_fullname)
        service = clazz(user_client, logs_client, stats_client)
        return service

    def _get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )

        for comp in parts[1:]:
            m = getattr(m, comp)

        return m
