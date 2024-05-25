import requests
import protocol


class BackendConn:
    """BackendConn is a class that represents a connection to the backend server.
    It is used to make requests to the backend server."""
    _address: str = ""

    def __init__(self, addr: str):
        self._address = addr

    def get_files_for_project(self,
                              project_id: str,
                              cursor: int = 0,
                              pageSize: int = 100) -> protocol.ListFilesResponse:
        # FIXME: User here should come from the flask login
        result = requests.get(
            url=f"http://{self._address}/project/{project_id}/files",
            params={"cursor": cursor, "pageSize": pageSize},
            headers={"userId": "testU"})

        print(result.json())
        return protocol.ListFilesResponse(**result.json())
