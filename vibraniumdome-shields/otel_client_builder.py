import os
import logging
import secrets

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

vibranium_dome_api_key = os.getenv('VIBRANIUM_DOME_API_KEY')
if vibranium_dome_api_key is None:
    raise ValueError("VIBRANIUM_DOME_API_KEY environment variable is not set")

headers = {"Authorization": f"Bearer {vibranium_dome_api_key}"}
trace.set_tracer_provider(TracerProvider())
vibranium_dome_base_url = os.environ["VIBRANIUM_DOME_BASE_URL"] or "http://localhost:5001"
otlp_exporter = OTLPSpanExporter(endpoint=vibranium_dome_base_url + "/v1/traces", headers=headers)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

class OpenTelemetryBuilder:
    """
    Build an Otel span and sends it to vibranium_dome_base_url

    an example of a simple open ai conversation:

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

    another example of an open ai conversation including function calling:

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

    def __init__(self):
        self.span_processor = span_processor
        self.tracer = trace.get_tracer(__name__)

    def _count_token(self, string):
        # Split the string into words based on whitespace
        words = string.split()
        # Return the number of words
        return round(0.75*len(words))

    def build_simple_qa(self, model, system_message, user_message, assistant_message, temperature='0', user_id='user-123456J3', session_id='abcd-1234-cdef'):
        with self.tracer.start_as_current_span("Default") as span:
            span.set_attribute('service.name', 'Default')
            span.set_attribute('llm.vendor', 'OpenAI')
            span.set_attribute('llm.request.type', 'chat')
            span.set_attribute('openai.api_base', 'https://api.openai.com/v1')
            span.set_attribute('openai.api_type', 'open_ai')
            span.set_attribute('llm.request.model', model)
            span.set_attribute('llm.response.model', model)
            span.set_attribute('llm.temperature', temperature)
            span.set_attribute('llm.user', user_id)
            span.set_attribute('llm.headers', "{'x-session-id': "+session_id+"}")
            # conversation below
            span.set_attribute('llm.prompts.0.role', 'system')
            span.set_attribute('llm.prompts.0.content', system_message)
            span.set_attribute('llm.prompts.1.role', 'user')
            span.set_attribute('llm.prompts.1.content', user_message)
            span.set_attribute('llm.completions.0.finish_reason', 'stop')
            span.set_attribute('llm.completions.0.role', 'assistant')
            span.set_attribute('llm.completions.0.content', assistant_message)

            prompt_tkn = self._count_token(system_message) + self._count_token(user_message)
            span.set_attribute('llm.usage.prompt_tokens', prompt_tkn)

            asst_tkn = self._count_token(assistant_message)
            span.set_attribute('llm.usage.total_tokens', asst_tkn)
            span.set_attribute('llm.usage.completion_tokens', prompt_tkn + asst_tkn)

            # setting a custom trace_id (hexadecimal string) i.e 'f5b1b6ad8df2bdfb3d84211fb2549f63'
            span.set_attribute('trace_id_hex', ''.join(secrets.choice('0123456789abcdef') for _ in range(32)))

            # For demonstration, setting custom start and end times (Unix nanoseconds)
            # Usually, OpenTelemetry manages these timestamps automatically
            #start_time = 1698944579020656000
            #end_time = 1698944580615480000
            #span.set_start_time(time.time_ns())
            #time.sleep(1)  # Simulate span duration
            #span.set_end_time(time.time_ns())

        self.span_processor.force_flush()

    def build_advanced_qa(self, model, system_message, user_message, assistant_message, attributes_dict, temperature='0', user_id='user-123456J3', session_id='abcd-1234-cdef'):
        """
            pass the conversation and additional attributes as a dictionary for more advanced scenarios
            for example:

            span.set_attribute('llm.prompts.0.role', 'system')
            span.set_attribute('llm.prompts.0.content', "system context")
            span.set_attribute('llm.prompts.1.role', 'user')
            span.set_attribute('llm.prompts.1.content', "user message")
            ...
            span.set_attribute('llm.completions.0.finish_reason', 'stop')
            span.set_attribute('llm.completions.0.role', 'assistant')
            span.set_attribute('llm.completions.0.content', "assistant message")
            span.set_attribute('llm.usage.prompt_tokens', 1000)
            span.set_attribute('llm.usage.total_tokens', 100)
            span.set_attribute('llm.usage.completion_tokens', 1000 + 100)
        """
        with self.tracer.start_as_current_span("Default") as span:
            span.set_attribute('service.name', 'Default')
            span.set_attribute('llm.vendor', 'OpenAI')
            span.set_attribute('llm.request.type', 'chat')
            span.set_attribute('openai.api_base', 'https://api.openai.com/v1')
            span.set_attribute('openai.api_type', 'open_ai')
            span.set_attribute('llm.request.model', model)
            span.set_attribute('llm.response.model', model)
            span.set_attribute('llm.temperature', temperature)
            span.set_attribute('llm.user', user_id)
            span.set_attribute('llm.headers', "{'x-session-id': "+session_id+"}")
            # setting a custom trace_id (hexadecimal string) i.e 'f5b1b6ad8df2bdfb3d84211fb2549f63'
            span.set_attribute('trace_id_hex', ''.join(secrets.choice('0123456789abcdef') for _ in range(32)))
            for key, value in attributes_dict.items():
                span.set_attribute(key, value)

        self.span_processor.force_flush()
