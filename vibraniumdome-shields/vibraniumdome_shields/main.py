import concurrent.futures
import logging
import os
import tempfile
import time

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request, make_response
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

from vibraniumdome_shields.utils import check_api_token

from prometheus_client import multiprocess
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, Counter, Histogram

load_dotenv()

app = Flask(__name__)

number_of_requests = Counter(
    'number_of_requests',
    'The number of requests, its a counter so the value can increase or reset to zero.'
)

llm_processing_seconds_histogram = Histogram('llm_processing_seconds', 'Time for processing the LLM interaction',
                                   buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

llm_saving_seconds_histogram = Histogram('llm_saving_seconds', 'Time for saving the processed LLM interaction to opensearch',
                                    buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

llm_interaction_total_seconds_histogram = Histogram('llm_interaction_total_seconds', 'Time for total handling LLM interaction',
                                    buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, float('inf')])

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


@app.route('/metrics', methods=['GET'])
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(data, content_type='text/plain')

@app.route("/api/health", methods=["GET"])
def api():
    return jsonify({"status": "OK"}), 200


@app.route("/api/vector/reload", methods=["POST", "GET"])
def vector_reload():
    try:
        vector_db_service.init_vector_store()
    except Exception as e:
        return jsonify({"errors": e.messages}), 400

    return jsonify({"response": "Done"}), 200


@app.route("/v1/scan", methods=["POST"])
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
    try:
        vibranium_dome_base_url = settings.get("VIBRANIUM_DOME_APP_BASE_URL", "http://localhost:3000")
        auth_header = request.headers.get('Authorization')
    
        if not auth_header:
            return make_response('Unauthorized Access', 401)
        
        token_type, vibranium_dome_api_key = auth_header.split()
        if token_type.lower() != 'bearer':
            return make_response('Unauthorized Access', 401)
        
        if not check_api_token(vibranium_dome_base_url, vibranium_dome_api_key):
            logger.warning("got an invalid API key")
            return make_response('Unauthorized Access', 401)
    except Exception:
        return make_response('Unauthorized Access', 401)
    
    number_of_requests.inc()
    llm_interactions: list(LLMInteraction) = parser.parse_llm_call(request.data)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1000, thread_name_prefix="traces")

    def process_traces(llm_interaction: LLMInteraction):
        try:
            start_time_total = time.time()

            policy = policy_service.get_policy_by_name(llm_interaction._interaction.get("service.name", "default"))
            
            start_time = time.time()
            llm_interaction._shields_result = captain_llm.deflect_shields(llm_interaction, policy)
            end_time = time.time() - start_time
            llm_processing_seconds_histogram.observe(end_time)

            shield_names = policy_service.get_shields_names()

            start_time = time.time()
            interaction_service.save_llm_interaction(llm_interaction, policy, shield_names)
            end_time = time.time() - start_time
            llm_saving_seconds_histogram.observe(end_time)
            
            end_time_total = time.time() - start_time_total
            llm_interaction_total_seconds_histogram.observe(end_time_total)
        except Exception:
            logger.exception("error while deflecting shields for interaction= %s with policy= %s", llm_interaction, policy)

    for llm_interaction in llm_interactions:
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
