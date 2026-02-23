FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# deps de runtime
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app
COPY . .

# DEBUG: validar se o JSON entrou na imagem
RUN echo "=== LS /app ===" && ls -la /app \
 && echo "=== LS /app/data ===" && ls -la /app/data || true \
 && echo "=== FIND pedidos.json ===" && find /app -maxdepth 4 -name "pedidos.json" -print || true


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]