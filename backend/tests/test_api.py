from os import remove
import pytest
from httpx import AsyncClient

from app.api import app
from app.db.service import recreate_tables, create_defaults

@pytest.mark.asyncio
@pytest.fixture(autouse=True)
async def reset_database():
    await recreate_tables()
    await create_defaults()

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

@pytest.mark.asyncio
async def test_block_sets():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        before_response = await ac.get("/block_sets/")
        before_block_sets = before_response.json()

        assert before_response.status_code == 200
        assert len(before_block_sets) == 1
        
        BLOCK_SET = "New Blockset"

        insert_response = await ac.post("/block_sets/", json={"name": BLOCK_SET})
        new_block_set = insert_response.json()

        assert insert_response.status_code == 200
        assert new_block_set["name"] == BLOCK_SET
        assert new_block_set["id"] == 2

        after_insert_response = await ac.get("/block_sets/")
        after_insert_block_sets = after_insert_response.json()

        assert after_insert_response.status_code == 200
        assert len(after_insert_block_sets) == 2

        remove_response = await ac.get("/block_sets/{}/delete".format(new_block_set["id"]))

        assert remove_response.status_code == 200

        after_remove_response = await ac.get("/block_sets/")
        after_remove_block_sets = after_remove_response.json()

        assert after_remove_response.status_code == 200
        assert len(after_remove_block_sets) == 1

        # todo: removing nonexisting block sets

@pytest.mark.asyncio
async def test_blocking():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        before_response = await ac.get("/block_sets/")
        before_block_sets = before_response.json()

        assert before_response.status_code == 200
        assert len(before_block_sets) == 1

        insert_response = await ac.post("/block_sets/", json={"name": "New Blockset"})
        new_block_set = insert_response.json()

        assert insert_response.status_code == 200
        assert new_block_set["name"] == "New Blockset"
        assert new_block_set["id"] == 2
        assert len(new_block_set["apps"]) == 0

        APP_PATH1 = "/path/to/app"
        APP_PATH2 = "/path/to/other/app"

        block_response = await ac.post(
            "/block_sets/{}/block/".format(new_block_set["id"]),
            json=[{"app_path": APP_PATH1},{"app_path": APP_PATH2}])
        block_set_blocked = block_response.json()

        assert block_response.status_code == 200
        assert block_set_blocked["id"] == new_block_set["id"]
        assert len(block_set_blocked["apps"]) == 2
        assert block_set_blocked["apps"][0]["app_path"] == APP_PATH1
        assert block_set_blocked["apps"][1]["app_path"] == APP_PATH2

        unblock_response = await ac.post(
            "/block_sets/{}/unblock/".format(new_block_set["id"]),
            json=[{"app_path": APP_PATH1}])
        block_set_unblocked = unblock_response.json()

        assert unblock_response.status_code == 200
        assert block_set_unblocked["id"] == new_block_set["id"]
        assert len(block_set_unblocked["apps"]) == 1
        assert block_set_unblocked["apps"][0]["app_path"] == APP_PATH2

    # todo: trying to block existing applications
    # todo: trying to remove nonexisting applications

# todo: Timeframes
