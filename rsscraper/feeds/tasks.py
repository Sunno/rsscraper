import logging
from config import celery_app
from .models import Feed


logger = logging.getLogger('celery')


@celery_app.task(name='fetch-feeds', bind=True)
def fetch_feeds(self, feeds=None):
    """
    Fetchs feeds in background
    @param feeds: a list of ids
    """
    updated = []
    failed = []
    if feeds:
        feeds = Feed.objects.filter(id__in=feeds)

    for feed in (feeds or Feed.objects.all()):
        parsed, valid = Feed.validate_url(feed.url)
        if valid:
            feed.set_content(parsed)
            feed.fetch()
            updated.append(feed)
        else:
            failed.append(feed)
            logger.error(
                'Error updating feed',
                extra={
                    'feed': feed,
                    'feed_id': feed.id,
                    'user': feed.user
                }
            )

    logger.info(
        'Updated {} feeds'.format(len(updated))
    )
    if len(failed) > 0:
        raise self.retry(
            args=([f.id for f in failed],),
            max_retries=3,
            countdown=30
        )

    return [f.id for f in updated]
