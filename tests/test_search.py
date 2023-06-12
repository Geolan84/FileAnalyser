import shutil
import os
import pytest
from src.search_repository import SearchRepository


@pytest.mark.asyncio
async def test_get_search_result_negative():
    SearchRepository._history = []
    with pytest.raises(ValueError):
        await SearchRepository.get_search_result("nonexistant search_id")


@pytest.mark.asyncio
async def test_get_search_result_positive():
    SearchRepository._history = {
        "21c54b3e-98ad-428e-a1fd-6a7de2d0138b": (True, [])}
    assert await SearchRepository.get_search_result("21c54b3e-98ad-428e-a1fd-6a7de2d0138b") == (True, [])


def test_check_nonexistant_text_keywords():
    with open("testKeywords.txt", "w", encoding="utf-8") as f:
        f.write("Шла Саша по шоссе и сосала сушку")
        f.flush()
    try:
        assert not SearchRepository._SearchRepository__check_text_keywords(
            "testKeywords.txt", "пончики")
    finally:
        os.remove("testKeywords.txt")


def test_check_text_keywords():
    with open("testKeywords.jpg", "w", encoding="utf-8") as f:
        f.write("Шла Саша по шоссе и сосала сушку\n"
                "Летели дракончики, кушали пончики.\n"
                "Сколько пончиков съели дракончики?\n")
        f.flush()
    try:
        assert SearchRepository._SearchRepository__check_text_keywords(
            "testKeywords.jpg", "пончики")
    finally:
        os.remove("testKeywords.jpg")


def test_search_by_file_mask():
    try:
        os.mkdir("testFilesForMask")
        os.chdir("testFilesForMask")
        with open("test1.jpg", "w", encoding="utf-8") as f:
            f.write("кушали пончики")
        with open("test1.txt", "w", encoding="utf-8") as f:
            f.write("кушали пончики")
        with open("test.txt", "w", encoding="utf-8") as f:
            f.write("кушали пончики")
        with open(".txt", "w", encoding="utf-8") as f:
            f.write("кушали пончики")
        with open("a.txt", "w", encoding="utf-8") as f:
            f.write("Шла Саша")
        with open("b.txt", "w", encoding="utf-8") as f:
            f.write("Шла Саша")
        os.chdir('..')
        # Платформозависимый тест, в будущем нужно исправить.
        assert SearchRepository._SearchRepository__search_by_file_mask(
            "testFilesForMask", "*.txt") == {'\\test1.txt', '\\test.txt', '\\a.txt', '\\b.txt'}
        assert SearchRepository._SearchRepository__search_by_file_mask(
            "testFilesForMask", "?.txt") == {'\\a.txt', '\\b.txt'}
    except FileExistsError:
        return
    finally:
        shutil.rmtree('testFilesForMask', ignore_errors=True)


def test_search_by_size():
    try:
        os.mkdir("testFilesForSize")
        os.chdir("testFilesForSize")
        with open("test1.txt", "w", encoding="utf-8") as f:
            f.write("a"*6000)
        with open("test2.txt", "w", encoding="utf-8") as f:
            f.write("r"*1000)
        with open("test3.txt", "w", encoding="utf-8") as f:
            f.write("q"*3000)
        os.chdir('..')

        assert SearchRepository._SearchRepository__search_by_size(
            "testFilesForSize", 4000, "gt") == {'\\test1.txt'}
        assert SearchRepository._SearchRepository__search_by_size(
            "testFilesForSize", 4000, "lt") == {'\\test2.txt', '\\test3.txt'}

    except FileExistsError:
        return
    finally:
        shutil.rmtree('testFilesForSize', ignore_errors=True)


def test_search_by_text():
    try:
        os.mkdir("testFilesForSearchText")
        os.chdir("testFilesForSearchText")
        with open("test1.txt", "w", encoding="utf-8") as f:
            f.write("ПОнчики пончики \nВот они дракончики")
        with open("test2.txt", "w", encoding="utf-8") as f:
            f.write("Саша не дошла, устала и уснула.")
        with open("test3.txt", "w", encoding="utf-8") as f:
            f.write("Опять пончики, но в нижнем регистре\nСтрока.")
        os.chdir('..')

        assert SearchRepository._SearchRepository__search_by_text(
            "testFilesForSearchText", "Саша") == {'\\test2.txt'}
        assert SearchRepository._SearchRepository__search_by_text(
            "testFilesForSearchText", "пончики") == {'\\test1.txt', '\\test3.txt'}

    except FileExistsError:
        return
    finally:
        shutil.rmtree('testFilesForSearchText', ignore_errors=True)
