from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal
from uuid import UUID, uuid4

app = FastAPI()

#Health endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

WorkflowName = Literal["agent_job"]

# The request schema defines what fields are allowed and their types. FastAPI validates incoming JSON against it and rejects invalid requests with 422.
class JobCreateRequest(BaseModel):
    workflow: WorkflowName = "agent_job"
    input: Dict[str, Any] = Field(default_factory=dict)
    steps: List[str] = Field(
        default_factory=lambda: ["validate_input", "run_agent", "validade_output"]
    )

#The response schema defines the exact shape we return so clients get a stable contract and we do not accidentally leak internal fields.
class JobCreateResponse(BaseModel):
    job_id: UUID
    workflow: WorkflowName
    status: Literal["queued"]
    steps: List[str]

# In memory store so endpoint has somewhere to write
JOBS: Dict[UUID, JobCreateResponse] = {}

#Post endpoint
@app.post("/v1/jobs", response_model=JobCreateResponse)
def create_job(req: JobCreateRequest) -> JobCreateResponse:
    # Accept only validate input
    # Generate a new job id
    job_id = uuid4(),

    job = JobCreateResponse(
    job_id = job_id,
    workflow = req.workflow,
    status = "queued",     # Set status to queued 
    steps = req.steps
    )
    # Persist in memory
    JOBS[job_id] = job
    # Return the response contract
    return job