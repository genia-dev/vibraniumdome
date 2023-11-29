import logging
from typing import List, Optional, Tuple
from uuid import UUID

from langchain.docstore.document import Document

from vibraniumdome_shields.shields.model import LLMInteraction, ShieldMatch, VibraniumShield
from vibraniumdome_shields.vector_db.vector_db_service import VectorDBService


class VectorDBShieldMatch(ShieldMatch):
    text: str = ""
    metadata: Optional[dict] = {}
    distance: float = 0.0


class VectorDBShield(VibraniumShield):
    logger = logging.getLogger(__name__)
    _shield_name: str = "vector_db_shield"
    _vector_db_service: VectorDBService

    def __init__(self, vector_db_service: VectorDBService):
        super().__init__(self._shield_name)
        self._vector_db_service = vector_db_service

    def deflect(self, llm_interaction: LLMInteraction, shield_policy_config: dict, scan_id: UUID, policy: dict) -> List[ShieldMatch]:
        threshold = shield_policy_config.get("threshold", 0.4)
        llm_message = llm_interaction.get_last_user_message()

        shield_matches = []
        try:
            matches: List[Tuple[Document, float]] = self._vector_db_service.query(llm_message)
            existing_texts: set = set()

            for match in matches:
                distance = match[1]
                text = match[0].page_content
                if distance < threshold and text not in existing_texts:
                    # with vector db a lower distance means higher vectors cosine similarity
                    shield_matches.append(VectorDBShieldMatch(text=text, metadata=match[0].metadata, distance=distance, risk=1))
                    # TODO: extract this logic to another strategy elsewhere
                    existing_texts.add(text)
        except Exception as err:
            self.logger.exception("Failed to perform vector shield, scan_id=%d", scan_id)
            raise err
        return shield_matches
