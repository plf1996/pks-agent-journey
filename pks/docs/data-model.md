# 个人知识管理系统（PKS）- 数据模型设计文档

**文档版本**：v1.0
**创建日期**：2026-01-08
**架构师**：后端系统架构师
**状态**：规划阶段

---

## 1. 数据模型概述

### 1.1 核心实体

本系统包含以下核心实体：

1. **User（用户）**：系统使用者，支持多租户数据隔离
2. **Card（卡片）**：知识卡片，支持多种内容类型
3. **Tag（标签）**：卡片分类标签，支持层级结构
4. **CardTag（卡片标签关联）**：卡片与标签的多对多关系
5. **CardLink（卡片关联）**：卡片间的双向链接关系
6. **KanbanColumn（看板列）**：看板视图的列定义
7. **KanbanCard（看板卡片关联）**：卡片在看板中的位置

### 1.2 ER 关系图

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    User      │         │  KanbanColumn│         │     Tag      │
│──────────────│         │──────────────│         │──────────────│
│ id (PK)      │         │ id (PK)      │         │ id (PK)      │
│ username     │         │ user_id (FK) │         │ user_id (FK) │
│ email        │         │ name         │         │ name         │
│ password_hash│         │ position     │         │ color        │
│ created_at   │         │ created_at   │         │ parent_id    │
│ updated_at   │         │ updated_at   │         │ created_at   │
└──────┬───────┘         └──────┬───────┘         └──────┬───────┘
       │                        │                        │
       │ 1                     1 │                    1   │
       │                        │                        │
       │ N                     N │                    N   │
       │                        │                        │
       ▼                        ▼                        ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    Card      │◄────────│  KanbanCard  │         │  CardTag     │
│──────────────│         │──────────────│         │──────────────│
│ id (PK)      │         │ card_id (FK) │         │ card_id (FK) │
│ user_id (FK) │         │ column_id    │         │ tag_id (FK)  │
│ title        │    ┌────│ position     │         └──────────────┘
│ content      │    │    └──────────────┘               ▲
│ card_type    │    │                                  │
│ is_pinned    │    │                                  │
│ created_at   │    │                                  │
│ updated_at   │    │                                  │
└──────┬───────┘    │                                  │
       │            │                                  │
       │            │                                  │
       ▼            │                                  │
┌──────────────┐    │                    ┌──────────────┐
│  CardLink    │    │                    │  CardTag     │
│──────────────│    │                    │──────────────│
│ id (PK)      │    │                    │ (同一表)      │
│ source_card  │    │                    │              │
│ target_card  │    │                    │              │
│ link_type    │    │                    │              │
│ created_at   │    │                    │              │
└──────────────┘    │                    │              │
       │            │                    │              │
       └────────────┴────────────────────┴──────────────┘
                     (所有关系都通过 user_id 隔离)
```

---

## 2. 详细表设计

### 2.1 用户表（users）

**用途：** 存储系统用户信息

**表结构：**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | 用户唯一标识 |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名（登录用） |
| email | VARCHAR(100) | UNIQUE, NOT NULL | 邮箱（登录用） |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt 哈希密码 |
| is_active | BOOLEAN | DEFAULT TRUE | 账户是否激活 |
| is_superuser | BOOLEAN | DEFAULT FALSE | 是否为超级管理员 |
| created_at | DATETIME | DEFAULT NOW | 创建时间 |
| updated_at | DATETIME | DEFAULT NOW | 更新时间 |

**索引设计：**
```sql
-- 唯一索引（自动创建）
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- 查询索引
CREATE INDEX idx_users_created_at ON users(created_at);
```

**SQLAlchemy 模型：**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

**业务规则：**
- 用户名：3-50 个字符，只能包含字母、数字、下划线
- 邮箱：必须符合邮箱格式，用于找回密码
- 密码：最少 8 位，包含字母和数字（应用层验证）
- 默认创建一个 admin 用户（首次启动时）

---

### 2.2 卡片表（cards）

**用途：** 存储知识卡片内容

**表结构：**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | 卡片唯一标识 |
| user_id | INTEGER | FOREIGN KEY → users.id, NOT NULL | 所属用户 |
| title | VARCHAR(200) | NOT NULL | 卡片标题 |
| content | TEXT | NOT NULL | 卡片内容（根据 type 类型存储） |
| card_type | VARCHAR(20) | NOT NULL | 内容类型：note/link/image/code |
| url | VARCHAR(500) | NULL | 网页链接（当 type=link 时） |
| is_pinned | BOOLEAN | DEFAULT FALSE | 是否置顶 |
| view_count | INTEGER | DEFAULT 0 | 浏览次数 |
| created_at | DATETIME | DEFAULT NOW | 创建时间 |
| updated_at | DATETIME | DEFAULT NOW | 更新时间 |

**索引设计：**
```sql
-- 主键索引（自动创建）
CREATE UNIQUE INDEX idx_cards_id ON cards(id);

