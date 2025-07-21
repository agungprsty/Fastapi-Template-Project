import pkgutil
import importlib
import inspect

from beanie import Document
from typing import Type


def collect_documents(package: str) -> list[Type[Document]]:
    """
    Scan dan kumpulkan semua class turunan `Beanie.Document` dari package.
    :param package: Misal 'src.infrastructure.document'
    :return: List of Document classes
    """
    documents: list[Type[Document]] = []

    package_module = importlib.import_module(package)
    for _, module_name, _ in pkgutil.walk_packages(package_module.__path__, prefix=package_module.__name__ + "."):
        module = importlib.import_module(module_name)

        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Document) and obj is not Document:
                documents.append(obj)

    return documents
