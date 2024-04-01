import binascii
import logging
from datetime import datetime

from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceRequest

from vibraniumdome_shields.shields.model import LLMInteraction
from vibraniumdome_shields.utils import safe_loads_dictionary_string


class OpenTelemetryParser:
    """
    {
        'service.name': 'insurance_classifier_ds',
        'llm.vendor': 'OpenAI',
        'llm.request.type': 'chat',

        'openai.api_base': 'https://api.openai.com/v1',
        'openai.api_type': 'open_ai',

        'llm.request.model': 'gpt-3.5-turbo-0613',
        'llm.response.model': 'gpt-3.5-turbo-0613',
        'llm.temperature': '1',
        'llm.user': 'user-123456J3',
        'llm.headers': "{\'x-session-id\': \'abcd-1234-cdef\'}",

        'llm.prompts.0.role': 'system',
        'llm.prompts.0.content': 'You are a helpful assistant.',
        'llm.prompts.1.role': 'user',
        'llm.prompts.1.content': 'Who won the world series in 2020?',
        'llm.prompts.2.role': 'assistant',
        'llm.prompts.2.content': 'The Los Angeles Dodgers won the World Series in 2020.',
        'llm.prompts.3.role': 'user',
        'llm.prompts.3.content': 'Where was it played?',

        'llm.completions.0.finish_reason': 'stop',
        'llm.completions.0.role': 'assistant',
        'llm.completions.0.content': 'The World Series in 2020 was played in Arlington, Texas at the Globe Life Field,
                                        which is the home stadium of the Texas Rangers.',

        'llm.usage.total_tokens': 82,
        'llm.usage.completion_tokens': 29,
        'llm.usage.prompt_tokens': 53,
        'start_time_unix_nano': 1698944579020656000,
        'end_time_unix_nano': 1698944580615480000,
        'trace_id_hex': 'f5b1b6ad8df2bdfb3d84211fb2549f63'
    }

    {
        'service.name': 'gpt_next',
        'start_timestamp': 1701355459392433000,
        'end_timestamp': 1701355460771553000,
        'id': 'c017a23e1d292ed887acedc6aedd70c0',
        'llm.vendor': 'OpenAI',
        'llm.request.type': 'chat',
        'openai.api_base': 'https://api.openai.com/v1',
        'openai.api_type': 'open_ai',
        'llm.request.model': 'gpt-3.5-turbo-0613',
        'llm.temperature': 0,
        'llm.user': 'user-456789',
        'llm.headers': "{'x-session-id': 'abcd-1234-cdef'}",
        'llm.prompts.0.role': 'assistant',
        'llm.prompts.0.content': 'You are ChatGPT an Artificial Intelligence developed by OpenAI, respond in a concise way, date: 2023/11/30 16:44:19, current location: New York, USA',
        'llm.prompts.1.role': 'user',
        'llm.prompts.1.content': 'whats the weather right now?',
        'llm.request.functions.0.name': 'get_current_weather',
        'llm.request.functions.0.description': 'get weather in location',
        'llm.request.functions.0.parameters': '{"type": "object", "properties": {"location": {"description": "CityName, CountryCode", "type": "string"}}}',
        'llm.response.model': 'gpt-3.5-turbo-0613',
        'llm.completions.0.finish_reason': 'function_call',
        'llm.completions.0.role': 'assistant',
        'llm.completions.0.function_call.name': 'get_current_weather',
        'llm.completions.0.function_call.arguments': '{\n  "location": "New York, USA"\n}',
        'llm.usage.total_tokens': 124,
        'llm.usage.completion_tokens': 19,
        'llm.usage.prompt_tokens': 105
    }
    """

    _logger = logging.getLogger(__name__)

    _datetime_format = "%Y-%m-%dT%H:%M:%S"

    def _bytes_to_hex(self, byte_str):
        return binascii.hexlify(byte_str).decode("utf-8")

    def convert_unix_nano_str_to_iso(self, unix_nano_str):
        try:
            # Convert nanoseconds string to integer
            unix_nano = int(unix_nano_str)

            # Convert nanoseconds to seconds
            unix_seconds = unix_nano / 1e9

            # Convert Unix timestamp to datetime object
            dt_object = datetime.utcfromtimestamp(unix_seconds)

            # Format datetime object in ISO 8601 format
            iso_format = dt_object.strftime(self._datetime_format)

            return iso_format
        except ValueError:
            self._logger.warning("Invalid input. Please provide a valid Unix timestamp in nanoseconds as a string: %s", unix_nano_str)

    def _extract_id_attributes(self, span):
        document = {}
        self._logger.debug("Start Time: %s", span.start_time_unix_nano)
        document["start_timestamp"] = span.start_time_unix_nano
        document["end_timestamp"] = span.end_time_unix_nano
        document["id"] = self._bytes_to_hex(span.trace_id)
        return document

    def _extract_value(self, attribute_kv):
        key = attribute_kv.key
        if attribute_kv.value.HasField("string_value"):
            value = attribute_kv.value.string_value
        elif attribute_kv.value.HasField("bool_value"):
            value = attribute_kv.value.bool_value
        elif attribute_kv.value.HasField("int_value"):
            value = attribute_kv.value.int_value
        elif attribute_kv.value.HasField("double_value"):
            value = attribute_kv.value.double_value
        else:
            value = None
        return key, value

    def _parse_completions(self, llm_interaction: LLMInteraction):
        """
        assistant completion response:
        'llm.completions.0.finish_reason': 'stop',
        funciton call:
        'llm.completions.0.finish_reason': 'function_call',
        'llm.completions.0.role': 'assistant',
        'llm.completions.0.function_call.name': 'get_current_weather',
        'llm.completions.0.function_call.arguments': '{\n  "location": "New York, USA"\n}',
        """
        data = llm_interaction._interaction
        finish_reason = data.get("llm.completions.0.finish_reason", "")
        if "stop" == finish_reason:
            llm_interaction.set_completion(data.get("llm.completions.0.content", ""))
        elif "function_call" == finish_reason:
            llm_interaction.set_function_call_name(data.get("llm.completions.0.function_call.name", ""))

    def _parse_prompts(self, llm_interaction, document):
        prompts = []
        i = 0
        while True:
            role_key = f"llm.prompts.{i}.role"
            content_key = f"llm.prompts.{i}.content"
            if role_key in document and content_key in document:
                prompts.append({"role": document[role_key], "content": document[content_key]})
                i += 1
            else:
                break
        llm_interaction["llm_prompts"] = prompts

    def _parse_functions(self, llm_interaction: dict, document):
        functions = []
        functions_names = []
        i = 0
        while True:
            name = f"llm.request.functions.{i}.name"
            description = f"llm.request.functions.{i}.description"
            parameters = f"llm.request.functions.{i}.parameters"
            if name in document:
                functions.append({"name": document[name], "description": document[description], "parameters": document[parameters]})
                functions_names.append(document[name])
                i += 1
            else:
                break
        llm_interaction["llm.request.functions"] = functions
        llm_interaction["llm.request.function_names"] = functions_names

    def _parse_headers(self, llm_interaction, document):
        llm_interaction["llm.user"] = document.get("llm.user")
        headers_dict = safe_loads_dictionary_string(document.get("llm.headers"))
        # parse all meaningful headers here
        if headers_dict:
            llm_interaction["session-id"] = headers_dict.get("x-session-id")
        return llm_interaction

    def _parse_trace_request(self, export_trace_service_request):
        documents = []
        for resource_span in export_trace_service_request.resource_spans:
            resource_attributes = {}

            for attribute_kv in resource_span.resource.attributes:
                key, value = self._extract_value(attribute_kv)
                resource_attributes[key] = value

            for scope_spans in resource_span.scope_spans:
                for span in scope_spans.spans:
                    document = resource_attributes.copy()
                    document.update(self._extract_id_attributes(span))

                    for attribute_kv in span.attributes:
                        key, value = self._extract_value(attribute_kv)
                        document[key] = value

                    documents.append(document)
                    self._logger.debug("document: %s", document)
        self._logger.debug("number of documents: %d", len(documents))
        return documents

    def parse_llm_call(self, request_data) -> list[LLMInteraction]:
        llm_interactions = []

        export_trace_service_request = ExportTraceServiceRequest()
        export_trace_service_request.ParseFromString(request_data)
        documents = self._parse_trace_request(export_trace_service_request)

        for document in documents:
            llm_interaction = {key: value for key, value in document.items() if not key.startswith("llm.prompts") and not key.startswith("llm.request.functions")}
            # convert timestamp to unix iso 8601 type
            llm_interaction = {key: self.convert_unix_nano_str_to_iso(value) if key.endswith("_timestamp") else value for key, value in llm_interaction.items()}
            llm_interaction["shields_timestamp"] = datetime.now().strftime(self._datetime_format)
            self._parse_headers(llm_interaction, document)
            self._parse_prompts(llm_interaction, document)
            self._parse_functions(llm_interaction, document)
            result = LLMInteraction(llm_interaction)
            self._parse_completions(result)
            self._logger.debug("llm_interaction: %s", llm_interaction)
            llm_interactions.append(result)
        return llm_interactions
