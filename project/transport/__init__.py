from project.config import Config
from project.dal.retailer import RetailerRepository
from project.logger import Logger
from project.services.auth.auth_service import AuthService

config = Config()
logger = Logger()

retailer_repository = RetailerRepository(config, logger)

auth_service = AuthService(config, logger, retailer_repository)
