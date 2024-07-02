# athena/services/llm_service.py
import logging
import requests
import json

class LLMService:
    def __init__(self, base_url):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    def set_base_url(self, new_base_url):
        self.base_url = new_base_url
        self.logger.info(f"LLM service base URL updated to: {new_base_url}")

    def get_available_models(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return [model['name'] for model in response.json()['models']]
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch models: {e}")
            raise

    def generate_response(self, prompt, model):
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": model, "prompt": prompt},
                stream=True
            )
            response.raise_for_status()
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if 'response' in data:
                            full_response += data['response']
                    except json.JSONDecodeError:
                        self.logger.warning(f"Failed to parse line: {line}")
            return full_response
        except requests.RequestException as e:
            self.logger.error(f"Failed to generate response: {e}")
            raise