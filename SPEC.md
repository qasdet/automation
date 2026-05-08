# Архитектурный рефакторинг автотестов

## Текущая структура (после рефакторинга)

```
automation/
├── admin_office/
│   ├── api_interactions/            # API методы
│   ├── data_builders/              # ✅ NEW: Builder Pattern
│   │   ├── base_builder.py
│   │   ├── brand_builder.py
│   │   └── __init__.py
│   ├── components/
│   │   ├── base_page.py           # ✅ UPDATED: Упрощен
│   │   ├── pages/
│   │   │   ├── page_factory.py    # ✅ NEW: Factory Method
│   │   │   └── brands/brands_page.py
│   │   └── models/ui/
│   │       └── sidebar/           # ✅ REFACTORED: Facade Pattern
│   │           ├── sidebar.py
│   │           ├── sidebar_config.py
│   │           └── __init__.py
│   ├── constants.py
│   ├── conftest.py
│   └── tests/
├── controller/                      # ✅ REFACTORED: Fluent interface
│   ├── factory.py                 # Базовый Factory (fluent assertions)
│   ├── button.py, input.py        # Конкретные компоненты
│   └── grid.py, table_new.py      # Таблицы (fluent)
├── user_office/                   # Аналогичная структура
├── http_methods/
├── helper/
└── conftest.py
```

---

## Было → Стало

### Factory Pattern (Этап 1)

**Было:**
```python
def should_be_visible(self, **kwargs) -> None:  # Не возвращает self
    ...
def click(self, **kwargs) -> None:
    ...
```

**Стало:**
```python
def should_be_visible(self, **kwargs) -> 'Factory':  # Возвращает self
    ...
    return self

def click(self, **kwargs) -> 'Factory':
    ...
    return self

# Fluent usage:
button.should_be_visible().click().hover()
```

### Выявленные проблемы

| Проблема | Файл/Модуль | Последствия |
|----------|-------------|-------------|
| **God Object** | `side_bar.py` (40+ методов) | Неподдерживаемость |
| **Отсутствие PageFactory** | `conftest.py` | Создание страниц разрознено |
| **Дублирование should_/check_** | Все модели | Копипаста |
| **Разрозненные API** | `api_interactions/*` | Нет унификации |
| **Builder не применяется** | `data_make_for_brands.py` | Тестовые данные создаются процедурно |
| **Сильная связанность фикстур** | `conftest.py` | Сложно тестировать изолированно |

---

## Целевая архитектура

### Паттерны и их применение

