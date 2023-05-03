from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import declarative_base, relationship

# Database Schema

Base = declarative_base()

class Artist(Base):
    '''
    Recording Artists
    '''
    __tablename__ = 'Artists'
    Id = Column(Integer, primary_key=True, nullable=False)
    ArtistName = Column(String(120), nullable=False, unique=True)
    Date_Created = Column(String(12), default=datetime.utcnow)
    Albums = relationship('Album')

class Genre(Base):
    '''
    Musical Styles
    '''
    __tablename__ = 'Genres'
    Id = Column(Integer, primary_key=True, nullable=False)
    GenreName = Column(String(120), nullable=False, unique=True)
    Date_Created = Column(String(12), default=datetime.utcnow)
    Tracks = relationship('Track')

class Mediatype(Base):
    '''
    MediaType of Track
    '''
    __tablename__ = 'MediaTypes'
    Id = Column(Integer, primary_key=True, nullable=False)
    MediaTypeName = Column(String(120), nullable=False, unique=True)
    Date_Created = Column(String(12), default=datetime.utcnow)
    Tracks = relationship('Track')

class Playlist(Base):
    '''
    Suggested Genre Mixes
    '''
    __tablename__ = 'Playlists'
    Id = Column(Integer, primary_key=True, nullable=False)
    PlayListName = Column(String(120), nullable=False, unique=True)
    Date_Created = Column(String(12), default=datetime.utcnow)
    PlaylistTrack = relationship('Playlisttrack')

class Album(Base):
    '''
    Available Albums
    '''
    __tablename__ = 'Albums'
    Id = Column(Integer, primary_key=True, nullable=False)
    Title = Column(String(160), nullable=False, unique=True)
    ArtistId = Column(Integer, ForeignKey('Artists.Id'), nullable=False, index=True)
    Date_Created = Column(String(12), default=datetime.utcnow)
    Tracks = relationship('Track')

class Employee(Base):
    '''
    Employees
    '''
    __tablename__ = 'Employees'
    Id = Column(Integer, primary_key=True, nullable=False)
    LastName = Column(String(20), nullable=False)
    FirstName = Column(String(20), nullable=False)
    Title = Column(String(30), nullable=False)
    ReportsTo = Column(Integer, ForeignKey('Employees.Id'), nullable=False, index=True)
    BirthDate = Column(String(65))
    HireDate = Column(String(65))
    Address = Column(String(70))
    City = Column(String(40))
    State = Column(String(40))
    Country = Column(String(40))
    PostalCode = Column(String(10))
    Phone = Column(String(24))
    Fax = Column(String(24))
    Email = Column(String(60), nullable=False, unique=True)
    Date_Created = Column(String(12), default=datetime.utcnow)
    SupportReps = relationship('Customer')
    Employees = relationship('Employee')

class Customer(Base):
    '''
    Customers
    '''
    __tablename__ = 'Customers'
    Id = Column(Integer, primary_key=True, nullable=False)
    FirstName = Column(String(40), nullable=False)
    LastName = Column(String(20), nullable=False)
    Company = Column(String(80))
    Address = Column(String(70))
    City = Column(String(40))
    State = Column(String(40))
    Country = Column(String(40))
    PostalCode = Column(String(10))
    Phone = Column(String(24))
    Fax = Column(String(24))
    Email = Column(String(60), nullable=False, unique=True)
    SupportRepId = Column(Integer, ForeignKey('Employees.Id'), index=True)
    Date_Created = Column(String(12), default=datetime.utcnow)
    Invoices = relationship('Invoice')

class Invoice(Base):
    '''
    Invoices
    '''
    __tablename__ = 'Invoices'
    Id = Column(Integer, primary_key=True, nullable=False)
    CustomerId = Column(Integer, ForeignKey('Customers.Id'), nullable=False, index=True)
    InvoiceDate = Column(String(65))
    BillingAddress = Column(String(70))
    BillingCity = Column(String(40))
    BillingState = Column(String(40))
    BillingCountry = Column(String(40))
    BillingPostalCode = Column(String(10))
    Email = Column(String(60))
    Total = Column(Numeric(10, 2), nullable=False)
    Date_Created = Column(String(12), default=datetime.utcnow)
    InvoiceItems = relationship('Invoiceitem')

class Track(Base):
    '''
    Available Tracks per Album
    '''
    __tablename__ = 'Tracks'
    Id = Column(Integer, primary_key=True, nullable=False)
    TrackName = Column(String(200), nullable=False)
    AlbumId = Column(Integer, ForeignKey('Albums.Id'), nullable=False, index=True)
    MediaTypeId = Column(Integer, ForeignKey('MediaTypes.Id'), nullable=False, index=True)
    GenreId = Column(Integer, ForeignKey('Genres.Id'), nullable=False, index=True)
    Composer = Column(String(220))
    Milliseconds = Column(Integer, nullable=False)
    Bytes = Column(Integer)
    UnitPrice = Column(Numeric(10, 2), nullable=False)
    Date_Created = Column(String(12), default=datetime.utcnow)
    PlaylistTracks = relationship('Playlisttrack')

class Invoiceitem(Base):
    '''
    Invoice Items
    '''
    __tablename__ = 'InvoiceItems'
    Id = Column(Integer, primary_key=True, nullable=False)
    InvoiceId = Column(Integer, ForeignKey('Invoices.Id'), nullable=False, index=True)
    TrackId = Column(Integer, ForeignKey('Tracks.Id'), nullable=False, index=True)
    UnitPrice = Column(Numeric(10, 2), nullable=False)
    Quantity = Column(Integer, nullable=False)
    Date_Created = Column(String(12), default=datetime.utcnow)

class Playlisttrack(Base):
    '''
    Playlist Tracks
    '''
    __tablename__ = 'PlaylistTracks'
    Id = Column(Integer, primary_key=True, nullable=False)
    PlaylistId = Column(Integer, ForeignKey('Playlists.Id'), nullable=False, index=True)
    TrackId = Column(Integer, ForeignKey('Tracks.Id'), nullable=False, index=True)
    Date_Created = Column(String(12), default=datetime.utcnow)
