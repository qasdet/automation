# Спецификация архитектурных изменений

## Оглавление
1. [Factory Pattern (Fluent Interface)](#1-factory-pattern-fluent-interface)
2. [Facade Pattern (SideBar)](#2-facade-pattern-sidebar)
3. [Factory Method (PageFactory)](#3-factory-method-pagefactory)
4. [Builder Pattern (Test Data)](#4-builder-pattern-test-data)
5. [Repository Pattern (API)](#5-repository-pattern-api)
6. [Обратная совместимость](#6-обратная-совместимость)

---

## 1. Factory Pattern (Fluent Interface)

### Что было ДО

```python
# controller/factory.py
class Factory(ABC):
    def should_be_visible(self, **kwargs) -> None:  # ❌ Не возвращает результат
        expect(...).to_be_visible()

    def click(self, **kwargs) -> None:  # ❌ Не возвращает результат
        locator.click()

# Использование:
button.should_be_visible()  # Отдельная строка
button.click()              # Еще одна строка
```

### Что стало ПОСЛЕ

```python
# controller/factory.py
class Factory(ABC):
    def should_be_visible(self, **kwargs) -> 'Factory':  # ✅ Возвращает self
        expect(...).to_be_visible()
        return self

    def click(self, **kwargs) -> 'Factory':  # ✅ Возвращает self
        locator.click()
        return self

# Использование:
button.should_be_visible().click()  # ✅ Цепочка вызовов
```

### Почему это улучшение

| До | После |
|----|-------|
| 3 строки на простое действие | 1 строка |
| Нельзя объединить проверку и действие | Fluent interface |
| Каждый метод возвращал `None` | Методы возвращают `self` |

### Измененные файлы

```
controller/
├── factory.py          # Ядро - все should_* и action методы возвращают self
├── button.py          # Удалены унаследованные click(), hover()
├── input.py           # Удалены унаследованные fill(), should_have_value()
├── drop_down_list.py  # Удалены унаследованные click(), should_have_text()
├── grid.py            # Все should_* и click_* возвращают self
├── table_new.py       # Все should_* и click_* возвращают self
├── title.py           # Удален дублирующий should_have_text()
├── link.py            # Только type_of property
├── navigation_menu.py # goto() возвращает self
├── paging.py          # go_to_next/prev_page() возвращают self
├── tabbar.py          # Все методы возвращают self
├── cell.py            # Только type_of property
├── context_menu.py    # click_item() возвращает self
├── date_picker.py     # fill() возвращает self
├── file.py            # Только type_of property
├── list_item.py       # Только type_of property
└── alphanumeric_element.py  # Только type_of property
```

### Примеры fluent цепочек

```python
# Было (4 строки):
button.should_be_visible()
button.hover()
button.click()
input.should_have_value("text")

# Стало (1 строка):
button.should_be_visible().hover().click()
input.should_have_value("text")

# Более сложный пример:
table.should_have_count_row(10).click_cell_in_row_by_num(1, 2).should_be_visible()
```

---

## 2. Facade Pattern (SideBar)

### Что было ДО (God Object)

```python
# admin_office/components/models/ui/side_bar/side_bar.py
class SideBar:
    def __init__(self, page):
        # 40+ ссылок создавались в __init__
        self.main_link = Link(...)
        self.users_link = Link(...)
        # ... еще 38 таких же

    # 40+ методов check_*() - ВСЕ ДУБЛИРУЮТ ОДНУ ЛОГИКУ
    def check_brands_link(self): self.brands_link.click()
    def check_users_link(self): self.users_link.click()
    def check_organizations_link(self): self.organizations_link.click()
    # ... и так для КАЖДОГО пункта меню
```

**Проблема:** При добавлении нового пункта меню нужно:
1. Добавить поле `self.xxx_link = Link(...)`
2. Добавить метод `def check_xxx_link(self)`
3. Дублировать код 40+ раз

### Что стало ПОСЛЕ (Facade + Configuration)

```python
# admin_office/components/models/ui/sidebar/sidebar_config.py
class MenuItem:
    name: str      # "Бренды"
    testid: str    # "sidebar_brands"
    category: MenuCategory
    has_hover: bool = False

class SideBar:
    ITEMS = [
        MenuItem('Главная', 'sidebar_home', MenuCategory.MAIN),
        MenuItem('Бренды', 'sidebar_brands', MenuCategory.DICTIONARIES),
        # Легко добавить новый пункт - одна строка
    ]

# admin_office/components/models/ui/sidebar/sidebar.py
class SideBar:
    def navigate_to(self, item_name: str) -> 'SideBar':
        """ОДИН метод вместо 40+"""
        link = self._links[item_name]  # Словарь, не 40 полей
        link.click()
        return self
```

### Структура нового SideBar

```
sidebar/
├── sidebar_config.py   # ДАННЫЕ: MenuItem, MenuCategory, ITEMS
├── sidebar.py          # ЛОГИКА: navigate_to(), deprecated check_*()
└── __init__.py
```

### Почему это улучшение

| До | После |
|----|-------|
| 40+ методов `check_*()` | 1 метод `navigate_to()` |
| Добавление меню = 2 изменения | Добавление меню = 1 строка |
| Конфигурация смешана с логикой | Конфигурация отделена |
| 350+ строк кода | ~100 строк |

### Примеры использования

```python
# Было:
side_bar.check_brands_link()
side_bar.check_clients_link()
side_bar.check_channels_link()

# Стало:
side_bar.navigate_to('Бренды')
side_bar.navigate_to('Клиенты')
side_bar.navigate_to('Каналы')

# Fluent:
side_bar.navigate_to('Бренды').navigate_to('Клиенты')
```

### Обратная совместимость

Старые методы сохранены, но выдают warning:

```python
def check_brands_link(self):
    warnings.warn(
        "Use navigate_to('Бренды') instead",
        DeprecationWarning
    )
    self.navigate_to('Бренды')
```

---

## 3. Factory Method (PageFactory)

### Что было ДО

```python
# admin_office/conftest.py
@pytest.fixture
def admin_brands_page(chromium_page):
    return AdminOfficeBrandsPage(chromium_page)  # Прямое создание

@pytest.fixture
def admin_organizations_page(chromium_page):
    return AdminOfficeOrganizationsPage(chromium_page)

@pytest.fixture
def admin_clients_page(chromium_page):
    return AdminOfficeClientsPage(chromium_page)

# ... и так для каждой страницы
```

**Проблема:**
- Нет стандартизации создания страниц
- Сложно добавить новую страницу (нужно помнить где какой fixture)
- Нет единой точки создания всех page objects

### Что стало ПОСЛЕ

```python
# admin_office/components/pages/page_factory.py
class PageType(Enum):
    BRANDS = auto()
    ORGANIZATIONS = auto()
    CHANNELS = auto()
    # Легко добавить новый тип

class PageFactory:
    _registry: dict[PageType, Type[BasePage]] = {}

    @classmethod
    def register(cls, page_type: PageType):
        def decorator(page_class):
            cls._registry[page_type] = page_class
            return page_class
        return decorator

    @classmethod
    def create(cls, page: Page, page_type: PageType) -> BasePage:
        return cls._registry[page_type](page)

# Автоматическая регистрация при импорте:
@PageFactory.register(PageType.BRANDS)
class AdminOfficeBrandsPage(BasePage):
    pass
```

### Использование

```python
# В fixture:
@pytest.fixture
def admin_brands_page(chromium_page):
    return PageFactory.create(chromium_page, PageType.BRANDS)

# Или напрямую в тесте:
page = PageFactory.create(page, PageType.BRANDS)
```

### Почему это улучшение

| До | После |
|----|-------|
| 15+ fixture функций | 1 PageFactory |
| Нет стандартизации | Единая точка создания |
| Добавление страницы = новый fixture | Добавление = декоратор у класса |

---

## 4. Builder Pattern (Test Data)

### Что было ДО (Процедурный стиль)

```python
# admin_office/tests/api/dictionaries/brands/data_make_for_brands.py
def brand_name():
    return f"0 {fake.text(5)}"

def brand_naming():
    return fake.lexify(text='?' * 4)

def make_data_all_brand_fields():
    return {
        'name': brand_name(),
        'naming': brand_naming(),
        'organization': ORGANIZATION,
        'brand_awareness': BRAND_AWARENESS,
    }
```

**Проблемы:**
- Нельзя переопределить отдельные поля
- Сложно создать вариации (например, только name)
- Данные создаются за один вызов, нет контроля

### Что стало ПОСЛЕ (Builder + Factory)

```python
# admin_office/data_builders/brand_builder.py
class BrandBuilder:
    def __init__(self):
        self.reset()

    def with_name(self, name: str) -> 'BrandBuilder':
        self._name = name
        return self

    def with_naming(self, naming: str) -> 'BrandBuilder':
        self._naming = naming
        return self

    def with_random_data(self) -> 'BrandBuilder':
        self._name = f"0 {fake.text(5)}"
        self._naming = fake.lexify(text='?' * 4)
        return self

    def build(self) -> dict:
        return {
            'name': self._name,
            'naming': self._naming,
            'organization': self._organization,
            'brand_awareness': self._brand_awareness,
        }


class BrandDataFactory:
    @staticmethod
    def create_default() -> dict:
        return BrandBuilder().build()

    @staticmethod
    def create_random() -> dict:
        return BrandBuilder().with_random_data().build()
```

### Примеры использования

```python
# Все значения по умолчанию:
data = BrandDataFactory.create_default()

# Все случайные значения:
data = BrandDataFactory.create_random()

# Только имя кастомное, остальное случайное:
data = BrandBuilder().with_name("My Brand").with_random_data().build()

# Только имя кастомное, остальное по умолчанию:
data = BrandBuilder().with_name("My Brand").build()

# Все поля кастомные:
data = (
    BrandBuilder()
    .with_name("Brand X")
    .with_naming("BRANDX")
    .with_organization("ООО Тест")
    .with_brand_awareness("Высокая")
    .build()
)
```

### Почему это улучшение

| До | После |
|----|-------|
| Фиксированный набор данных | Гибкое создание вариаций |
| Нет контроля над полями | Любое поле можно переопределить |
| 3+ функции для одного объекта | 1 класс BrandBuilder |
| Процедурный стиль | Fluent interface |

---

## 5. Repository Pattern (API)

### Что было ДО (Разрозненные функции)

```python
# admin_office/api_interactions/brands/brands_api_interactions.py
def brand_creation(brand_data, user_office_token):
    query = {...}
    result = post_request(query, user_office_token)
    return result['data']['brandCreate']['id']

def delete_brand_by_id(id_brand, token):
    query = {...}
    response = post_request(query, token)
    assert response == {...}

def get_count_of_brands(token):
    query = {...}
    return len(post_request(query, token)['data']['adminBrands'])
```

**Проблемы:**
- Нет единого интерфейса
- Каждая функция требует ручной передачи токена
- Нет модели данных (возвращают dict, а не объекты)
- Сложно тестировать изолированно

### Что стало ПОСЛЕ (Repository)

```python
# admin_office/api_repositories/base_repository.py
class BaseRepository(ABC):
    def __init__(self, token: dict):
        self._token = token

    def _execute_query(self, query: dict) -> dict:
        return post_request(query, self._token)

    @abstractmethod
    def create(self, data: dict): ...
    @abstractmethod
    def get_by_id(self, id: str): ...
    @abstractmethod
    def delete(self, id: str) -> bool: ...
    @abstractmethod
    def get_count(self) -> int: ...


# admin_office/api_repositories/brand_repository.py
@dataclass
class Brand:
    id: str
    name: str
    naming: str
    client_id: str | None = None

class BrandRepository(BaseRepository):
    def create(self, data: dict) -> Brand:
        query = {...}
        result = self._execute_query(query)
        return Brand.from_dict(result['data']['brandCreate'])

    def get_by_id(self, id: str) -> Brand | None:
        ...

    def delete(self, id: str) -> bool:
        ...

    def get_count(self) -> int:
        query = {...}
        return len(self._execute_query(query).get('data', {}).get('adminBrands', []))
```

### Использование

```python
# Токен передается один раз при создании репозитория:
repo = BrandRepository({'admin-authorization': 'Bearer xxx'})

# Все методы используют этот токен:
brand = repo.create({'name': 'Test', 'naming': 'TEST'})
count = repo.get_count()
repo.delete(brand.id)

# Возвращает объекты, не dict:
print(brand.name, brand.naming)
```

### Почему это улучшение

| До | После |
|----|-------|
| Функции требуют токен каждый раз | Токен передается при инициализации |
| Возвращают dict | Возвращают типизированные объекты (Brand) |
| Нет стандартизации | Единый интерфейс BaseRepository |
| Сложно мокать | Легко тестировать изолированно |

---

## 6. Обратная совместимость

### Стратегия

Все старые модули сохранены, но отмечены как deprecated:

```python
# admin_office/api_interactions/brands/brands_api_interactions.py
"""@deprecated Use admin_office.api_repositories.BrandRepository instead"""
from admin_office.api_repositories import BrandRepository

def delete_brand_by_id(id_brand: int, token: str) -> None:
    """@deprecated Use BrandRepository.delete() instead"""
    BrandRepository(token).delete(str(id_brand))

def get_count_of_brands(token: str) -> int:
    """@deprecated Use BrandRepository.get_count() instead"""
    return BrandRepository(token).get_count()
```

### SideBar deprecated методы

```python
def check_brands_link(self):
    warnings.warn(
        "Use navigate_to('Бренды') instead",
        DeprecationWarning
    )
    self.navigate_to('Бренды')
```

---

## Итоговая структура после рефакторинга

```
admin_office/
├── api_repositories/                    # ✅ NEW
│   ├── __init__.py
│   ├── base_repository.py             # Абстрактный базовый класс
│   └── brand_repository.py            # Реализация для брендов
├── api_interactions/                   # ⏪ DEPRECATED (wrapper)
│   └── brands/
│       └── brands_api_interactions.py # Прокси к BrandRepository
├── components/
│   ├── base_page.py                   # ✅ Упрощен
│   ├── models/ui/
│   │   └── sidebar/                   # ✅ REFACTORED
│   │       ├── sidebar_config.py      # Конфигурация меню
│   │       ├── sidebar.py             # Facade с navigate_to()
│   │       └── __init__.py
│   └── pages/
│       ├── page_factory.py           # ✅ NEW
│       └── ...
├── data_builders/                     # ✅ NEW
│   ├── __init__.py
│   ├── base_builder.py
│   └── brand_builder.py
└── tests/
    └── ui/dictionaries/brands/
        └── test_brands.py            # ✅ Обновлен
```

---

## Паттерны - итоговая таблица

| Паттерн | До | После | Зачем |
|---------|-----|------|-------|
| **Factory** | Методы возвращали `None` | Методы возвращают `self` | Fluent interface, цепочки вызовов |
| **Facade** | 40+ методов `check_*()` | 1 метод `navigate_to()` + конфиг | Убрать дублирование, легко добавлять |
| **Factory Method** | 15+ fixtures | 1 `PageFactory.create()` | Стандартизация, единая точка входа |
| **Builder** | Функции `make_*()` | `BrandBuilder` с fluent | Гибкое создание вариаций данных |
| **Repository** | Функции `*_api()` | `BrandRepository` класс | Типизация, инкапсуляция, легко тестировать |
