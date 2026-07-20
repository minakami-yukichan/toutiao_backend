from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, \
    general_exception_handler

def register_exception_handler(app):
    """
    注册全局异常处理器
    """
    app.add_exception_handler(HTTPException, http_exception_handler)  # 业务逻辑异常
    app.add_exception_handler(IntegrityError, integrity_error_handler)  # 数据库完整性
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)  # 数据库异常
    app.add_exception_handler(Exception, general_exception_handler)  # 兜底异常处理