from src.modules.api_source.api.v1.trigger.trigger_repo import TriggerRepo
from src.modules.api_source.api.v1.trigger.trigger_service import CRUDTriggerService
from src.shared.services.base_get_service import base_get_service

get_trigger_service = base_get_service(CRUDTriggerService, TriggerRepo)
