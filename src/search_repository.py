from operator import gt, ge, lt, le, eq
from typing import Tuple
from datetime import datetime
from threading import Thread
import uuid
import os
import glob


class SearchRepository():
    _history = {}

    @classmethod
    def __check_text_keywords(cls, file_path: str, text: str) -> bool:
        """Read file row by row, return True when file contains keyword"""
        file = open(file_path, "r", encoding="utf-8")
        with file:
            while (line := file.readline().rstrip()):
                if text.lower() in line.lower():
                    return True
        return False

    @classmethod
    def __search_by_text(cls, search_directory: str, text: str):
        """Searches files by text in body."""
        result = []
        try:
            for root, _, files in os.walk(search_directory):
                for file in files:
                    path = os.path.join(root, file)
                    if cls.__check_text_keywords(path, text):
                        result.append(path.replace(search_directory, "", 1))
            return set(result)
        except Exception:
            return set()

    @classmethod
    def __search_by_size(cls, search_directory: str, value: int, operator: str) -> set:
        """Search files by size and operator of comparison."""
        operators = {"gt": gt, 'lt': lt, 'ge': ge, 'le': le, 'eq': eq}
        result = []
        try:
            for root, _, files in os.walk(search_directory):
                for file in files:
                    path = os.path.join(root, file)
                    if operators.get(operator)(os.path.getsize(path), value):
                        result.append(path.replace(search_directory, "", 1))
            return set(result)
        except Exception:
            return set()

    @classmethod
    def __search_by_file_mask(cls, search_directory: str, file_mask: str) -> set:
        """Recursively searches files by glob mask."""
        try:
            full_path = f"{search_directory}{os.sep}**{os.sep}{file_mask}"
            res = [x.replace(search_directory, "", 1)
                   for x in glob.glob(full_path, recursive=True)]
            return set(res)
        except Exception:
            return set()

    @classmethod
    def __search_by_creation_time(cls, search_directory, value: int, operator: str) -> set:
        """Search files by creation time and operator of comparison."""
        operators = {"gt": gt, 'lt': lt, 'ge': ge, 'le': le, 'eq': eq}
        result = []
        print("It is creation time method. ", value, operator)
        try:
            for root, _, files in os.walk(search_directory):
                for file in files:
                    path = os.path.join(root, file)
                    timestamp = os.path.getctime(path)
                    datestamp = datetime.fromtimestamp(timestamp)
                    if operators.get(operator)(datestamp.astimezone(value.tzinfo), value):
                        result.append(path.replace(search_directory, "", 1))
            return set(result)
        except:
            return set()

    @classmethod
    def __search_task(cls, key: str, search_directory: str, text: str = None, file_mask: str = None, size: dict = None, creation_time: dict = None):
        """Aggregate results of search by different filters and save them."""
        paths = set()
        if file_mask is not None:
            results = cls.__search_by_file_mask(
                search_directory, file_mask)
            paths = paths.union(results) if paths == set(
            ) else paths.intersection(results)
            print(results)
        if size is not None:
            results = cls.__search_by_size(
                search_directory, size["value"], size["operator"].value)
            paths = paths.union(results) if paths == set(
            ) else paths.intersection(results)
            print(results)
        if creation_time is not None:
            results = cls.__search_by_creation_time(
                search_directory, creation_time["value"], creation_time["operator"].value)
            paths = paths.union(results) if paths == set(
            ) else paths.intersection(results)
        if text is not None:
            results = cls.__search_by_text(search_directory, text)
            paths = paths.union(results) if paths == set(
            ) else paths.intersection(results)
        cls._history[key] = (True, list(paths))

    @classmethod
    async def search_files(cls, search_directory: str, text: str = None, file_mask: str = None, size: dict = None, creation_time: dict = None) -> str:
        """Main search method, starts search in other thread."""
        key = str(uuid.uuid4())
        thread1 = Thread(target=cls.__search_task, args=(
            key, search_directory, text, file_mask, size, creation_time))
        thread1.start()
        cls._history[key] = (False, )
        return key

    @classmethod
    async def get_search_result(cls, search_id: str) -> Tuple[bool, ...]:
        """Returns result of search from history."""
        if search_id in cls._history:
            return (cls._history[search_id])
        else:
            raise ValueError()
