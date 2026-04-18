"""
基础DAO类
"""
from typing import List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from models.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseDao:
    """基础DAO类"""
    
    def __init__(self, session: Session, model_class: Type[T]):
        self.session = session
        self.model_class = model_class
    
    def create(self, entity: T) -> T:
        """创建实体"""
        self.session.add(entity)
        self.session.flush()
        return entity
    
    def update(self, entity: T) -> T:
        """更新实体"""
        self.session.merge(entity)
        self.session.flush()
        return entity
    
    def delete(self, entity: T):
        """删除实体"""
        self.session.delete(entity)
        self.session.flush()
    
    def get_by_id(self, id: int) -> Optional[T]:
        """根据ID获取实体"""
        return self.session.query(self.model_class).filter_by(id=id).first()
    
    def get_all(self) -> List[T]:
        """获取所有实体"""
        return self.session.query(self.model_class).all()
    
    def count(self) -> int:
        """统计数量"""
        return self.session.query(self.model_class).count()
