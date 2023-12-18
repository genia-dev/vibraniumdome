import concurrent.futures
import logging
import os
import tempfile

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request
from marshmallow import Schema, fields
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceResponse

from vibraniumdome_shields.llm_interaction.llm_interaction_service import LLMInteractionService
from vibraniumdome_shields.open_telemetry.open_telemetry_parser import OpenTelemetryParser
from vibraniumdome_shields.policies.policy_service import PolicyService
from vibraniumdome_shields.settings_loader import settings
from vibraniumdome_shields.shields.model import LLMInteraction
from vibraniumdome_shields.shields.vibranium_shields_service import CaptainLLM, VibraniumShieldsFactory
from vibraniumdome_shields.user_interface.cli_app import main
from vibraniumdome_shields.vector_db.vector_db_service import VectorDBService

load_dotenv()

app = Flask(__name__)

# Configure logging levels
logging.basicConfig(level=settings.logger_level.DEFAULT_LOGGING_LEVEL)
for logger_name, log_level in settings.logger_level.to_dict().items():
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)


class ScanInputSchema(Schema):
    llm_session = fields.String(required=True)


scan_input_schema = ScanInputSchema()

vector_db_service = VectorDBService(
    settings.get("vector_db.vector_db_dir", tempfile.gettempdir()),
    settings.get("vector_db.collection_name"),
    settings.get("vector_db.embedding_model_name"),
    # settings.get("OPENAI_API_KEY"),
)
captain_llm = CaptainLLM(VibraniumShieldsFactory(vector_db_service))
policy_service = PolicyService()
parser = OpenTelemetryParser()
interaction_service = LLMInteractionService()


@app.route("/api/health", methods=["GET"])
def api():
    return jsonify({"status": "OK"}), 200


@app.route("/api/vector/reload", methods=["POST", "GET"])
def vector_reload():
    try:
        vector_db_service.load_external_data()
    except Exception as e:
        return jsonify({"errors": e.messages}), 400

    return jsonify({"response": "Done"}), 200


@app.route("/api/scan", methods=["POST"])
def scan():
    data = request.json
    try:
        validated_data = scan_input_schema.load(data)
    except Exception as e:
        return jsonify({"errors": e.messages}), 400

    response = captain_llm.deflect_shields(validated_data["llm_session"])
    return jsonify({"response": response.model_dump()})


@app.route("/v1/traces", methods=["POST"])
def receive_traces():
    llm_interaction: LLMInteraction = parser.parse_llm_call(request.data)
    executor = concurrent.futures.ThreadPoolExecutor()
    def process_traces(llm_interaction: LLMInteraction):
        try:
            # policy = policy_service.get_default_policy()
            policy = policy_service.get_policy_by_name(llm_interaction._interaction.get("service_name", "default"))
            llm_interaction._shields_result = captain_llm.deflect_shields(llm_interaction, policy)
            interaction_service.save_llm_interaction(llm_interaction)
        except Exception:
            logger.exception("error while deflecting shields for interaction= %s with policy= %s", llm_interaction, policy)

    executor.submit(process_traces, llm_interaction)

    return Response(ExportTraceServiceResponse().SerializeToString(), mimetype="application/octet-stream")


def server():
    host = "0.0.0.0"
    port = 5001

    logging.info("starting server listening at host: %s with port: %s", host, port)
    app.run(debug=os.environ.get("PYTHON_ENV") == "development", host=host, port=5001)


def cli():
    main()


if __name__ == "__main__":
    if settings.vibraniumdome_shields.app == "cli":
        cli()
    elif settings.vibraniumdome_shields.app == "server":
        server()
