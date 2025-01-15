DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/dbname")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "new_applications")
producer = None
