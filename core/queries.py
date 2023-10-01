# Authors list

authors_math_aggregations_query = ('''
                                        SELECT core_author.id, last_name, first_name, 
                                        COUNT(core_book.id) AS Number_of_books,
                                        IFNULL(ROUND(AVG(price), 2), 0) AS Average_price
                                        FROM core_author
                                        LEFT JOIN core_book
                                        ON core_author.id = author_id
                                        GROUP BY last_name, first_name, birth_date
                                                                                    ''')

books_of_authors_query  = ('''
                                SELECT core_book.id, title, price, core_category.name AS category_name
                                FROM core_book, core_category, core_author
                                WHERE author_id = core_author.id  AND category_id = core_category.id
                                ORDER BY last_name, first_name, title                                              
                                                                        ''')

# For Update Author

particular_author_data_query = (''' 
                                    SELECT id,
                                    COUNT(core_book.id) AS Number_of_books,
                                    IFNULL(ROUND(AVG(price), 2), 0) AS Average_price
                                    FROM core_book
                                    WHERE core_book.author_id = %(author_id)s
                                                                                ''')

particular_author_books_query = ('''
                                    SELECT core_book.id, title, price, core_category.name AS category_name
                                    FROM core_book, core_category
                                    WHERE author_id = %(author_id)s  AND category_id = core_category.id
                                    ORDER BY title                                              
                                                    ''')

# For Update Book

particular_book_query = ('''
                            SELECT core_book.id, title, pub_date, price, is_published, core_book.description, 
                            author_id, category_id
                            FROM core_book, core_author, core_category
                            WHERE core_book.author_id = core_author.id AND
                            core_book.category_id = core_category.id AND
                            core_book.id = %(book_id)s
                                                        ''')

# For searching

author_search_one_parameter_query = (''' 
                                        SELECT core_author.id, last_name, first_name,
                                        COUNT(core_book.id) AS Number_of_books,
                                        IFNULL(ROUND(AVG(price), 2), 0) AS Average_price
                                        FROM core_author
                                        LEFT JOIN core_book 
                                        ON core_author.id = author_id
                                        WHERE last_name LIKE %(lname)s OR 
                                        first_name LIKE %(fname)s
                                        GROUP BY last_name, first_name
                                                                        ''')

particular_author_search_two_parameters_query = (''' 
                                                    SELECT core_author.id, last_name, first_name,
                                                    COUNT(core_book.id) AS Number_of_books,
                                                    IFNULL(ROUND(AVG(price), 2), 0) AS Average_price
                                                    FROM core_author
                                                    LEFT JOIN core_book 
                                                    ON core_author.id = author_id
                                                    WHERE last_name LIKE %(lname_first_check)s AND 
                                                    first_name LIKE %(fname_first_check)s OR 
                                                    last_name LIKE %(lname_second_check)s AND
                                                    first_name LIKE %(fname_second_check)s
                                                    GROUP BY last_name
                                                                        ''')

author_search_two_parameters_query = (''' 
                                        SELECT core_author.id, last_name, first_name,
                                        COUNT(core_book.id) AS Number_of_books,
                                        IFNULL(ROUND(AVG(price), 2), 0) AS Average_price
                                        FROM core_author
                                        LEFT JOIN core_book 
                                        ON core_author.id = author_id
                                        WHERE last_name LIKE %(lname_first_check)s OR 
                                        last_name LIKE %(lname_second_check)s OR 
                                        first_name LIKE %(fname_first_check)s OR
                                        first_name LIKE %(fname_second_check)s
                                        GROUP BY last_name, first_name
                                                                        ''')

book_search_query = ('''
                        SELECT core_book.id, title, price, core_category.name AS category_name,
                        last_name AS author_lastname, first_name As author_firstname,
                        core_author.id AS author_id 
                        FROM core_book, core_category, core_author
                        WHERE title LIKE %(title)s AND
                        author_id = core_author.id  AND 
                        category_id = core_category.id
                        ORDER BY title 
                                        ''')
