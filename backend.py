import requests
import protocol
from pydantic import BaseModel, HttpUrl


class BackendConn(BaseModel):
    """BackendConn is a class that represents a connection to the backend server.
    It is used to make requests to the backend server."""
    url: HttpUrl

    def get_files_for_project(self,
                              user_id: str,
                              project_id: str,
                              cursor: int = 0,
                              pageSize: int = 100) -> protocol.ListFilesResponse:
        """Get files for a project from the backend server."""
        result = requests.get(
            url=f"http://{self.url}/project/{project_id}/files",
            params={"cursor": cursor, "pageSize": pageSize},
            headers={"userId": user_id})

        print(result.json())
        return protocol.ListFilesResponse(**result.json())
