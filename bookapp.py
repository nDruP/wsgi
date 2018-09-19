import re
import traceback
from bookdb import BookDB

DB = BookDB()


def book(book_id):
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    else:
        body = "<h1>"+book['title']+'</h1>\n'
        body += "<h2>Author: </h2>"+book['author']+'\n'
        body += "<h2>Publisher: </h2>"+book['publisher']+'\n'
        body += "<h2>ISBN: </h2>"+book['isbn']+'\n'
    return body


def books():
    all_books = DB.titles()
    body = "<h1>Bookshelf</h1>\n<ul>"
    for book in all_books:
        body += "<li>"
        body += "<a href=/book/"+book['id']+'>'+book['title']
        body += "</a>"
        body += "</li>\n"
    body += "</ul>"
    return body


def resolve_path(path):
    funcs = {
        '': books,
        'book': book,
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
