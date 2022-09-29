from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SLQ access layer initialization
DATABASE_FILE = "database.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dateBirth = Column(Date) # A type for datetime.date() objects.
    def __repr__(self):
        return "<Author(id=%d name='%s', dateBirth='%s', n_books=%d)>" % (
                                self.id, self.name, str(self.dateBirth), len(self.books))

class Book(Base):
    __tablename__ = 'books'
    isbn = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    reserved = Column(String)

    author_id = Column(Integer, ForeignKey('author.id')) 

    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return "<Book(isbn ='%s', title = %s, author_id = %d, editora = %s)>" % (self.isbn, self.title,self.author_id, self.publisher)

Author.books = relationship(
    "Book", order_by=Book.isbn, back_populates="author")


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()


def listBooks():
    return session.query(Book).all()

def listAuthors():
    return session.query(Author).all()


def getAuthor(authorID):
    return session.query(Author).filter(Author.id==authorID).first()

def getBook(bookID):
    return session.query(Book).filter(Book.isbn==bookID).first()


def getBooksfromAuthor(authorID):
    author = session.query(Author).filter(Author.id==1).first()
    return author.books

def newAuthor(name , year, mounth, day):
    auth = Author(name = name, dateBirth = datetime.date(year, mounth, day))
    session.add(auth)
    session.commit()


def newBook(authorID, isbn, title , publisher):
    book1 = Book(isbn = isbn, title = title, publisher=publisher, reserved = False, author_id = authorID)
    session.add(book1)
    session.commit()

def changeReserveState(bookID, newState):
    b = getBook(bookID)
    b.reserved = newState
    session.commit()




if __name__ == "__main__":

    if not db_exists:
        newAuthor("Camões" , 1524, 1, 1)
        newAuthor("Fernando pessoa" , 1888, 6, 13)
        newAuthor("José Saramago" , 1888, 6, 13)
        
        newBook(authorID = 1, isbn = "978989702182", title = 'Os Lusíadas', publisher="Guerra & Paz")
        newBook(authorID = 1, isbn = "978090000045", title = 'Os Lusíadas', publisher="Open Gate Press")
        newBook(authorID = 2, isbn = "978024120013", title = 'The Book of Disquiet', publisher="Penguin Books Ltd")

    #queries
    print("\nall authors")
    lAuthors = session.query(Author).all()
    print(lAuthors)
    print(listAuthors())

    print("\nall books")
    lBooks = session.query(Book).all()
    print(lBooks)
    print(listBooks())
    print("\nauthors born before 1900")
    oldAuthors = session.query(Author).filter(Author.dateBirth < datetime.date(1900, 1, 1)).all()
    for a in oldAuthors:
        print(a.id, a.name, a.dateBirth, a.books)


    print("\ncamoes")
    authx = session.query(Author).filter(Author.id==1).first()
    print(authx)
    print("\nBooks by camoes (id = 1)")
    print(authx.books)


    booksCamoes = session.query(Book).filter(Book.author == authx).all()
    print(booksCamoes)

    print(getBooksfromAuthor(1))