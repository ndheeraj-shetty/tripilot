import asyncio
import traceback
from app.core.database import AsyncSessionLocal
from app.services.project_service import ProjectService
from app.services.training_manager import training_manager

async def main():
    try:
        async with AsyncSessionLocal() as db:
            service = ProjectService(db)
            projects = await service.list_projects()
            print(f"Found {len(projects)} projects.")
            if projects:
                proj = projects[0]
                print(f"Starting training for project ID: {proj.id} ({proj.name})")
                res = await training_manager.start_training(project_id=proj.id)
                print(f"Start training success: {res}")
    except Exception as e:
        print("EXCEPTION CAUGHT IN TEST:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
