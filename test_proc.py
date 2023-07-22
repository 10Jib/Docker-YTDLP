import pytest
import requests
import logging

from process_functions import startytdl, init
from app import app 

longVideo="https://www.youtube.com/watch?v=PZJlA8Mur_g"
midVideo="https://www.youtube.com/watch?v=xnpQCHJzhHM"
shortVideo="https://www.youtube.com/watch?v=Ades3pQbeh8"

logger = logging.Logger(__name__)
logger.addHandler(logging.StreamHandler())
print("starting test")

@pytest.fixture
def process():
    init(logger)

def test_download(tmp_path, process):
    
    p = tmp_path / "test.txt"
    p.write_text("this is a test")
    result = startytdl(shortVideo, {"paths":tmp_path})
    assert result[-1] == 200


# def test_api():
#     print(f'/download/{shortVideo}')
#     response = app.test_client().get(f'/download/{shortVideo}')
#     # somehow this can download multiple videos... not good
#     assert response.status_code == 200
#     # also it wont close the pool correctly
