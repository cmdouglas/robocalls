from dataclasses import dataclass, field


@dataclass
class Person():
    email: str = field(default='')
    given_name: str = field(default='')
    family_name: str = field(default='')
    postal_code: str = field(default='')
