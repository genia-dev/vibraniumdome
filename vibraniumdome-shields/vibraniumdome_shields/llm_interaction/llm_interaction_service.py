import json
import logging

from opensearchpy import OpenSearch

from vibraniumdome_shields.settings_loader import settings
from vibraniumdome_shields.shields.model import LLMInteraction
from vibraniumdome_shields.utils import pydantic_json_encoder


class LLMInteractionService:
    _logger = logging.getLogger(__name__)
    _host: str
    _port: str
    _index_name: str
    _auth = ("admin", "admin")
    _repository: OpenSearch

    def __init__(self):
        self._host = settings.get("VIBRANIUM_DOME_OPENSEARCH_HOST", "localhost")
        self._port = settings.get("VIBRANIUM_DOME_OPENSEARCH_PORT", "9200")
        self._index_name = settings.get("VIBRANIUM_DOME_OPENSEARCH_INTERACTIONS_INDEX", "vibranium_index")
        self._repository = OpenSearch(
            hosts=[{"host": self._host, "port": self._port}],
            http_auth=self._auth,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

    def save_llm_interaction(self, llm_interaction: LLMInteraction):
        # json_data = model_instance.json()
        document = llm_interaction._interaction
        scan_id = str(llm_interaction._shields_result.scan_id)
        document["risk"] = llm_interaction._shields_result.risk.value
        document["scan_id"] = scan_id
        document["risk_factor"] = llm_interaction._shields_result.risk_factor
        document["shields_result"] = json.dumps(llm_interaction._shields_result.results, default=pydantic_json_encoder)
        document["last_prompt"] = llm_interaction.get_last_user_message()
        document["completion"] = llm_interaction.get_chat_completion()

        response = self._repository.index(index=self._index_name, body=document, id=scan_id, refresh=True)
        self._logger.info(response)