```
┌─────────────────────────────────────────────────────────────────┐
│                      TEST LAYER                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ API Tests   │  │  UI Tests   │  │  Unit Tests │           │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘           │
└─────────┼────────────────┼────────────────┼───────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PAGE OBJECT LAYER                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    PageFactory                            │  │
│  │  create_page(page, PageTypes.BRANDS) → AdminOfficeBrandsPage│ │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  BasePage   │  │ Page Models │  │  Page Obj.  │           │
│  │  (Facade)   │  │ (Domain)     │  │  (Entry)    │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────────────────────────────────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   COMPONENT LAYER                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  Factory    │  │   Widgets   │  │   Grid/     │           │
│  │  (Base)     │  │  (Composite)│  │   Table     │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────────────────────────────────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA LAYER                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │   Builder   │  │   Builder   │  │  Repository │           │
│  │  (Brands)   │  │  (Channels) │  │  (API)      │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Этапы рефакторинга

### Этап 1: Рефакторинг Factory и компонентов

**Цель:** Устранить дублирование, добавить единый интерфейс компонентов

**Изменения:**

#### 1.1 Расширить `Factory` базовый класс
```python
# controller/factory.py
class Factory(ABC):
    def __init__(self, page: Page, locator: str, name: str) -> None:
        self.page = page
        self.name = name
        self.locator = locator

    @property
    @abstractmethod
    def type_of(self) -> str:
        return 'component'

    def get_locator(self, **kwargs) -> Locator:
        locator = self.locator.format(**kwargs)
        return self.page.locator(locator)

    # === UNIFIED ASSERTION METHODS ===
    def should_be_visible(self, timeout: float = 10.0, **kwargs) -> 'Factory':
        """ Fluent assertion - returns self """
        with allure.step(f'Checking {self.type_of} "{self.name}" is visible'):
            expect(self.get_locator(**kwargs)).to_be_visible(timeout=timeout)
        return self

    def should_not_be_visible(self, **kwargs) -> 'Factory':
        with allure.step(f'Checking {self.type_of} "{self.name}" is NOT visible'):
            expect(self.get_locator(**kwargs)).not_to_be_visible()
        return self

    def should_have_text(self, text: str, **kwargs) -> 'Factory':
        with allure.step(f'Checking {self.type_of} "{self.name}" has text "{text}"'):
            expect(self.get_locator(**kwargs)).to_have_text(text)
        return self

    def should_have_value(self, value: str, **kwargs) -> 'Factory':
        expect(self.get_locator(**kwargs)).to_have_value(value)
        return self

    # === UNIFIED ACTION METHODS ===
    def click(self, **kwargs) -> 'Factory':
        with allure.step(f'Clicking {self.type_of} "{self.name}"'):
            self.get_locator(**kwargs).click()
        return self

    def fill(self, value: str, **kwargs) -> 'Factory':
        with allure.step(f'Filling {self.type_of} "{self.name}" with "{value}"'):
            self.get_locator(**kwargs).fill(value)
        return self

    def hover(self, **kwargs) -> 'Factory':
        self.get_locator(**kwargs).hover()
        return self

    def get_text(self, **kwargs) -> str:
        return self.get_locator(**kwargs).inner_text()

    def get_value(self, **kwargs) -> str:
        return self.get_locator(**kwargs).input_value()
```

#### 1.2 Удалить дублирование из конкретных компонентов
```python
# controller/button.py - ПОСЛЕ
class Button(Factory):
    @property
    def type_of(self) -> str:
        return 'button'

    def double_click(self, **kwargs) -> 'Button':
        with allure.step(f'Double clicking {self.type_of} "{self.name}"'):
            self.get_locator(**kwargs).dblclick()
        return self
```

**Результат:**
- `should_*` методы возвращают `self` для fluent interface
- Базовые `click()`, `fill()`, `hover()` - в Factory
- Конкретные классы содержат только специфику

---

### Этап 2: Рефакторинг SideBar (Facade Pattern)

**Цель:** Преобразовать God Object в управляемый Facade

**Текущее:** 40+ методов `check_*()` в одном классе

**После:**

```python
# admin_office/components/models/ui/sidebar/sidebar.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page

class MenuCategory(Enum):
    """Категории меню"""
    MAIN = auto()
    DICTIONARIES = auto()
    PRODUCT_PARAMETERS = auto()
    SOURCE_PARAMETERS = auto()
    OTHER = auto()


@dataclass
class MenuItem:
    """Конфигурация пункта меню"""
    name: str
    testid: str
    category: MenuCategory
    has_hover: bool = False  # Для submenu


class SidebarConfig:
    """Конфигурация меню - данные отдельно от логики"""
    ITEMS = [
        MenuItem('Главная', 'sidebar_home', MenuCategory.MAIN),
        MenuItem('Доступы', 'sidebar_accesses', MenuCategory.MAIN),
        MenuItem('Пользователи', 'sidebar_users', MenuCategory.MAIN),
        MenuItem('Организации', 'sidebar_organizations', MenuCategory.MAIN),
        MenuItem('Справочники', 'sidebar_dictionaries', MenuCategory.MAIN),
        # ... остальные пункты
        MenuItem('Бренды', 'sidebar_brands', MenuCategory.DICTIONARIES),
        MenuItem('Клиенты', 'sidebar_clients', MenuCategory.DICTIONARIES),
        # ...
    ]


