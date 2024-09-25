import pytest
from unittest.mock import patch, MagicMock
from main import main
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("INPUT_SOURCE", "api")
    monkeypatch.setenv("API_URL", "https://mock-api.example.com")
    monkeypatch.setenv("API_KEY", "mock-api-key")


@pytest.fixture
def mock_api_response():
    return {
        "data": {
            "Primary_FirstName": "John",
            "Primary_LastName": "Doe",
            "Primary_BirthDate": "1980-01-01T00:00:00",
            "Primary_Age": 43,
            "Primary_GenderID": "Male",
            "Primary_Email": "john.doe@example.com",
            "Primary_Phone": "123-456-7890",
            "Primary_Blind": False,
            "Spouse_FirstName": "Jane",
            "Spouse_LastName": "Doe",
            "Spouse_BirthDate": "1982-01-01T00:00:00",
            "Spouse_Age": 41,
            "Spouse_GenderID": "Female",
            "Spouse_Email": "jane.doe@example.com",
            "Spouse_Phone": "987-654-3210",
            "Spouse_Blind": False,
            "SSCalData": {
                "Primary_PIA": 2000,
                "Primary_FRA": "2047-01-01T00:00:00",
                "Primary_FRAAge": 67,
                "Primary_HasFullCoverage": True,
                "Primary_IsDisabled": False,
                "Primary_HasChildren": False,
                "Primary_HasPension": False,
                "Primary_IsCollectingBenefits": False,
                "Primary_IsRemarried": False,
                "Primary_MarriedBefore60": False,
                "Primary_MarriedOver10Years": False,
                "Primary_CalBasis": "PIA",
                "Primary_EstRetirementAge": 65,
                "Primary_HowCalBenefits": "Standard",
                "Primary_BenefitsStartDate": None,
                "Primary_DivorceDate": None,
                "Primary_EntitlementDate": None,
                "Primary_AnualEarningRate": 50000,
                "Primary_AnualPartTimeEarningRate": 0,
                "Primary_BenefitsAmount": 0,
                "Primary_DisabilityBenefit": 0,
                "Primary_PenAmount": 0,
                "Primary_PenSalarySS": 0,
                "Primary_PIA62": 1800,
                "Primary_PIA70": 2200,
                "Primary_QEAvgSalary": 45000,
                "Primary_SSPIA": 2000,
                "Primary_SSEarning": 50000,
                "Primary_WEPBendRate": 0,
                "Primary_FRAYear": 2047,
                "Primary_LastYearEarningsAge": 65,
                "Primary_LastYearPartTimeEarningsAge": 0,
                "Primary_LifeExpectancy": 85,
                "Primary_QEYearsWorked": 20,
                "Spouse_PIA": 1800,
                "Spouse_FRA": "2049-01-01T00:00:00",
                "Spouse_FRAAge": 67,
                "Spouse_HasFullCoverage": True,
                "Spouse_IsDisabled": False,
                "Spouse_HasPension": False,
                "Spouse_IsCollectingBenefits": False,
                "Spouse_IsLiving": True,
                "Spouse_CalBasis": "PIA",
                "Spouse_EstRetirementAge": 65,
                "Spouse_HowCalBenefits": "Standard",
                "Spouse_BenefitsStartDate": None,
                "Spouse_EntitlementDate": None,
                "Spouse_AnualEarningRate": 45000,
                "Spouse_AnualIncome": 45000,
                "Spouse_AnualPartTimeEarningRate": 0,
                "Spouse_BenefitAmount": 0,
                "Spouse_DisabilityBenefit": 0,
                "Spouse_PenAmount": 0,
                "Spouse_PenSalarySS": 0,
                "Spouse_PIA62": 1600,
                "Spouse_PIA70": 2000,
                "Spouse_QEAvgSalary": 40000,
                "Spouse_SSPIA": 1800,
                "Spouse_SSEarning": 45000,
                "Spouse_WEPBendRate": 0,
                "Spouse_FRAYear": 2049,
                "Spouse_LastYearEarningsAge": 65,
                "Spouse_LastYearPartTimeEarningsAge": 0,
                "Spouse_LifeExpectancy": 88,
                "Spouse_QEYearsWorked": 18,
                "SSCalEarnings": [
                    {"YearID": 2023, "Earning": 50000, "IsPrimary": True},
                    {"YearID": 2022, "Earning": 48000, "IsPrimary": True},
                    {"YearID": 2021, "Earning": 46000, "IsPrimary": True},
                    {"YearID": 2023, "Earning": 45000, "IsPrimary": False},
                    {"YearID": 2022, "Earning": 43000, "IsPrimary": False},
                    {"YearID": 2021, "Earning": 41000, "IsPrimary": False},
                ],
                "SSCalChildren": [],
                "SSCalPensions": [],
            },
            "MaritalStatus": 2,
            "Settings": {
                "COLA": 2.5,
                "InflationRate": 2.0,
                "NominalRateOfReturn": 6.0,
                "RealRateOfReturn": 4.0,
            },
        }
    }


