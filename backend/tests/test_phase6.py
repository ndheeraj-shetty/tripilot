import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.core.metrics import get_system_health, generate_prometheus_metrics
from app.services.backup_service import backup_service

def test_password_hashing():
    raw_pass = "AdminSecret123!"
    hashed = hash_password(raw_pass)
    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPass", hashed) is False

def test_jwt_token_creation_and_decoding():
    payload = {"sub": "user@zombierun.ai", "role": "ADMIN"}
    token = create_access_token(payload, expires_delta=3600)
    assert isinstance(token, str)
    assert len(token.split(".")) == 3

    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user@zombierun.ai"
    assert decoded["role"] == "ADMIN"

def test_system_health_and_prometheus_metrics():
    health = get_system_health()
    assert health["status"] == "HEALTHY"
    assert "cpu_utilization_pct" in health

    prom = generate_prometheus_metrics()
    assert "zombierun_uptime_seconds" in prom
    assert "zombierun_cpu_utilization_pct" in prom

@pytest.mark.asyncio
async def test_backup_service(tmp_path):
    bdir = str(tmp_path / "backups")
    res = await backup_service.create_backup(bdir)
    assert res["status"] == "COMPLETED"
    assert res["file_path"].endswith(".zip")