class SideBar:
    """Фасад для навигации - инкапсулирует логику меню"""

    def __init__(self, page: 'Page') -> None:
        self.page = page
        self._config = SidebarConfig()
        self._links = self._init_links()

    def _init_links(self) -> dict[str, Link]:
        """Ленивая инициализация ссылок"""
        from controller.link import Link
        return {
            item.name: Link(page=self.page, locator=f"[data-testid='{item.testid}']", name=item.name)
            for item in self._config.ITEMS
        }

    def navigate_to(self, item_name: str) -> None:
        """Единый метод навигации"""
        link = self._links.get(item_name)
        if not link:
            raise ValueError(f"Menu item '{item_name}' not found")
        
        with allure.step(f'Navigate to "{item_name}"'):
            if self._needs_hover(item_name):
                link.hover()
            link.click()

    def _needs_hover(self, item_name: str) -> bool:
        """Проверка необходимости hover для submenu"""
        item = next((i for i in self._config.ITEMS if i.name == item_name), None)
        return item.has_hover if item else False

    # === DEPRECATED: обратная совместимость ===
    def check_brands_link(self) -> None:
        """@deprecated Use navigate_to('Бренды')"""
        warnings.warn("Use navigate_to() instead", DeprecationWarning)
        self.navigate_to('Бренды')
```

**Результат:**
- Конфигурация отделена от логики
- Добавление пункта меню = добавление строки в `ITEMS`
- `navigate_to()` вместо 40+ методов

---

### Этап 3: PageFactory для создания страниц

**Цель:** Унифицировать создание page objects

```python
# admin_office/components/pages/page_factory.py
from enum import Enum, auto
from typing import Type, Callable

from playwright.sync_api import Page

class PageType(Enum):
    BRANDS = auto()
    ORGANIZATIONS = auto()
    CHANNELS = auto()
    # ...

class PageFactory:
    """Фабрика для создания page objects"""

    _registry: dict[PageType, Callable[[Page], Any]] = {}

    @classmethod
    def register(cls, page_type: PageType):
        """Декоратор для регистрации page class"""
        def decorator(page_class: Type):
            cls._registry[page_type] = page_class
            return page_class
        return decorator

    @classmethod
    def create(cls, page: Page, page_type: PageType, **kwargs):
        """Создать page object по типу"""
        if page_type not in cls._registry:
            raise ValueError(f"Page type {page_type} not registered")
        return cls._registry[page_type](page, **kwargs)

    @classmethod
    def get_registered_pages(cls) -> list[PageType]:
        return list(cls._registry.keys())


# === РЕГИСТРАЦИЯ СТРАНИЦ ===
from admin_office.components.pages.brands.brands_page import AdminOfficeBrandsPage

@PageFactory.register(PageType.BRANDS)
class AdminOfficeBrandsPage(BasePage):
    # ... существующий код
```

**Использование в фикстурах:**
```python
# admin_office/conftest.py
@pytest.fixture
def admin_brands_page(chromium_page: Page) -> AdminOfficeBrandsPage:
    return PageFactory.create(chromium_page, PageType.BRANDS)

@pytest.fixture
def admin_organizations_page(chromium_page: Page) -> AdminOfficeOrganizationsPage:
    return PageFactory.create(chromium_page, PageType.ORGANIZATIONS)
```

---

### Этап 4: Builder Pattern для тестовых данных

**Цель:** Создание тестовых данных через fluent interface

**Текущее:**
```python
# data_make_for_brands.py
def make_data_all_brand_fields() -> dict:
    return {
        'name': brand_name(),  # процедурный стиль
        'naming': brand_naming(),
        'organization': ORGANIZATION,
        'brand_awareness': BRAND_AWARENESS,
    }
```

**После:**
```python
# admin_office/data_builders/brand_builder.py
from dataclasses import dataclass, field
from typing import Optional
import string
from faker import Faker

fake = Faker()