@pytest.fixture
def mock_input_handler(mock_api_response):
    mock_handler = MagicMock()
    mock_handler.get_input.return_value = mock_api_response
    return mock_handler


@pytest.fixture
def mock_openai_provider():
    mock_provider = MagicMock()
    mock_provider.analyze.return_value = (
        "<html><body><h1>Analysis Result</h1></body></html>"
    )
    return mock_provider


@patch("main.get_input_handler")
@patch("main.get_openai_provider")
@patch("main.validate_llm_html")
@patch("main.get_output_handler")
@patch("main.preprocess_roadmap_output")
def test_main_function(
    mock_preprocess,
    mock_output_handler,
    mock_validate_llm_html,
    mock_get_openai_provider,
    mock_get_input_handler,
    mock_env_vars,
    mock_input_handler,
    mock_openai_provider,
):
    # Set up mocks
    mock_get_input_handler.return_value = mock_input_handler
    mock_get_openai_provider.return_value = mock_openai_provider
    mock_validate_llm_html.return_value = (True, "")
    mock_output = MagicMock()
    mock_output_handler.return_value = mock_output
    mock_preprocess.return_value = "Preprocessed data"

    # Run the main function
    try:
        main()
    except Exception as e:
        logger.exception(f"An error occurred in main: {str(e)}")
        pytest.fail(f"main() raised {type(e).__name__} unexpectedly!")

    # Assertions with logging
    logger.debug("Checking if get_input_handler was called...")
    mock_get_input_handler.assert_called_once_with(
        "api", api_url="https://mock-api.example.com", api_key="mock-api-key"
    )

    logger.debug("Checking if get_input was called...")
    mock_input_handler.get_input.assert_called_once()

    logger.debug("Checking if preprocess_roadmap_output was called...")
    mock_preprocess.assert_called_once()

    logger.debug("Checking if get_openai_provider was called...")
    mock_get_openai_provider.assert_called_once()

    logger.debug("Checking if analyze was called...")
    mock_openai_provider.analyze.assert_called_once()

    logger.debug("Checking if validate_llm_html was called...")
    mock_validate_llm_html.assert_called_once()

    logger.debug("Checking if process_output was called...")
    mock_output.process_output.assert_called_once()


@patch("main.get_input_handler")
@patch("main.get_openai_provider")
@patch("main.validate_llm_html")
@patch("main.get_output_handler")
@patch("main.preprocess_roadmap_output")
def test_main_function_no_spouse(
    mock_preprocess,
    mock_output_handler,
    mock_validate_llm_html,
    mock_get_openai_provider,
    mock_get_input_handler,
    mock_env_vars,
    mock_input_handler,
    mock_openai_provider,
):
    # Modify mock_api_response to remove spouse data
    mock_api_response = mock_input_handler.get_input.return_value
    del mock_api_response["data"]["Spouse_FirstName"]
    del mock_api_response["data"]["Spouse_LastName"]
    del mock_api_response["data"]["Spouse_Age"]
    del mock_api_response["data"]["Spouse_BirthDate"]
    del mock_api_response["data"]["Spouse_GenderID"]
    del mock_api_response["data"]["Spouse_Email"]
    del mock_api_response["data"]["Spouse_Blind"]
    del mock_api_response["data"]["Spouse_Phone"]

    # Set up mocks
    mock_get_input_handler.return_value = mock_input_handler
    mock_get_openai_provider.return_value = mock_openai_provider
    mock_validate_llm_html.return_value = (True, "")
    mock_output = MagicMock()
    mock_output_handler.return_value = mock_output
    mock_preprocess.return_value = "Preprocessed data without spouse"

    # Run the main function
    try:
        main()
    except Exception as e:
        logger.exception(f"An error occurred in main (no spouse): {str(e)}")
        pytest.fail(f"main() (no spouse) raised {type(e).__name__} unexpectedly!")

    # Assertions
    mock_get_input_handler.assert_called_once_with(
        "api", api_url="https://mock-api.example.com", api_key="mock-api-key"
    )
    mock_input_handler.get_input.assert_called_once()
    mock_preprocess.assert_called_once()
    mock_get_openai_provider.assert_called_once()
    mock_openai_provider.analyze.assert_called_once()
    mock_validate_llm_html.assert_called_once()
    mock_output.process_output.assert_called_once()
