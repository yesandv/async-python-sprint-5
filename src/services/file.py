from src.models import FileModel
from src.schemas.file import FileUpload, FileInDB
from src.services.file_base import FileDBRepository


class FileRepository(FileDBRepository[FileModel, FileUpload, FileInDB]):
    pass


file_crud = FileRepository(FileModel)
