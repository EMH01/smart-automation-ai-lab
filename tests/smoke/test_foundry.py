"""Opt-in smoke test of a configured Microsoft Foundry deployment.

Run with Azure CLI authenticated and environment variables configured:
PowerShell: $env:RUN_AZURE_SMOKE="1"; python -m pytest tests/smoke -q
"""
import os
from pathlib import Path

import pytest
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@pytest.mark.skipif(os.getenv("RUN_AZURE_SMOKE") != "1", reason="Opt-in Azure integration smoke test")
def test_foundry_inference():
    endpoint = os.environ["AZURE_FOUNDRY_ENDPOINT"]
    deployment = os.environ["AZURE_FOUNDRY_DEPLOYMENT"]
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )
    client = OpenAI(base_url=endpoint, api_key=token_provider, timeout=30, max_retries=1)
    response = client.responses.create(
        model=deployment,
        input="Explain an example of safe enterprise document automation in one sentence.",
    )
    assert response.output_text.strip()
