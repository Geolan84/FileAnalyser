# FileAnalyser

Данная программа разворачивается на сервере и поддерживает работу двух ручек: POST-метод search, где указываются фильтры для поиска файлов (время создания, маска названия, слова в текстовом представлении, размер файла) и GET-метод searches(), который возвращает результат поиска по его идентификатору.


Инструкция

* В проекте есть виртуальная среда, поэтому дополнительно ничего устанавливать не нужно.
  Для активации среды откройте папку проекта в терминале и введите команду ./venv/Scripts/activate если вы на Windows, на unix допишите source.
* Если хотите развернуть программу в своём окружении, то перед запуском введите в терминале "pip install -r requirements.txt".
* Для запуска введите в терминал команду 'python src/main.py {path}', где path - это путь к папке для поиска.
* Api удобно тестировать через swagger, после запуска откройте его по адресу http://localhost:8080/docs

Заметка: поиск без параметров вернёт пустой список. Параметры опциональны, можно комбинировать в разном количестве.
Важно: если задаёте size для файлов, не забудьте, что размер файла - неотрицательное число!

Пояснительная записка к реализации.

1. В условии не оговорено, существуют ли ограничения на использование фреймворков и библиотек,
посему я решил реализовать сервер на FastAPI - этот фреймворк обеспечивает быструю работу программы,
поскольку активно использует асинхронность, а ешё поддерживает автоматическое документирование в swagger.

2. Для декларирования формата входных данных в endpoint'ах использовался pydantic, представления описаны в файле schemas.py

3. Были мысли прикрутить сюда PostgreSQL, чтобы история поиска не обнулялась после перезапуска программы, обернуть всё в docker-compose,
но это решение кажется несколько излишним.

4. Так как поиск может быть весьма длительным, а вернуть идентификатор поиска мы можем и не дождавшись результатов, было принято решение
производить поиск в отдельном потоке. После завершения поиска новый поток будет убит системой.

5. В ТЗ не сказано, должен ли поиск быть вложенным. Я опирался на пример ответа к запросу "GET /searches/<search_id>" из условия - там
содержатся вложенные файлы, поэтому мой поиск вложенный.

6. Поиск внутри файлов может занять очень много ресурсов, если считывать файлы полностью, поэтому файлы читаются построчно.
Для большего охвата поиск проводится регистронезависимо.

7. Так был выбран FastAPI тестирование сервера пришлось делать на pytest, он лучше интегрирован. Чаще я работаю с unittest, но здесь для
соблюдения единого стиля/стека использовал только pytest.

P.S. В данной работе я не в полной мере реализовал то, что хотел (здесь не достаёт несколько тестов, как минимум), учёба требовала безотлагательного участия,
однако я старался сделать проект хорошо, если у вас будут какие-то вопросы или замечания, я открыт к диалогу. Спасибо.

P.P.S Получаемые списки файлов в методе поиска переводятся в set для удобства использования операций над множествами.
На данный момент каждый поиск обрабатывает всю директорию, однако стоит учитывать, что поиск по названию или размеру сильно легче, чем поиск по тексту,
поэтому было бы разумно искать по тексту только в тех файлах, которые были найдены на предыдущих этапах. К сожалению, не успеваю реализовать.
