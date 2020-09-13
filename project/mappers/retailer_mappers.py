from project.dal.models import RetailerModel
from project.dtos.retailer import RetailerInputDTO, RetailerOutputDTO


def convert_input_dto_to_model(retailer_dto: RetailerInputDTO) -> RetailerModel:
    return RetailerModel(
        full_name=retailer_dto.full_name,
        document=retailer_dto.document,
        email=retailer_dto.email,
        password=retailer_dto.password,
    )


def convert_model_to_output_dto(retailer_model: RetailerModel) -> RetailerOutputDTO:
    return RetailerOutputDTO(
        full_name=retailer_model.full_name,
        document=retailer_model.document,
        email=retailer_model.email,
    )
