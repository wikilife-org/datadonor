# coding=utf-8

from physical.models import GlobalPhysicalActivity, RUNNING_WL_ACT_ID, \
    WALKING_WL_ACT_ID, ELLIPTICAL_WL_ACT_ID, GlobalDistributionLastWeek, \
    STEPS_ACT_CODE, MILES_ACT_CODE, HOURS_ACT_CODE
from wikilife.base_sync import BaseSync


class PhysicalSync(BaseSync):

    _stat_client = None

    def __init__(self, stat_client):
        self._stat_client = stat_client

    def sync(self):
        self._pull_from_devices()
        self._pull_globals_from_wl()

    def _pull_from_devices(self):
        """        
        date_from = None
        date_to = None
        
        for user in users:
            
            for device in user_devices:
                device_service.pull_user_activity(user_id, user_auth)
                
            pull user physical aggregated activity data from WL
        """        

    def _pull_globals_from_wl(self):

        running = GlobalPhysicalActivity.objects.get(act_wl_id=RUNNING_WL_ACT_ID)
        running.tpw = self._stats_client.get_global_physical_activity(running.act_wl_id)
        running.save()

        walking = GlobalPhysicalActivity.objects.get(act_wl_id=WALKING_WL_ACT_ID)
        walking.tpw = self._stats_client.get_global_physical_activity(walking.act_wl_id)
        walking.save()

        elliptical = GlobalPhysicalActivity.objects.get(act_wl_id=ELLIPTICAL_WL_ACT_ID)
        elliptical.tpw = self._stats_client.get_global_physical_activity(elliptical.act_wl_id)
        elliptical.save()

        steps = GlobalDistributionLastWeek.objects.get(act_code=STEPS_ACT_CODE)
        r = self._stat_client.get_global_physical_distribution_last_week(node_id)
        steps.sun = r.sum
        steps.mon = r.mon
        steps.tue = r.tue
        steps.wed = r.wed
        steps.thu = r.thu
        steps.fri = r.fri
        steps.sat = r.sat
        steps.avg = r.avg
        steps.save()
        
        miles =  GlobalDistributionLastWeek.objects.get(act_code=MILES_ACT_CODE)
        r = self._stat_client.get_global_physical_distribution_last_week(node_id)
        miles.sun = r.sum
        miles.mon = r.mon
        miles.tue = r.tue
        miles.wed = r.wed
        miles.thu = r.thu
        miles.fri = r.fri
        miles.sat = r.sat
        miles.avg = r.avg
        miles.save()
        
        hours =  GlobalDistributionLastWeek.objects.get(act_code=HOURS_ACT_CODE)
        r = self._stat_client.get_global_physical_distribution_last_week(node_id)
        hours.sun = r.sum
        hours.mon = r.mon
        hours.tue = r.tue
        hours.wed = r.wed
        hours.thu = r.thu
        hours.fri = r.fri
        hours.sat = r.sat
        hours.avg = r.avg
        hours.save()
