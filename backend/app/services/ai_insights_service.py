import os
import logging
import threading
import time
from google import genai

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

GEMINI_LOCK = threading.Lock()
GEMINI_MIN_INTERVAL = 4.5
_last_call_time = 0


def _wait_for_rate_limit():
    global _last_call_time
    with GEMINI_LOCK:
        elapsed = time.time() - _last_call_time
        if elapsed < GEMINI_MIN_INTERVAL:
            time.sleep(GEMINI_MIN_INTERVAL - elapsed)
        _last_call_time = time.time()


def generate_climate_insights(climatology_data, current_year_data):
    climatology_text = climatology_data.to_string()
    current_year_text = current_year_data.to_string()

    prompt = f"""
        Você é um meteorologista especialista em agronegócio, analisando dados climáticos de um talhão agrícola em Jataí, Goiás, Brasil.

        Dados de climatologia histórica (médias mensais dos últimos 30 anos):
        {climatology_text}

        Dados climáticos do ano atual até o mês mais recente disponível:
        {current_year_text}

        Com base na comparação entre os dados históricos e o ano atual, escreva uma análise objetiva (2-3 parágrafos curtos) sobre:
        1. Anomalias climáticas relevantes observadas neste ano em comparação à média histórica
        2. Possíveis riscos ou impactos para a produção agrícola nesse talhão
        3. Recomendações práticas, se aplicável

        Seja direto e use linguagem acessível para um produtor rural, evitando jargão técnico excessivo.
        Não inclua título, cabeçalho ou introdução do tipo "Análise climática de..." — comece direto pelo conteúdo, já que este texto será inserido em um documento que já possui seu próprio título de seção.
        Limite sua resposta a no máximo 900 caracteres no total, mantendo a análise concisa mas completa.
        """

    _wait_for_rate_limit()

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        return response.text
    except Exception as e:
        logger.error(f"Erro ao gerar insights de IA: {e}")
        return "Não foi possível gerar a análise por IA no momento."