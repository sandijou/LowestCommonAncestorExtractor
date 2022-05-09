from enum import Enum

# Different types of content extractors presented in Section 4.4.
class ContentExtractor(Enum):
    NaiveStyle = 1
    RenderedStyle = 2
    NaiveStyleAndShortTextExclusion = 3
    RenderedStyleAndShortTextExclusion = 4
