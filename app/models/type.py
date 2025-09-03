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

class ProjectStatusTypes(enum.Enum):
    ACTIVE = 'active'
    INPROGRESS = 'inprogress'
    COMPLETED = 'completed'
    ARCHIVED = 'archived'