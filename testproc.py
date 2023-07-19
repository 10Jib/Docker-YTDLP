import pytest
import requests

from processes.process_functions import startytdl

url="https://www.youtube.com/shorts/lnk2znjCy9M"


print("starting test")
#targetDir = pytest.tmpdir.mkdir("temp")
result = startytdl(url, )
print(result)

# I cant directly import the file because that will change the name