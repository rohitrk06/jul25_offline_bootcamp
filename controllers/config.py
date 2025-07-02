class Config:
    """
    Configuration class for the Flask application.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False