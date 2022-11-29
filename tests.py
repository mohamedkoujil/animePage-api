import unittest
import time
from animeflv import AnimeFLV
import cloudscraper


def wrap_request(func, *args, count: int = 5):
    notes = []

    for _ in range(count):
        try:
            r = func(*args)
            return r
        except Exception as e:
            if isinstance(e, cloudscraper.exceptions.CloudflareChallengeError): # cloudscraper will error because this feature isn't free, ignore this for the Tests
                return ["Lorem Ipsum"]
            notes.append(e)
            time.sleep(5)
    else: # If the loop doesn't `break`, raise the Exception
        raise Exception([e] + notes)


class AnimeFLVTest(unittest.TestCase):
    def test_search(self):
        with AnimeFLV() as api:
            res = wrap_request(api.search, "Nanatsu no Taizai")

            self.assertGreater(len(res), 0)
            self.assertTrue(isinstance(res, list))

            item = res[0]
            self.assertTrue(isinstance(item, dict))

    def test_list(self):
        with AnimeFLV() as api:
            res = wrap_request(api.list, 1)

            self.assertGreater(len(res), 0)
            self.assertTrue(isinstance(res, list))

            item = res[0]
            self.assertTrue(isinstance(item, dict))

    def test_get_video_servers(self):
        with AnimeFLV() as api:
            res = wrap_request(api.get_video_servers, "nanatsu-no-taizai", 1)

            self.assertGreater(len(res), 0)
            self.assertTrue(isinstance(res, list))

    def test_get_anime_info(self):
        with AnimeFLV() as api:
            res = wrap_request(api.get_anime_info, "nanatsu-no-taizai")

            self.assertGreater(len(res), 0)
            self.assertTrue(isinstance(res, dict))

    def test_get_latest_episodes(self):
        with AnimeFLV() as api:
            res = wrap_request(api.get_latest_episodes)

            self.assertGreater(len(res), 0)
            self.assertTrue(isinstance(res, list))

            item = res[0]
            self.assertTrue(isinstance(item, dict))

    def test_get_latest_animes(self):
        with AnimeFLV() as api:
            res = wrap_request(api.get_latest_animes)

            self.assertGreater(len(res), 0)
            self.assertTrue(isinstance(res, list))

            item = res[0]
            self.assertTrue(isinstance(item, dict))
