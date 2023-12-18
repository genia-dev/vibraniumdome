// update also in prisma/seed.ts
export const defaultPolicy = {
    "id": "-99",
    "name": "Default Policy",
    "content": {
        "shields_filter": "all",
        "high_risk_threshold": 0.8,
        "low_risk_threshold": 0.2,
        "input_shields": [
            {"type": "com.vibraniumdome.shield.input.semantic_similarity", "metadata": {}},
            {"type": "com.vibraniumdome.shield.input.regex", "metadata": {}, "name": "policy number"},
            {"type": "com.vibraniumdome.shield.input.captain", "metadata": {"model": "gpt-3.5-turbo", "model_vendor": "openai"}},
            {"type": "com.vibraniumdome.shield.input.transformer", "metadata": {}},
            {"type": "com.vibraniumdome.shield.input.prompt_safety", "metadata": {}},
            {"type": "com.vibraniumdome.shield.input.sensitive_info_disc", "metadata": {}},
            {"type": "com.vibraniumdome.shield.input.model_dos", "metadata": {"threshold": 10, "interval_sec": 60, "limit_by": "llm.user"}},
        ],
        "output_shields": [
            {"type": "com.vibraniumdome.shield.output.regex", "metadata": {}, "name": "credit card"},
            {"type": "com.vibraniumdome.shield.output.refusal", "metadata": {}},
            {"type": "com.vibraniumdome.shield.output.refusal.canary_token_disc", "metadata": {"canary_tokens": []}},
            {"type": "com.vibraniumdome.shield.output.sensitive_info_disc", "metadata": {}},
        ],
    },
}