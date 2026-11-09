# Each module registers its pages with build.quiz_page / article_page / tool_page.
# Order here = order on the category pages.
# tools.py (the older calculators) is deliberately not loaded for now: Feng Shui is the only tool.
from . import quizzes, fengshui, scratch, wallpaper, names_fr, games  # meanings.py removed from the site for now  # names.py (older name articles) removed from the site  # noqa