@dataclass
class BrandBuilder:
    """Builder для данных бренда"""
    _name: str = field(default_factory=lambda: f"0 {fake.text(5).replace('.', '')}")
    _naming: str = field(default_factory=lambda: fake.lexify(text='?' * 4, letters=string.ascii_uppercase))
    _organization: str = "ООО Автотесты"
    _brand_awareness: str = "Высокая"

    def with_name(self, name: str) -> 'BrandBuilder':
        self._name = name
        return self

    def with_naming(self, naming: str) -> 'BrandBuilder':
        self._naming = naming
        return self

    def with_organization(self, org: str) -> 'BrandBuilder':
        self._organization = org
        return self

    def with_brand_awareness(self, awareness: str) -> 'BrandBuilder':
        self._brand_awareness = awareness
        return self

    def with_random_data(self) -> 'BrandBuilder':
        """Заполнить случайными данными"""
        self._name = f"0 {fake.text(5).replace('.', '')}"
        self._naming = fake.lexify(text='?' * 4, letters=string.ascii_uppercase)
        return self

    def build(self) -> dict:
        return {
            'name': self._name,
            'naming': self._naming,
            'organization': self._organization,
            'brand_awareness': self._brand_awareness,
        }


# === Фабрика для удобства ===
class BrandDataFactory:
    """Фабрика создания данных бренда"""
    
    @staticmethod
    def create_default() -> dict:
        return BrandBuilder().build()

    @staticmethod
    def create_with_name(name: str) -> dict:
        return BrandBuilder().with_name(name).build()

    @staticmethod
    def create_random() -> dict:
        return BrandBuilder().with_random_data().build()
```

**Использование в тестах:**
```python
# Вместо make_data_all_brand_fields()
data = BrandDataFactory.create_default()
data = BrandBuilder().with_name("Test Brand").with_random_data().build()
```

---

### Этап 5: Repository Pattern для API

**Цель:** Унифицировать доступ к API

```python
# admin_office/api_repositories/base_repository.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class BaseRepository(ABC):
    """Базовый репозиторий для API операций"""

    def __init__(self, token: str) -> None:
        self._token = token

    @abstractmethod
    def create(self, data: dict) -> T:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass


# admin_office/api_repositories/brand_repository.py
from dataclasses import dataclass
from typing import Optional
from admin_office.api_repositories.base_repository import BaseRepository
from http_methods.post import post_request

@dataclass
class Brand:
    id: str
    name: str
    naming: str
    client_id: Optional[str] = None

class BrandRepository(BaseRepository):
    """Репозиторий для работы с брендами через API"""

    def create(self, data: dict) -> Brand:
        query = {
            'operation_name': 'BrandCreate',
            'variables': {'data': data},
            'query': 'mutation BrandCreate($clientID: ID, $data: BrandData!) { brandCreate(clientID: $clientID, data: $data) {id}}',
        }
        result = post_request(query, self._token)
        return Brand(id=result['data']['brandCreate']['id'], **data)

    def get_by_id(self, id: str) -> Optional[Brand]:
        query = {
            'operationName': 'adminBrand',
            'variables': {'id': id},
            'query': 'query adminBrand($id: ID!) { adminBrand(id: $id) { id name naming } }',
        }
        result = post_request(query, self._token)
        data = result.get('data', {}).get('adminBrand')
        return Brand(**data) if data else None

    def delete(self, id: str) -> bool:
        query = {
            'operationName': 'adminBrandDelete',
            'variables': {'id': id},
            'query': 'mutation adminBrandDelete($id: ID!) { adminBrandDelete(id: $id) }',
        }
        result = post_request(query, self._token)
        return result == {'data': {'adminBrandDelete': True}}

    def get_count(self) -> int:
        query = {
            'operationName': 'adminBrands',
            'query': 'query adminBrands { adminBrands {id} }',
        }
        return len(post_request(query, self._token)['data']['adminBrands'])
```

---

### Этап 6: Улучшение BasePage (Facade)

```python
# admin_office/components/base_page.py
from playwright.sync_api import Page, Response
from dataclasses import dataclass
import requests

@dataclass
class NavigationContext:
    """Контекст навигации"""
    previous_url: str = ""
    current_url: str = ""

