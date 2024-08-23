import psycopg2
# import pandas as pd
# from src.config import config

connector = config()

class DbAdmin:
    """Класс для управление Базой данных."""

    def __init__(self, host=connector['host'], database= connector['database'], user=connector['user'],
                 password=connector['password']):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

    def _delete_db(self, name: str):
        """Удаляет базу данных."""
        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        request_del = f"""DROP DATABASE IF EXISTS {name}"""
        self.connect.autocommit = True
        cursor.execute(request_del)
        self.connect.commit()
        cursor.close()
        # connect.close()

    def _create_db(self, name: str):
        """Создает базу данных."""
        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        request_create = f"""CREATE DATABASE {name}"""
        self.connect.autocommit = True
        cursor.execute(request_create)
        # connect.commit()

        cursor.close()
        # connect.close()

    def _create_table(self, table_name: str, references= False, **kwargs):
        """Создает таблицу.
        name - название таблицы.
        kwargs - столбец=type"""
        columns = []
        for key, val in kwargs.items():
            list_1 = [key, val]
            data = ' '.join(list_1)
            columns.append(data)
        col_type = ', '.join(columns)

        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        request_create = f"""CREATE TABLE IF NOT EXISTS {table_name}
                        (
                            {col_type}
                        )"""
        cursor.execute(request_create)
        self.connect.commit()
        cursor.close()
        # connect.close()

    def _delete_table(self, table_name: str):
        """Удаляет таблицу"""
        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        request = f"""DROP TABLE IF EXISTS {table_name} CASCADE"""
        cursor.execute(request)
        self.connect.commit()
        cursor.close()
        # connect.close()

    def _truncate_table(self, table_name: str):
        """отчищает таблицу."""
        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        request = f"""TRUNCATE TABLE IF EXISTS {table_name}"""
        cursor.execute(request)
        self.connect.commit()
        cursor.close()
        # connect.close()

    def _insert_into_table(self, table_name: str, column_name: list, *args: tuple):
        """Добавляет данные в таблицу.
        table_name -имя таблицы.
        args - данные в кортеже, которые хотим добавить
        Например:
        (1, test), (2, test_2) - добавит 2 строки в таблицу.
        кол-во элементов в кортеже должно быть равно кол-ву столбцов выбранной таблице.
        если в столбец не заносятся данные, то ставим - NULL"""
        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        cursor.execute(f"""select * from {table_name} limit 0""")
        val = '%s, ' * len(column_name)
        request_into = f"""insert into {table_name} ({', '.join(column_name)}) values ({val[:-2]})"""
        if len(column_name) != 1:
            data_into = args
        else:
            data_into = []
            for arg in args:
                values = []
                values.append(arg)
                data_into.append(values)
        # print(request_into, data_into, val, sep='\n')
        cursor.executemany(request_into, data_into)
        self.connect.commit()
        cursor.close()
        # connect.close()

    def get_data(self):
        """Получаем список компаний и кол-во вакансий."""
        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        request = f"""select *
                    from user_data ud
                    """
        cursor.execute(request)
        data = cursor.fetchall()
        info = ''
        for el in data:
            info += f"Имя {el[1]}, password: {el[2]}\n"

        # df = pd.DataFrame(data, columns=columns)
        cursor.close()
        return info
        # print(df)
        # want_to_save = input("Do you want to save the data? (y/n): ").lower().strip()
        # if want_to_save == 'y':
        #     self.excel_saver(df)
        # # connect.close()
        # return df

    def get_all_vacancies(self) -> pd.DataFrame:
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        request = f"""select e.name
                        ,v.*
                    from employers e
                        left join vacancies v
                        on e.employer_id = v.employer_id"""
        cursor.execute(request)
        data = cursor.fetchall()
        columns = []
        for desc in cursor.description:
            columns.append(desc[0])

        df = pd.DataFrame(data, columns=columns)
        cursor.close()
        print(df)
        want_to_save = input("Do you want to save the data? (y/n): ").lower().strip()
        if want_to_save == 'y':
            self.excel_saver(df)
        # self.connect.close()
        return df

    def get_avg_salary(self) -> pd.DataFrame:
        """получает среднюю зарплату по вакансиям."""
        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        request = f"""select round(AVG(v.salary)::numeric, 2) as avg_salary
                    from vacancies v
                                """
        cursor.execute(request)
        data = cursor.fetchall()
        columns = []
        for desc in cursor.description:
            columns.append(desc[0])

        df = pd.DataFrame(data, columns=columns)
        cursor.close()
        print(df)
        want_to_save = input("Do you want to save the data? (y/n): ").lower().strip()
        if want_to_save == 'y':
            self.excel_saver(df)
        # self.connect.close()
        return df

    def get_vacancies_with_higher_salary(self) -> pd.DataFrame:
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        request = f"""select *
                        from vacancies v
                        where v.salary > (
                            select AVG(v.salary)
                            from vacancies v
                                )
                                """
        cursor.execute(request)
        data = cursor.fetchall()
        columns = []
        for desc in cursor.description:
            columns.append(desc[0])

        df = pd.DataFrame(data, columns=columns)
        cursor.close()
        print(df)
        want_to_save = input("Do you want to save the data? (y/n): ").lower().strip()
        if want_to_save == 'y':
            self.excel_saver(df)
        # connect.close()
        return df

    def get_vacancies_with_keyword(self, keywords: list) -> pd.DataFrame:
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        for keyword in range(len(keywords)):
            keyword_1 = f"'%{keywords[keyword]}%'"
            keywords[keyword] = keyword_1
        condition = ' or v.name like '.join(keywords)
        # connect = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = self.connect.cursor()
        request = f"""select *
                    from vacancies v
                    where v.name like {condition}
                                """
        cursor.execute(request)
        data = cursor.fetchall()
        columns = []
        for desc in cursor.description:
            columns.append(desc[0])

        df = pd.DataFrame(data, columns=columns)
        cursor.close()
        print(df)
        want_to_save = input("Do you want to save the data? (y/n): ").lower().strip()
        if want_to_save == 'y':
            self.excel_saver(df)
        # connect.close()
        # print(df.columns)
        # df.to_excel('test_file.xlsx')
        return df

    def excel_saver(self, data):
        """Сохраняет данные в excel"""
        file_name = input('Введите название файла:')
        data.to_excel(f'{file_name}.xlsx', index=False)
