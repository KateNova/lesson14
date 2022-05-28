import sqlite3


def execut_query(query):
    with sqlite3.connect('netflix.db') as con:
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        # получение списка кортежей из названий колонок
        column_names = cur.description
    # возврат пустого списка в случае отсутствия фильма в базе данных
    if not data:
        return []
    # создание списка из названий колонок без None
    column_list = []
    for item in column_names:
        column_list.append(item[0])
    # объединение в список словарей из результатов запроса и списка названий колонок
    final_list = []
    for row in data:
        final_dict = dict(zip(column_list, row))
        final_list.append(final_dict)
    return final_list


def search_by_title(title):
    '''
    :param title: строка с названием фильма для поиска
    :return: словарь
    '''
    result = execut_query(f'SELECT title, country, release_year, type, description FROM netflix WHERE title LIKE "{title}%" ' \
                   f'ORDER BY release_year DESC;')
    if not result:
        # возврат строки в случае, если фильма нет в базе данных
        return "Такого фильма нет!"
    else:
        return result[0]


def search_by_year_range(start_year, end_year):
    '''
    :param start_year:
    :param end_year:
    :return: список словарей с перечислением фильмов из базы данных в диапозоне заданных лет
    '''
    result = execut_query(f'SELECT title, release_year FROM netflix WHERE release_year BETWEEN {start_year} AND {end_year} '
                          f'ORDER BY release_year LIMIT 100;')
    return result


def search_by_rating(rating_list):

    # делаем новый список для того чтобы слева и справа добавить по кавычке
    rating_list_str = []
    for rating in rating_list:
        rating_list_str.append('"' + rating + '"')

    # собираем из списка строку через запятую и пробел джоином
    q_string = ', '.join(rating_list_str)

    # собираем общий запрос и использованием сделанной строки
    query = f'SELECT title, rating, description FROM netflix WHERE rating in ({q_string});'
    result = execut_query(query)
    return result


def search_by_genre(genre):
    '''
    :param genre: строка
    :return: список словарей
    '''
    # в запросе намеренно оставлен год выпуска для отслеживания правильной сортировки по дате выхода картины
    result = execut_query(f'SELECT title, description, release_year FROM netflix WHERE listed_in LIKE "%{genre}%" ORDER by release_year DESC '
                          f'LIMIT 10;')
    return result


def get_list_of_actors(first_actor, second_actor):
    result = execut_query(f'SELECT "cast" FROM netflix '
                          f'WHERE "cast" LIKE "%{first_actor}%" AND "cast" LIKE "%{second_actor}%"')
    # создаем список всех актеров из запроса с участием first_actor и second_actor
    actors = []
    for row in result:
        actors.extend(row["cast"].split(', '))
    # запускаем цикл для создания словаря, где ключ равен актеру, а значение равно количеству вхождений в список actors
    unique_actors = {}
    for actor in actors:
        # задаем условие, что если ключ(актер) не найден в словаре unique_actors, то значение = 1
        if not unique_actors.get(actor, None):
            unique_actors[actor] = 1
        # если ключ найден, то значение увеличивается на 1
        else:
            unique_actors[actor] += 1
    # запускаем цикл для создания списка актеров (за исключением first_actor и second_actor), чье значение > 2
    final_result = []
    for k, v in unique_actors.items():
        if v > 2 and k != first_actor and k != second_actor:
            final_result.append(k)
    return final_result


def get_movies_by_params(cinema_type, release_year, genre):
    '''
    :param cinema_type: строка - тип картины
    :param release_year: целое число - год выхода кратины
    :param genre: строка - жанр картины
    :return: список словарей с название  и описанием картины
    '''
    result = execut_query(f'SELECT title, description FROM netflix WHERE type LIKE "%{cinema_type}%" '
                          f'AND release_year LIKE "%{release_year}%" AND listed_in LIKE "%{genre}%";')
    return result
