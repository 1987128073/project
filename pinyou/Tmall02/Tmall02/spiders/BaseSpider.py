from scrapy_redis.spiders import RedisSpider


class BaseSpider(RedisSpider):

    def next_requests(self):
        # self.environment_name = self.settings.get('ENVIRONMENT')
        """Returns a request to be scheduled or none."""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', False)
        fetch_one = self.server.spop if use_set else self.server.lpop
        # XXX: Do we need to use a timeout here?
        found = 0
        # TODO: Use redis pipeline execution.
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                # Queue empty.
                break
            reqs = self.make_request_from_data(data)
            if reqs:
                for req in reqs:
                    yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)