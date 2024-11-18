import requests
import logging
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel

class FlowiseAIResponse(BaseModel):
    response: str
    agent_id: str
    status: str

class FlowiseAI:
    def __init__(self):
        self.base_url = os.getenv("FLOWISE_BASE_URL", "https://goose-ai.app.flowiseai.com/api/v1/prediction")
        self.agents = {
            "jarvis": os.getenv("FLOWISE_JARVIS_ID", "21d1ee07-fbde-4790-96f1-e8a82de105ee"),
            "psychographicAvatar": os.getenv("FLOWISE_PSYCHOGRAPHIC_ID", "f109807e-04d0-4aed-b4b3-b84c17caa490"),
            "companyProfile": os.getenv("FLOWISE_COMPANY_PROFILE_ID", "59ce8a70-2a14-472b-b16c-0af0d03da164"),
            "googleDorking": os.getenv("FLOWISE_GOOGLE_DORKING_ID", "fdf58cff-b539-4287-851f-f18dce1780da"),
            "systemPromptCreator": os.getenv("FLOWISE_SYSTEM_PROMPT_ID", "dbc6e8ca-2c9f-4dce-a4e5-510c32dfc2c7"),
            "botpressIntructions": os.getenv("FLOWISE_BOTPRESS_ID", "1514a0ff-2568-42dd-942b-5ea1b07231f6"),
        }
   
    async def query_agent(self, agent_type: str, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Query a specific Flowise AI agent.
       
        Args:
            agent_type: The type of agent to query (must exist in self.agents)
            question: The question or prompt to send to the agent
            context: Optional additional context for the query
           
        Returns:
            Dict containing the agent's response
        """
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}. Available agents: {list(self.agents.keys())}")
           
        agent_id = self.agents[agent_type]
        api_url = f"{self.base_url}/{agent_id}"
       
        payload = {
            "question": question,
            **(context or {})
        }
       
        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()
            return {
                "response": response.json(),
                "agent_id": agent_id,
                "status": "success"
            }
        except requests.exceptions.RequestException as e:
            logging.error(f"Error querying Flowise AI agent: {str(e)}")
            return {
                "response": str(e),
                "agent_id": agent_id,
                "status": "error"
            }