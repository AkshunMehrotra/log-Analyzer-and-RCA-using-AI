import json
class LLMService:
    def __init__(self, errors):
        response = []
        for error in errors:
            response.append({
            "error": error["message"],
            "ai_root_cause": "AI services is not cofigured yest.",
            "ai_recommendation": "Wating For LLM integration."
        })
        return response
