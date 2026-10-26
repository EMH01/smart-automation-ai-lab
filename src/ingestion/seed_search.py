"""Populate a sample Azure AI Search index with fictional documents."""
import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchFieldDataType, SearchableField, SimpleField,
)
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def seed_documents():
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    index_name = os.getenv("AZURE_SEARCH_INDEX", "hr-knowledge")
    credential = DefaultAzureCredential()
    schema = SearchIndex(
        name=index_name,
        fields=[
            SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
            SearchableField(name="title", type=SearchFieldDataType.String),
            SearchableField(name="content", type=SearchFieldDataType.String),
        ],
    )
    with SearchIndexClient(endpoint=endpoint, credential=credential) as client:
        client.create_or_update_index(schema)

    docs = [
        {"id": "hr-001", "title": "Vacaciones", "content": "Documento ficticio: las solicitudes de vacaciones se tramitan en el portal interno y requieren aprobación."},
        {"id": "payroll-001", "title": "Consulta de nóminas", "content": "Documento ficticio: las dudas sobre nóminas se comunican mediante una incidencia interna sin enviar información bancaria por correo."},
        {"id": "security-001", "title": "Protección de datos", "content": "Documento ficticio: antes de procesar información personal hay que comprobar identidad, permisos y minimización de datos."},
    ]
    with SearchClient(endpoint=endpoint, index_name=index_name, credential=credential) as client:
        results = client.upload_documents(documents=docs)
        print("Uploaded:", [(r.key, r.succeeded) for r in results])
        print("Search results:")
        for item in client.search(search_text="vacaciones", select=["id", "title"], top=3):
            print(item["id"], item["title"])


if __name__ == "__main__":
    seed_documents()
