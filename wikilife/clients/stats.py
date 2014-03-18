# coding=utf-8

from wikilife.clients.base_wikilife_client import BaseWikilifeClient


class Stats(BaseWikilifeClient):

    def get_global_education_stats(self):
        response_dto = self.rest_get("/4/stats/global/education/level/")[2]
        return response_dto

    def get_global_work_stats(self):
        response_dto = self.rest_get("/4/stats/global/work/experience/")[2]
        return response_dto

    def get_global_social_stats(self):
        response_dto = self.rest_get("/4/stats/global/social/")[2]
        return response_dto

    def get_global_physical_activity(self, node_id):
        response_dto = self.rest_get("/4/stats/global/physical/activity/tpw/"+str(node_id))[2]
        return response_dto

    def get_global_physical_distribution_last_week(self, node_id):
        response_dto = self.rest_get("/4/stats/global/physical/distribution/last_week/"+str(node_id))[2]
        return response_dto
    
    def get_global_complaints(self):
        response_dto = self.rest_get("/4/stats/global/health/complaints/mostpopular")[2]
        return response_dto

    def get_global_conditions(self):
        response_dto = self.rest_get("/4/stats/global/health/conditions/mostpopular")[2]
        return response_dto 

    def get_global_emotions(self):
        response_dto = self.rest_get("/4/stats/global/psychological/moods/mostpopular")[2]
        return response_dto 