-- 用户数据隔离索引（非常重要！）
CREATE INDEX idx_cards_user_id ON cards(user_id);

-- 全文搜索索引（PostgreSQL）
CREATE INDEX idx_cards_title_gin ON cards USING gin(to_tsvector('simple', title));
CREATE INDEX idx_cards_content_gin ON cards USING gin(to_tsvector('simple', content));

-- 复合索引（用户 + 创建时间，用于列表查询）
CREATE INDEX idx_cards_user_created ON cards(user_id, created_at DESC);

-- 类型筛选索引
CREATE INDEX idx_cards_type ON cards(user_id, card_type);

-- SQLite FTS5 虚拟表（开发环境）
CREATE VIRTUAL TABLE cards_fts USING fts5(
    title, content,
    content='cards',
    content_rowid='id'
);

-- 触发器（保持 FTS 索引同步）
CREATE TRIGGER cards_ai AFTER INSERT ON cards BEGIN
  INSERT INTO cards_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
END;

CREATE TRIGGER cards_ad AFTER DELETE ON cards BEGIN
  DELETE FROM cards_fts WHERE rowid = old.id;
END;

CREATE TRIGGER cards_au AFTER UPDATE ON cards BEGIN
  DELETE FROM cards_fts WHERE rowid = old.id;
  INSERT INTO cards_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
END;
```

**SQLAlchemy 模型：**
```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class CardType(str, enum.Enum):
    NOTE = "note"      # 笔记
    LINK = "link"      # 网页链接
    IMAGE = "image"    # 图片（存储 Base64 或 URL）
    CODE = "code"      # 代码片段

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    card_type = Column(Enum(CardType), nullable=False, default=CardType.NOTE)
    url = Column(String(500), nullable=True)  # 仅当 type=link 时使用
    is_pinned = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="cards")
    tags = relationship("CardTag", back_populates="card", cascade="all, delete-orphan")
    source_links = relationship("CardLink", foreign_keys="CardLink.source_card_id", back_populates="source_card")
    target_links = relationship("CardLink", foreign_keys="CardLink.target_card_id", back_populates="target_card")
    kanban_items = relationship("KanbanCard", back_populates="card", cascade="all, delete-orphan")
```

**业务规则：**
- 标题：1-200 个字符
- 内容：根据类型不同，存储格式不同
  - note：Markdown 文本
  - link：存储在 url 字段，content 存储备注
  - image：Base64 编码或图片 URL
  - code：代码文本 + 语言标识（content 中存储 JSON）
- 用户只能查看和操作自己的卡片（user_id 隔离）
- 删除用户时，级联删除所有卡片

---

### 2.3 标签表（tags）

**用途：** 存储卡片分类标签

**表结构：**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | 标签唯一标识 |
| user_id | INTEGER | FOREIGN KEY → users.id, NOT NULL | 所属用户 |
| name | VARCHAR(50) | NOT NULL | 标签名称 |
| color | VARCHAR(7) | DEFAULT '#1976D2' | 标签颜色（十六进制） |
| parent_id | INTEGER | FOREIGN KEY → tags.id, NULL | 父标签 ID（支持层级） |
| created_at | DATETIME | DEFAULT NOW | 创建时间 |
| updated_at | DATETIME | DEFAULT NOW | 更新时间 |

**索引设计：**
```sql
-- 唯一索引（同一用户下标签名称唯一）
CREATE UNIQUE INDEX idx_tags_user_name ON tags(user_id, name);

-- 用户数据隔离索引
CREATE INDEX idx_tags_user_id ON tags(user_id);

-- 父子关系索引
CREATE INDEX idx_tags_parent_id ON tags(parent_id);

-- 复合索引（用于层级查询）
CREATE INDEX idx_tags_user_parent ON tags(user_id, parent_id);
```

**SQLAlchemy 模型：**
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    color = Column(String(7), default="#1976D2")  # 十六进制颜色码
    parent_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="tags")
    parent = relationship("Tag", remote_side=[id], back_populates="children")
    children = relationship("Tag", back_populates="parent", cascade="all, delete-orphan")
    card_tags = relationship("CardTag", back_populates="tag", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_tag_user_name'),
    )
```

