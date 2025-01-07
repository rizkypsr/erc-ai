import hishel
import logging

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("hishel.controller").setLevel(logging.DEBUG)

storage = hishel.InMemoryStorage()

controller = hishel.Controller(force_cache=True)
client = hishel.CacheClient(storage=storage, controller=controller)
