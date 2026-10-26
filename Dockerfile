FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
EXPOSE 8000
RUN useradd --create-home appuser
USER appuser
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