**业务规则：**
- 标签名称：1-50 个字符
- 同一用户下标签名称唯一
- 支持层级结构（最多 3 层）
- 颜色格式：#RRGGBB（如 #FF5733）
- 删除父标签时，级联删除所有子标签

---

### 2.4 卡片标签关联表（card_tags）

**用途：** 实现卡片与标签的多对多关系

**表结构：**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | 关联唯一标识 |
| card_id | INTEGER | FOREIGN KEY → cards.id, NOT NULL | 卡片 ID |
| tag_id | INTEGER | FOREIGN KEY → tags.id, NOT NULL | 标签 ID |
| created_at | DATETIME | DEFAULT NOW | 创建时间 |

**索引设计：**
```sql
-- 唯一索引（防止重复关联）
CREATE UNIQUE INDEX idx_card_tags_card_tag ON card_tags(card_id, tag_id);

-- 查询索引（查询卡片的所有标签）
CREATE INDEX idx_card_tags_card_id ON card_tags(card_id);

-- 查询索引（查询标签下的所有卡片）
CREATE INDEX idx_card_tags_tag_id ON card_tags(tag_id);
```

**SQLAlchemy 模型：**
```python
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class CardTag(Base):
    __tablename__ = "card_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    card = relationship("Card", back_populates="tags")
    tag = relationship("Tag", back_populates="card_tags")

    __table_args__ = (
        UniqueConstraint('card_id', 'tag_id', name='uq_card_tag'),
    )
```

**业务规则：**
- 同一卡片不能重复关联同一标签
- 删除卡片时，级联删除所有关联
- 删除标签时，级联删除所有关联

---

### 2.5 卡片关联表（card_links）

**用途：** 存储卡片间的双向链接关系

**表结构：**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | 关联唯一标识 |
| source_card_id | INTEGER | FOREIGN KEY → cards.id, NOT NULL | 源卡片 ID |
| target_card_id | INTEGER | FOREIGN KEY → cards.id, NOT NULL | 目标卡片 ID |
| link_type | VARCHAR(20) | DEFAULT 'reference' | 链接类型：reference/related/parent |
| created_at | DATETIME | DEFAULT NOW | 创建时间 |

**索引设计：**
```sql
-- 唯一索引（防止重复关联）
CREATE UNIQUE INDEX idx_card_links_source_target ON card_links(source_card_id, target_card_id);

-- 查询索引（查询卡片的所有出链）
CREATE INDEX idx_card_links_source ON card_links(source_card_id);

-- 查询索引（查询卡片的所有入链）
CREATE INDEX idx_card_links_target ON card_links(target_card_id);

-- 复合索引（查询双向关系）
CREATE INDEX idx_card_links_source_type ON card_links(source_card_id, link_type);
```

**SQLAlchemy 模型：**
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class LinkType(str, enum.Enum):
    REFERENCE = "reference"  # 普通引用
    RELATED = "related"      # 相关推荐
    PARENT = "parent"        # 父子关系

class CardLink(Base):
    __tablename__ = "card_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    target_card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    link_type = Column(String(20), default=LinkType.REFERENCE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    source_card = relationship("Card", foreign_keys=[source_card_id], back_populates="source_links")
    target_card = relationship("Card", foreign_keys=[target_card_id], back_populates="target_links")

    __table_args__ = (
        UniqueConstraint('source_card_id', 'target_card_id', name='uq_card_link'),
    )
```

**业务规则：**
- 卡片不能链接到自身
- 同一对卡片只能存在一种链接关系
- 创建双向链接时，需要插入两条记录（A→B 和 B→A）
- 删除卡片时，级联删除所有相关链接

**双向链接实现示例：**
```python
# 用户操作：将卡片 A 链接到卡片 B
def create_bidirectional_link(source_id: int, target_id: int, link_type: LinkType):
    # 创建正向链接
    link1 = CardLink(source_card_id=source_id, target_card_id=target_id, link_type=link_type)
    # 创建反向链接
    link2 = CardLink(source_card_id=target_id, target_card_id=source_id, link_type=link_type)
    session.add(link1)
    session.add(link2)
    session.commit()

# 查询卡片的所有关联（正向 + 反向）
def get_all_linked_cards(card_id: int):
    # 正向链接：我链接到的卡片
    outgoing = session.query(CardLink).filter(CardLink.source_card_id == card_id).all()

    # 反向链接：链接到我的卡片
    incoming = session.query(CardLink).filter(CardLink.target_card_id == card_id).all()

    return {
        "outgoing": outgoing,
        "incoming": incoming
    }
