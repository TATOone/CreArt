import enum

class RoleType(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'

class SkillLevelType(enum.Enum):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    PROFESSIONAL = 'professional'

class ThemeType(enum.Enum):
    DARK = 'dark'
    LIGHT = 'light'
