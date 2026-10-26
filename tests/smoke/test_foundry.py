"""Smoke-test the user's existing Microsoft Foundry Responses deployment.

Prerequisites: pip install -r requirements.txt ; az login
Run: python scripts/test_foundry.py
"""
import os
import pytest
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

@pytest.mark.skipif(os.getenv("RUN_AZURE_SMOKE") != "1", reason="Requires Azure login and opt-in")
def test_foundry_inference():
    endpoint = os.getenv(
        "AZURE_FOUNDRY_ENDPOINT",
        "https://ai-foundry-emh.services.ai.azure.com/openai/v1",
    )
    deployment = os.getenv("AZURE_FOUNDRY_DEPLOYMENT", "gpt-5.6-sol")
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default",
    )
    client = OpenAI(base_url=endpoint, api_key=token_provider, timeout=30.0, max_retries=1)
    response = client.responses.create(
        model=deployment,
        input="In one sentence, explain how AI can help process fictional HR documents.",
    )
    assert response.output_text.strip()