class BasePage:
    """Базовый класс для всех страниц - Facade"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self._navigation = NavigationContext()

    @property
    def sidebar(self):
        """Lazy loading SideBar"""
        from admin_office.components.models.ui.sidebar import SideBar
        return SideBar(self.page)

    @property
    def url(self) -> str:
        return self.page.url

    def visit(self, url: str) -> Response:
        """Посещение URL с логированием"""
        with allure.step(f'Opening URL: {url}'):
            self._navigation.previous_url = self.url
            response = requests.get(url, verify=False)
            return self.page.goto(response.url)

    def reload(self) -> Response:
        return self.page.reload(wait_until='domcontentloaded')

    def should_be_on_page(self, expected_url_fragment: str) -> bool:
        """Проверка что мы на правильной странице"""
        return expected_url_fragment in self.page.url

    # === FLUENT NAVIGATION ===
    def then_go_to(self, page_type: 'PageType') -> 'BasePage':
        """Фluent навигация к следующей странице"""
        return PageFactory.create(self.page, page_type)
```

---

## Структура после рефакторинга

```
admin_office/
├── api_repositories/              # NEW: Repository Pattern
│   ├── base_repository.py
│   ├── brand_repository.py
│   └── __init__.py
├── components/
│   ├── base_page.py               # UPDATED: Facade
│   ├── pages/
│   │   ├── page_factory.py        # NEW: Factory Method
│   │   └── brands/brands_page.py
│   └── models/ui/
│       └── sidebar/
│           ├── sidebar.py         # UPDATED: Facade
│           └── sidebar_config.py  # NEW: Configuration
├── data_builders/                 # NEW: Builder Pattern
│   ├── base_builder.py
│   ├── brand_builder.py
│   └── __init__.py
├── api_interactions/             # DEPRECATED: перенести в repositories
│   └── brands/brands_api_interactions.py
└── tests/
    └── ui/dictionaries/brands/test_brands.py
```

---

## Порядок внедрения

| Этап | Название | Сложность | Время | Приоритет | Статус |
|------|----------|-----------|-------|-----------|--------|
| 1 | Factory components (fluent assertions) | Низкая | 1ч | **P0** | ✅ Выполнен |
| 2 | SideBar Facade | Средняя | 2ч | **P0** | ✅ Выполнен |
| 3 | PageFactory | Низкая | 1ч | **P1** | ✅ Выполнен |
| 4 | BasePage improvements | Средняя | 1ч | **P1** | ✅ Выполнен |
| 5 | Builder Pattern (data) | Средняя | 2ч | **P1** | ✅ Выполнен |
| 6 | Repository Pattern (API) | Высокая | 3ч | **P2** | ✅ Выполнен |

---

## Критерии завершения

- [x] Все `should_*` методы возвращают `self` (fluent interface)
- [x] SideBar содержит ≤5 публичных методов
- [x] PageFactory создаёт все страницы
- [x] BrandBuilder используется в тестах
- [x] BrandRepository заменяет brands_api_interactions
- [ ] Нет закомментированного кода в активных файлах

---

## Новые файлы

```
admin_office/
├── api_repositories/                 # ✅ NEW: Repository Pattern
│   ├── __init__.py
│   ├── base_repository.py
│   └── brand_repository.py
├── data_builders/                   # ✅ NEW: Builder Pattern
│   ├── __init__.py
│   ├── base_builder.py
│   └── brand_builder.py
└── components/
    └── pages/
        └── page_factory.py          # ✅ NEW: PageFactory

admin_office/components/models/ui/
└── sidebar/                         # ✅ REFACTORED: Facade
    ├── __init__.py
    ├── sidebar_config.py
    └── sidebar.py
```

---

## Использование

### Fluent assertions:
```python
# Было:
button.should_be_visible()
button.click()

# Стало:
button.should_be_visible().click()
```

### SideBar навигация:
```python
# Было:
side_bar.check_brands_link()
side_bar.check_clients_link()

# Стало:
side_bar.navigate_to('Бренды')
side_bar.navigate_to('Клиенты')
```

### PageFactory:
```python
page = PageFactory.create(page, PageType.BRANDS)
```

### Builder:
```python
data = BrandDataFactory.create_default()
data = BrandBuilder().with_name("X").with_random_data().build()
```

### Repository:
```python
repo = BrandRepository(token)
brand = repo.create({'name': 'Test', 'naming': 'TEST'})
count = repo.get_count()
repo.delete(brand.id)
```
