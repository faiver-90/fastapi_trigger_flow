from src.modules.api_source.api.v1.user_trigger_bindings.user_trigger_binding_repo import UserTriggerBindingRepo
from src.modules.api_source.api.v1.user_trigger_bindings.user_trigger_binding_service import \
    CRUDUserTriggerBindingService
from src.shared.services.base_get_service import base_get_service


get_user_trigger_binding_service = base_get_service(CRUDUserTriggerBindingService, UserTriggerBindingRepo)