```

---

### 2.6 看板列表表（kanban_columns）

**用途：** 存储看板视图的列定义

**表结构：**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | 列唯一标识 |
| user_id | INTEGER | FOREIGN KEY → users.id, NOT NULL | 所属用户 |
| name | VARCHAR(50) | NOT NULL | 列名称 |
| position | INTEGER | NOT NULL | 排序位置（0, 1, 2...） |
| created_at | DATETIME | DEFAULT NOW | 创建时间 |
| updated_at | DATETIME | DEFAULT NOW | 更新时间 |

**索引设计：**
```sql
-- 复合唯一索引（同一用户下，位置唯一）
CREATE UNIQUE INDEX idx_kanban_columns_user_position ON kanban_columns(user_id, position);

-- 用户数据隔离索引
CREATE INDEX idx_kanban_columns_user_id ON kanban_columns(user_id);
```

**SQLAlchemy 模型：**
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class KanbanColumn(Base):
    __tablename__ = "kanban_columns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    position = Column(Integer, nullable=False)  # 排序位置
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="kanban_columns")
    kanban_cards = relationship("KanbanCard", back_populates="column", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('user_id', 'position', name='uq_kanban_column_user_position'),
    )
```

**业务规则：**
- 列名称：1-50 个字符
- 默认创建 3 列：待处理（0）、进行中（1）、已完成（2）
- 用户可自定义列的数量和名称
- 删除列时，级联删除该列下的所有卡片

---

### 2.7 看板卡片关联表（kanban_cards）

**用途：** 存储卡片在看板列中的位置

**表结构：**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | 关联唯一标识 |
| card_id | INTEGER | FOREIGN KEY → cards.id, NOT NULL | 卡片 ID |
| column_id | INTEGER | FOREIGN KEY → kanban_columns.id, NOT NULL | 列 ID |
| position | INTEGER | NOT NULL | 在列中的排序位置 |
| created_at | DATETIME | DEFAULT NOW | 创建时间 |
| updated_at | DATETIME | DEFAULT NOW | 更新时间 |

**索引设计：**
```sql
-- 唯一索引（同一列中，位置唯一）
CREATE UNIQUE INDEX idx_kanban_cards_column_position ON kanban_cards(column_id, position);

-- 查询索引（查询卡片在看板中的位置）
CREATE INDEX idx_kanban_cards_card_id ON kanban_cards(card_id);

-- 查询索引（查询列中的所有卡片）
CREATE INDEX idx_kanban_cards_column_id ON kanban_cards(column_id);
```

**SQLAlchemy 模型：**
```python
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class KanbanCard(Base):
    __tablename__ = "kanban_cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    column_id = Column(Integer, ForeignKey("kanban_columns.id", ondelete="CASCADE"), nullable=False, index=True)
    position = Column(Integer, nullable=False)  # 在列中的排序位置
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    card = relationship("Card", back_populates="kanban_items")
    column = relationship("KanbanColumn", back_populates="kanban_cards")

    __table_args__ = (
        UniqueConstraint('column_id', 'position', name='uq_kanban_card_column_position'),
    )
```

**业务规则：**
- 同一卡片可以出现在多个看板列中（未来扩展，当前一对一）
- 拖拽卡片时，动态更新 position 字段
- 删除列时，级联删除该列下的所有卡片关联

---

## 3. 数据模型关系总结

### 3.1 完整关系图

```
User (1) ──< (N) Card
  │                 │
  │                 ├─< (N) CardTag >─ (N) Tag
  │                 │
  │                 ├─< (N) CardLink (source)
  │                 │
  │                 ├─ (N) CardLink (target) >─┐
  │                 │                          │
  │                 └─< (N) KanbanCard >─ (N) KanbanColumn
  │
  └─< (N) Tag
        │
        └─ (1) >─< (N) Tag (parent_id, self-referential)
```

### 3.2 数据隔离策略

**多租户隔离：**
- 所有表都包含 `user_id` 字段（除关联表外）
- 所有查询都必须包含 `WHERE user_id = current_user.id` 条件
- 级联删除：删除用户时，删除所有相关数据

**示例查询：**
```python
# 错误：没有数据隔离
cards = session.query(Card).all()

# 正确：添加用户过滤
current_user = get_current_user()
cards = session.query(Card).filter(Card.user_id == current_user.id).all()
```

### 3.3 级联删除规则

| 操作 | 级联效果 |
|------|---------|
| 删除 User | 删除该用户的所有 Card、Tag、KanbanColumn |
| 删除 Card | 删除相关的 CardTag、CardLink（双向）、KanbanCard |
| 删除 Tag | 删除相关的 CardTag、子 Tag |
| 删除 KanbanColumn | 删除相关的 KanbanCard |

---

## 4. 性能优化策略

