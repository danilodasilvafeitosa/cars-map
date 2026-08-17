import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"


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

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Erro ao gerar insights de IA: {e}")
        return "Não foi possível gerar a análise por IA no momento."