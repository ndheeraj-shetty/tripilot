import asyncio
from app.core.database import AsyncSessionLocal
from app.services.project_service import ProjectService
from app.domain.schemas.project_schema import ProjectCreate

async def seed():
    async with AsyncSessionLocal() as db:
        service = ProjectService(db)
        projects = await service.list_projects()
        if not projects:
            p = await service.create_project(ProjectCreate(
                name="PyTorch Image Classifier",
                description="ResNet50 model training session with synthetic dataset.",
                framework="PyTorch",
                model_name="resnet50",
                dataset_path="./storage/datasets",
                training_script_path="./scripts/sample_training.py",
                output_dir="./storage/outputs",
                checkpoint_dir="./storage/checkpoints",
                automation_enabled=True
            ))
            print(f"Successfully seeded sample project: {p.id}")
        else:
            print(f"Projects already exist ({len(projects)} found).")

if __name__ == "__main__":
    asyncio.run(seed())
