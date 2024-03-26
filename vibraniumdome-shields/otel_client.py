import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

vibranium_dome_api_key = os.getenv('VIBRANIUM_DOME_API_KEY')

if vibranium_dome_api_key is None:
    raise ValueError("VIBRANIUM_DOME_API_KEY environment variable is not set")

headers = {"Authorization": f"Bearer {vibranium_dome_api_key}"}

trace.set_tracer_provider(TracerProvider())
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:5001/v1/traces", headers=headers)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Get a tracer
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("Default") as span:
    span.set_attribute('service.name', 'Default')
    span.set_attribute('llm.vendor', 'OpenAI')
    span.set_attribute('llm.request.type', 'chat')
    span.set_attribute('openai.api_base', 'https://api.openai.com/v1')
    span.set_attribute('openai.api_type', 'open_ai')
    span.set_attribute('llm.request.model', 'gpt-3.5-turbo-0613')
    span.set_attribute('llm.response.model', 'gpt-3.5-turbo-0613')
    span.set_attribute('llm.temperature', '1')
    span.set_attribute('llm.user', 'user-123456J3')
    span.set_attribute('llm.headers', "{'x-session-id': 'abcd-1234-cdef'}")
    span.set_attribute('llm.prompts.0.role', 'system')
    span.set_attribute('llm.prompts.0.content', 'You are a helpful assistant.')
    span.set_attribute('llm.prompts.1.role', 'user')
    span.set_attribute('llm.prompts.1.content', 'Who won the world series in 2020?')
    span.set_attribute('llm.prompts.2.role', 'assistant')
    span.set_attribute('llm.prompts.2.content', 'The Los Angeles Dodgers won the World Series in 2020.')
    span.set_attribute('llm.prompts.3.role', 'user')
    span.set_attribute('llm.prompts.3.content', 'Where was it played?')
    span.set_attribute('llm.completions.0.finish_reason', 'stop')
    span.set_attribute('llm.completions.0.role', 'assistant')
    span.set_attribute('llm.completions.0.content', 'The World Series in 2020 was played in Arlington, Texas at the Globe Life Field, which is the home stadium of the Texas Rangers.')
    span.set_attribute('llm.usage.total_tokens', 82)
    span.set_attribute('llm.usage.completion_tokens', 29)
    span.set_attribute('llm.usage.prompt_tokens', 53)

    # For demonstration, setting custom start and end times (Unix nanoseconds)
    # Usually, OpenTelemetry manages these timestamps automatically
    #start_time = 1698944579020656000
    #end_time = 1698944580615480000
    #span.set_start_time(time.time_ns())
    #time.sleep(1)  # Simulate span duration
    #span.set_end_time(time.time_ns())

    # Setting a custom trace_id (hexadecimal string)
    span.set_attribute('trace_id_hex', 'f5b1b6ad8df2bdfb3d84211fb2549f63')
span_processor.force_flush()