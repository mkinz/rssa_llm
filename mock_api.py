import http.server
import socketserver
import json
from datetime import datetime, timedelta

# Sample data matching the format expected by roadmap_output_ingestor.py
sample_data = {
    "id": 21214,
    "name": "R Hall & R Munster",
    "advisor": {"Id": "64035a1d-a514-4e84-86f6-86f1db700243", "Name": "Corey Castillo"},
    "exported": "2024-08-30T15:01:25.9566996Z",
    "data": {
        "Address": "Anonymous",
        "City": "Transilvainia",
        "MaritalStatus": 2,
        "State": "CA",
        "Zip": "90123",
        "Primary_Age": 58,
        "Primary_BirthDate": "1966-06-06T00:00:00",
        "Primary_Blind": False,
        "Primary_Email": "anonymous@rssa.com",
        "Primary_FirstName": "R",
        "Primary_GenderID": "M",
        "Primary_LastName": "Hall",
        "Primary_Phone": "Anonymous",
        "Spouse_Age": 59,
        "Spouse_BirthDate": "1965-05-05T00:00:00",
        "Spouse_Blind": False,
        "Spouse_Email": "anonymous@rssa.com",
        "Spouse_FirstName": "R",
        "Spouse_GenderID": "F",
        "Spouse_LastName": "Munster",
        "Spouse_Phone": "Anonymous",
        "SSCalData": {
            "Primary_HasFullCoverage": True,
            "Primary_IsDisabled": False,
            "Primary_Blind": False,
            "Primary_HasChildren": False,
            "Primary_HasPension": False,
            "Primary_IsCollectingBenefits": False,
            "Primary_IsRemarried": True,
            "Primary_MarriedBefore60": True,
            "Primary_MarriedOver10Years": True,
            "Primary_CalBasis": 0,
            "Primary_EstRetirementAge": 0,
            "Primary_HowCalBenefits": 2,
            "Primary_BenefitsStartDate": None,
            "Primary_DivorceDate": "2020-05-18T04:00:00",
            "Primary_EntitlementDate": None,
            "Primary_FRA": "2033-06-05T00:00:00",
            "Primary_AnualEarningRate": 50000.0000,
            "Primary_AnualPartTimeEarningRate": 0.0000,
            "Primary_BenefitsAmount": None,
            "Primary_DisabilityBenefit": None,
            "Primary_PenAmount": None,
            "Primary_PenSalarySS": None,
            "Primary_PIA": 390.6000,
            "Primary_PIA62": 390.6000,
            "Primary_PIA70": 390.6000,
            "Primary_QEAvgSalary": None,
            "Primary_SSPIA": 0.0000,
            "Primary_SSEarning": None,
            "Primary_WEPBendRate": 0.0000,
            "Primary_FRAAge": 67,
            "Primary_FRAYear": 804,
            "Primary_LastYearEarningsAge": 56,
            "Primary_LastYearPartTimeEarningsAge": 0,
            "Primary_LifeExpectancy": 85,
            "Primary_QEYearsWorked": None,
            "Spouse_HasFullCoverage": True,
            "Spouse_IsDisabled": False,
            "Spouse_Blind": False,
            "Spouse_HasPension": False,
            "Spouse_IsCollectingBenefits": False,
            "Spouse_IsLiving": True,
            "Spouse_CalBasis": 0,
            "Spouse_EstRetirementAge": 0,
            "Spouse_HowCalBenefits": 2,
            "Spouse_BenefitsStartDate": None,
            "Spouse_DeathDate": None,
            "Spouse_EntitlementDate": None,
            "Spouse_FRA": "2032-05-04T00:00:00",
            "Spouse_AnualEarningRate": 60000.0000,
            "Spouse_AnualIncome": None,
            "Spouse_AnualPartTimeEarningRate": 0.0000,
            "Spouse_BenefitAmount": None,
            "Spouse_DisabilityBenefit": None,
            "Spouse_PenAmount": None,
            "Spouse_PenSalarySS": None,
            "Spouse_PIA": 282.6000,
            "Spouse_PIA62": 282.6000,
            "Spouse_PIA70": 282.6000,
            "Spouse_QEAvgSalary": None,
            "Spouse_SSPIA": 1560.0000,
            "Spouse_SSEarning": None,
            "Spouse_WEPBendRate": 0.0000,
            "Spouse_FRAAge": 67,
            "Spouse_FRAYear": 804,
            "Spouse_LastYearEarningsAge": 0,
            "Spouse_LastYearPartTimeEarningsAge": 0,
            "Spouse_LifeExpectancy": 90,
            "Spouse_QEYearsWorked": None,
            "SSCalChildren": [
                {
                    "Name": "Bill",
                    "BirthDate": "2009-09-09T04:00:00",
                    "Age": 12,
                    "HighSchoolGradDate": "2029-09-09T04:00:00",
                    "IsCollectingBenefits": False,
                    "BenefitsStartDate": None,
                    "BenefitsAmount": None,
                    "IsDisabled": True,
                    "DisabilityBenefit": None,
                    "SupplementalIncome": None,
                    "DependentType": 1,
                }
            ],
            "SSCalEarnings": [
                {
                    "YearID": 2022,
                    "IsPrimary": True,
                    "IsAssumed": False,
                    "Earning": 50000.0000,
                    "NCEarning": 0.0000,
                },
                {
                    "YearID": 2022,
                    "IsPrimary": False,
                    "IsAssumed": False,
                    "Earning": 60000.0000,
                    "NCEarning": 0.0000,
                },
            ],
            "SSCalPensions": [],
        },
        "Settings": {
            "COLA": 0.00,
            "InflationRate": 2.25,
            "NominalRateOfReturn": 3.75,
            "RealRateOfReturn": 1.47,
        },
    },
    "encrypted": False,
}


class MockAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(sample_data).encode())


def run_mock_api(port=8000):
    with socketserver.TCPServer(("", port), MockAPIHandler) as httpd:
        print(f"Serving mock API at port {port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_mock_api()
