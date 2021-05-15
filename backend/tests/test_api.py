from os import remove
import pytest
from httpx import AsyncClient

from app.api import app
from app.db.service import recreate_tables, create_defaults

NEW_BLOCK_SET_NAME1 = "New Blockset"
NEW_BLOCK_SET_NAME2 = "Other Blockset"
APP_PATH1 = "/path/to/app"
APP_PATH2 = "/path/to/other/app"

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
async def test_block_set_remove_nonexisting():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/block_sets/")
        block_sets = response.json()

        block_set_ids = [bs["id"] for bs in block_sets]

        remove_response = await ac.get("/block_sets/{}/delete".format(max(block_set_ids) + 1))

        assert remove_response.status_code == 404

@pytest.mark.asyncio
async def test_block_set_insert_and_remove():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        before_response = await ac.get("/block_sets/")
        before_block_sets = before_response.json()

        assert before_response.status_code == 200
        assert len(before_block_sets) == 1
        
        insert_response = await ac.post("/block_sets/", json={"name": NEW_BLOCK_SET_NAME1})
        new_block_set = insert_response.json()

        assert insert_response.status_code == 200
        assert new_block_set["name"] == NEW_BLOCK_SET_NAME1
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

@pytest.mark.asyncio
async def test_block_and_unblock():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        before_response = await ac.get("/block_sets/")
        before_block_sets = before_response.json()

        assert before_response.status_code == 200
        assert len(before_block_sets) == 1

        insert_response = await ac.post("/block_sets/", json={"name": NEW_BLOCK_SET_NAME1})
        new_block_set = insert_response.json()

        assert insert_response.status_code == 200
        assert new_block_set["name"] == NEW_BLOCK_SET_NAME1
        assert new_block_set["id"] == 2
        assert len(new_block_set["apps"]) == 0

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

@pytest.mark.asyncio
async def test_block_existing():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        insert_response = await ac.post("/block_sets/", json={"name": NEW_BLOCK_SET_NAME1})
        new_block_set = insert_response.json()

        assert insert_response.status_code == 200
        
        assert len(new_block_set["apps"]) == 0

        block_response = await ac.post(
            "/block_sets/{}/block/".format(new_block_set["id"]),
            json=[{"app_path": APP_PATH1},{"app_path": APP_PATH2}])
        block_set_blocked = block_response.json()
        
        assert len(block_set_blocked["apps"]) == 2

        block_existing_response = await ac.post(
            "/block_sets/{}/block/".format(new_block_set["id"]),
            json=[{"app_path": APP_PATH1}])
       
        assert block_existing_response.status_code == 303 # see other --> send id of existing application

@pytest.mark.asyncio
async def test_unblock_nonexisting():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        insert_response = await ac.post("/block_sets/", json={"name": NEW_BLOCK_SET_NAME1})
        new_block_set = insert_response.json()

        assert insert_response.status_code == 200
        
        assert len(new_block_set["apps"]) == 0

        block_response = await ac.post(
            "/block_sets/{}/block/".format(new_block_set["id"]),
            json=[{"app_path": APP_PATH1}])
        block_set_blocked = block_response.json()
        
        assert block_response.status_code == 200
        assert len(block_set_blocked["apps"]) == 1

        unblock_response = await ac.post(
            "/block_sets/{}/unblock/".format(new_block_set["id"]),
            json=[{"app_path": APP_PATH2}])
        
        assert unblock_response.status_code == 404

@pytest.mark.asyncio
async def test_block_unblock_multiple_block_sets():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        insert_response_1 = await ac.post("/block_sets/", json={"name": NEW_BLOCK_SET_NAME1})
        new_block_set_1 = insert_response_1.json()

        insert_response_2 = await ac.post("/block_sets/", json={"name": NEW_BLOCK_SET_NAME2})
        new_block_set_2 = insert_response_2.json()

        block_response_1 = await ac.post(
            "/block_sets/{}/block/".format(new_block_set_1["id"]),
            json=[{"app_path": APP_PATH1},{"app_path": APP_PATH2}])
        block_set_blocked_1 = block_response_1.json()

        assert block_response_1.status_code == 200
        assert block_set_blocked_1["id"] == new_block_set_1["id"]
        assert len(block_set_blocked_1["apps"]) == 2

        block_response_2 = await ac.post(
            "/block_sets/{}/block/".format(new_block_set_2["id"]),
            json=[{"app_path": APP_PATH1},{"app_path": APP_PATH2}])
        block_set_blocked_1 = block_response_2.json()

        assert block_response_2.status_code == 200
        assert block_set_blocked_1["id"] == new_block_set_2["id"]
        assert len(block_set_blocked_1["apps"]) == 2

        unblock_response = await ac.post(
            "/block_sets/{}/unblock/".format(new_block_set_2["id"]),
            json=[{"app_path": APP_PATH2}])
        block_set_2_refreshed = unblock_response.json()

        assert unblock_response.status_code == 200
        assert block_set_2_refreshed["id"] == new_block_set_2["id"]
        assert len(block_set_2_refreshed["apps"]) == 1
        
        get_response = await ac.get(
            "/block_sets/{}".format(new_block_set_1["id"]))
        block_set_1_refreshed = get_response.json()

        assert len(block_set_1_refreshed["apps"]) == 2

# todo: Timeframes
