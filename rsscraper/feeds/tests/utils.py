from django.conf import settings


URLS_MAP = {
    'https://atom1.0.com': {
        'path': settings.ROOT_DIR(
            'rsscraper/feeds/tests/examples/atom1.0.xml'),
        'empty_content': False
    },
    'https://atom0.3.com': {
        'path': settings.ROOT_DIR(
            'rsscraper/feeds/tests/examples/atom0.3.xml'),
        'empty_content': False
    },
    'https://rss2.0.com': {
        'path': settings.ROOT_DIR(
            'rsscraper/feeds/tests/examples/rss2.0.xml'),
        'empty_content': True
    },
    'https://rss2.0namespaced.com': {
        'path': settings.ROOT_DIR(
            'rsscraper/feeds/tests/examples/rss2.0namespaced.xml'),
        'empty_content': False
    },
    'https://rss1.0.com': {
        'path': settings.ROOT_DIR(
            'rsscraper/feeds/tests/examples/rss1.0.xml'),
        'empty_content': False
    },
    'http://www.nu.nl/rss/Algemeen': {
        'path': settings.ROOT_DIR(
            'rsscraper/feeds/tests/examples/algemeen.xml'),
        'empty_content': True,
        'count': 10
    },
    'https://feeds.feedburner.com/tweakers/mixed': {
        'path': settings.ROOT_DIR(
            'rsscraper/feeds/tests/examples/tweakers.xml'),
        'empty_content': True,
        'count': 40
    },
}
