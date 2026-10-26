"""Create a small, fictional HR knowledge index in Azure AI Search.

Requires Azure roles: Search Service Contributor (index management) and
Search Index Data Contributor (document upload), assigned to your user.
Run from repo root:
  $env:AZURE_SEARCH_ENDPOINT="https://<search-name>.search.windows.net"
  python scripts/seed_search.py
"""
import os
from pathlib import Path
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SearchField, SearchFieldDataType, SimpleField, SearchableField

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
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
    {"id": "hr-001", "title": "Vacaciones", "content": "Documento de demostración: el empleado solicita vacaciones mediante el portal interno; el responsable revisa y aprueba o rechaza la solicitud. No es una política real."},
    {"id": "payroll-001", "title": "Consulta de nóminas", "content": "Documento de demostración: ante una discrepancia en la nómina, el empleado abre una incidencia interna adjuntando el periodo y una descripción, sin compartir datos bancarios por correo. No es una política real."},
    {"id": "security-001", "title": "Protección de datos", "content": "Documento de demostración: antes de procesar datos personales, se comprueban la identidad del usuario, su autorización y la minimización de datos. No es una política real."},
]
with SearchClient(endpoint=endpoint, index_name=index_name, credential=credential) as client:
    results = client.upload_documents(documents=docs)
    print("Uploaded:", [(r.key, r.succeeded) for r in results])
    print("\nSearch results for 'vacaciones':")
    for item in client.search(search_text="vacaciones", select=["id", "title", "content"], top=3):
        print(f"- {item['id']} | {item['title']}: {item['content']}")