### 4.1 索引策略

**必选索引：**
- 所有外键字段
- 所有 user_id 字段（数据隔离）
- 常用查询字段（title, created_at）

**可选索引（根据查询模式优化）：**
- 复合索引：(user_id, created_at)
- 全文搜索索引（PostgreSQL GIN）
- FTS5 虚拟表（SQLite）

### 4.2 查询优化

**避免 N+1 查询：**
```python
# 错误：N+1 查询
cards = session.query(Card).all()
for card in cards:
    print(card.tags)  # 每次循环都执行一次查询

# 正确：使用 joinedload
from sqlalchemy.orm import joinedload
cards = session.query(Card).options(joinedload(Card.tags)).all()
for card in cards:
    print(card.tags)  # 已经加载，不会执行额外查询
```

**分页查询：**
```python
def get_cards(user_id: int, page: int = 1, page_size: int = 20):
    offset = (page - 1) * page_size
    return session.query(Card)\
        .filter(Card.user_id == user_id)\
        .order_by(Card.created_at.desc())\
        .limit(page_size)\
        .offset(offset)\
        .all()
```

### 4.3 缓存策略（可选）

**缓存场景：**
- 热点卡片（高 view_count）
- 标签列表
- 看板列配置

**实现方式：**
- 开发环境：使用 functools.lru_cache
- 生产环境：集成 Redis

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_tag_by_id(tag_id: int):
    return session.query(Tag).filter(Tag.id == tag_id).first()
```

---

## 5. 数据迁移计划

### 5.1 Alembic 迁移脚本

**初始迁移（001_initial_schema.py）：**
```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # 创建用户表
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_username', 'users', ['username'], unique=True)

    # 创建卡片表
    op.create_table(
        'cards',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('card_type', sa.String(length=20), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('is_pinned', sa.Boolean(), nullable=True),
        sa.Column('view_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_cards_type', 'cards', ['user_id', 'card_type'])
    op.create_index('idx_cards_user_created', 'cards', ['user_id', 'created_at'])
    op.create_index('idx_cards_user_id', 'cards', ['user_id'])

    # ... 其他表的创建

def downgrade():
    op.drop_table('cards')
    op.drop_table('users')
```

### 5.2 数据库切换方案

**SQLite → PostgreSQL 迁移：**

1. 使用 `pg_dump` 导出 SQLite 数据为 SQL
2. 调整 SQL 语法（SQLite → PostgreSQL）
3. 导入到 PostgreSQL
4. 运行 Alembic 迁移到最新版本

**简化方案：**
```python
# 使用 SQLAlchemy 的数据库抽象
# 只需修改连接字符串，无需修改代码

# 开发环境
DATABASE_URL = "sqlite:///./pks.db"

# 生产环境
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/pks"
```

---

## 6. 数据完整性约束

### 6.1 应用层约束

```python
from pydantic import BaseModel, validator

class CardCreate(BaseModel):
    title: str
    content: str
    card_type: CardType

    @validator('title')
    def validate_title(cls, v):
        if not 1 <= len(v) <= 200:
            raise ValueError('标题长度必须在 1-200 个字符之间')
        return v

    @validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError('内容不能为空')
        return v
```

### 6.2 数据库层约束

- NOT NULL 约束：必填字段
- UNIQUE 约束：唯一性约束
- FOREIGN KEY 约束：引用完整性
- CHECK 约束：复杂条件验证（PostgreSQL）

```sql
-- PostgreSQL CHECK 约束示例
ALTER TABLE cards ADD CONSTRAINT check_title_length
CHECK (char_length(title) BETWEEN 1 AND 200);
```

---

## 7. 总结

### 7.1 数据模型特点

✅ **简单清晰**：7 张表，关系明确
✅ **数据隔离**：所有数据通过 user_id 隔离
✅ **可扩展性**：预留扩展字段，支持未来功能
✅ **性能优化**：合理的索引设计，支持高效查询
✅ **数据完整性**：级联删除 + 唯一约束

### 7.2 下一步行动

1. 创建 Alembic 迁移脚本
2. 实现 SQLAlchemy 模型类
3. 编写 Repository 层 CRUD 方法
4. 编写单元测试验证数据模型

### 7.3 注意事项

- 所有查询都必须包含 user_id 过滤（安全第一）
- 级联删除要谨慎（建议软删除）
- 全文搜索在不同数据库实现不同（需适配）
- 生产环境建议使用 PostgreSQL（性能更好）

---

**文档维护：** 本文档应随数据模型变更同步更新
**相关文档：** `architecture.md`（架构设计）、`api-design.md`（API 设计）
