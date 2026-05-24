import json
from typing import Optional

import httpx

from config import MUAPI_API_KEY


API_BASE = "https://api.muapi.ai"


class MuAPIClient:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or MUAPI_API_KEY
        self.base_url = API_BASE
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    async def _post(self, path: str, data: dict, timeout: int = 120) -> dict:
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, headers=self.headers, json=data)
            resp.raise_for_status()
            return resp.json()

    async def _get(self, path: str) -> dict:
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    # ─── Auth ─────────────────────────────────────────────────────────

    async def login(self, email: str, password: str) -> dict:
        return await self._post("/auth/login", {
            "email": email, "password": password
        })

    async def generate_api_key(self) -> dict:
        return await self._post("/app/generate-api-key", {})

    # ─── Workflow Orchestration ────────────────────────────────────────

    async def architect_workflow(self, prompt: str) -> dict:
        """Use the AI architect to design a workflow from natural language."""
        return await self._post("/workflow/architect", {
            "prompt": prompt,
        }, timeout=180)

    async def poll_architect(self, architect_id: str) -> dict:
        """Poll the architect for the completed workflow design."""
        return await self._get(f"/workflow/poll-architect/{architect_id}/result")

    async def create_workflow(self, name: str, nodes: list, edges: list) -> dict:
        """Create a workflow with specified nodes and connections."""
        return await self._post("/workflow/create", {
            "name": name,
            "nodes": nodes,
            "edges": edges,
        })

    async def run_workflow(self, workflow_id: str, inputs: dict) -> dict:
        """Execute a workflow with given inputs."""
        return await self._post(f"/workflow/{workflow_id}/run", {
            "inputs": inputs
        }, timeout=300)

    async def execute_workflow_api(self, workflow_id: str, inputs: dict) -> dict:
        """Execute a workflow via the dedicated API execute endpoint."""
        return await self._post(
            f"/workflow/{workflow_id}/api-execute", inputs, timeout=300
        )

    async def get_workflow_status(self, run_id: str) -> dict:
        """Check workflow run status."""
        return await self._get(f"/workflow/run/{run_id}/status")

    async def get_workflow_outputs(self, run_id: str) -> dict:
        """Get workflow run outputs."""
        return await self._get(f"/workflow/run/{run_id}/api-outputs")

    async def get_workflow_inputs(self, workflow_id: str) -> dict:
        """Get expected inputs for a workflow."""
        return await self._get(f"/workflow/{workflow_id}/api-inputs")

    async def list_workflows(self) -> list:
        data = await self._get("/workflow/get-workflow-defs")
        return data if isinstance(data, list) else data.get("workflows", [])

    async def get_workflow_def(self, workflow_id: str) -> dict:
        return await self._get(f"/workflow/get-workflow-def/{workflow_id}")

    # ─── Agent / Avatar ────────────────────────────────────────────────

    async def create_agent(self, name: str, system_prompt: str = "", skills: list = None) -> dict:
        """Create an AI agent (avatar)."""
        payload = {"name": name}
        if system_prompt:
            payload["system_prompt"] = system_prompt
        if skills:
            payload["skills"] = skills
        return await self._post("/agents", payload)

    async def chat_with_agent(self, agent_id: str, message: str) -> dict:
        """Chat with an agent (avatar)."""
        return await self._post(f"/agents/{agent_id}/chat", {
            "message": message
        })

    async def quick_create_agent(self, description: str) -> dict:
        """Quick-create an agent from a description."""
        return await self._post("/agents/quick-create", {
            "description": description
        })

    async def list_agents(self) -> list:
        data = await self._get("/agents/user/agents")
        return data if isinstance(data, list) else data.get("agents", [])

    # ─── Media Generation (API v1) ─────────────────────────────────────

    async def generate_image(self, prompt: str, aspect_ratio: str = "16:9",
                              resolution: str = "2K", quality: str = "high") -> dict:
        return await self._post("/api/v1/gpt-image-2-text-to-image", {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "quality": quality,
        })

    async def lipsync_video(self, video_url: str, audio_url: str) -> dict:
        """Lip-sync a video with audio."""
        return await self._post("/api/v1/sync-lipsync", {
            "video_url": video_url,
            "audio_url": audio_url,
        })

    async def generate_speech(self, prompt: str, voice_id: str = "male-optimistic-upbeat",
                              webhook_url: str = "") -> dict:
        """Generate speech audio. Results delivered via webhook."""
        payload = {"prompt": prompt, "voice_id": voice_id}
        if webhook_url:
            payload["webhook_url"] = webhook_url
        return await self._post("/api/v1/minimax-speech-2.6-hd", payload)

    async def generate_music(self, style: str, prompt: str = "",
                             webhook_url: str = "") -> dict:
        """Generate background music. Results delivered via webhook."""
        payload = {"style": style}
        if prompt:
            payload["prompt"] = prompt
        if webhook_url:
            payload["webhook_url"] = webhook_url
        return await self._post("/api/v1/suno-create-music", payload)

    async def generate_talking_head(self, image_url: str, audio_url: str, prompt: str = "") -> dict:
        """Generate talking head video from an image + audio."""
        payload = {"image_url": image_url, "audio_url": audio_url}
        if prompt:
            payload["prompt"] = prompt
        return await self._post("/api/v1/infinitetalk-image-to-video", payload)



    async def apply_video_effect(self, image_url: str, effect_name: str = "Melt") -> dict:
        return await self._post("/api/v1/video-effects", {
            "image_url": image_url,
            "name": effect_name,
        })

    async def generate_video(self, prompt: str, model: str = "wan2.1") -> dict:
        return await self._post("/api/v1/wan2.1-text-to-video", {
            "prompt": prompt,
        })

    async def check_credits(self) -> dict:
        return await self._get("/api/v1/account/balance")

    async def list_models(self) -> list:
        data = await self._get("/api/v1/models")
        return data if isinstance(data, list) else data.get("models", [])

    async def poll_result(self, prediction_id: str) -> dict:
        """Poll a prediction for its result."""
        return await self._get(f"/api/v1/predictions/{prediction_id}/result")

    async def upload_media(self, file_path: str) -> dict:
        async with httpx.AsyncClient(timeout=120) as client:
            with open(file_path, "rb") as f:
                resp = await client.post(
                    f"{self.base_url}/api/v1/upload_file",
                    headers={"x-api-key": self.api_key},
                    files={"file": f},
                )
                resp.raise_for_status()
                return resp.json()

    async def health_check(self) -> bool:
        try:
            await self._get("/api/v1/models")
            return True
        except Exception:
            return False
