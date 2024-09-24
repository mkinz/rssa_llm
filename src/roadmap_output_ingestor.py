import json
from datetime import datetime


def get_primary(raw_data: dict):
    return {
        "name": f"{raw_data['data']['Primary_FirstName']} {raw_data['data']['Primary_LastName']}",
        "birth_date": datetime.strptime(
            raw_data["data"]["Primary_BirthDate"], "%Y-%m-%dT%H:%M:%S"
        ),
        "age": raw_data["data"]["Primary_Age"],
        "gender": raw_data["data"]["Primary_GenderID"],
        "email": raw_data["data"]["Primary_Email"],
        "phone": raw_data["data"]["Primary_Phone"],
        "blind": raw_data["data"]["Primary_Blind"],
        "pia": raw_data["data"]["SSCalData"]["Primary_PIA"],
        "fra": datetime.strptime(
            raw_data["data"]["SSCalData"]["Primary_FRA"], "%Y-%m-%dT%H:%M:%S"
        ),
        "fra_age": raw_data["data"]["SSCalData"]["Primary_FRAAge"],
        "has_full_coverage": raw_data["data"]["SSCalData"]["Primary_HasFullCoverage"],
        "is_disabled": raw_data["data"]["SSCalData"]["Primary_IsDisabled"],
        "has_children": raw_data["data"]["SSCalData"]["Primary_HasChildren"],
        "has_pension": raw_data["data"]["SSCalData"]["Primary_HasPension"],
        "is_collecting_benefits": raw_data["data"]["SSCalData"][
            "Primary_IsCollectingBenefits"
        ],
        "is_remarried": raw_data["data"]["SSCalData"]["Primary_IsRemarried"],
        "married_before_60": raw_data["data"]["SSCalData"]["Primary_MarriedBefore60"],
        "married_over_10_years": raw_data["data"]["SSCalData"][
            "Primary_MarriedOver10Years"
        ],
        "cal_basis": raw_data["data"]["SSCalData"]["Primary_CalBasis"],
        "est_retirement_age": raw_data["data"]["SSCalData"]["Primary_EstRetirementAge"],
        "how_cal_benefits": raw_data["data"]["SSCalData"]["Primary_HowCalBenefits"],
        "benefits_start_date": raw_data["data"]["SSCalData"][
            "Primary_BenefitsStartDate"
        ],
        "divorce_date": raw_data["data"]["SSCalData"]["Primary_DivorceDate"],
        "entitlement_date": raw_data["data"]["SSCalData"]["Primary_EntitlementDate"],
        "annual_earning_rate": raw_data["data"]["SSCalData"][
            "Primary_AnualEarningRate"
        ],
        "annual_part_time_earning_rate": raw_data["data"]["SSCalData"][
            "Primary_AnualPartTimeEarningRate"
        ],
        "benefits_amount": raw_data["data"]["SSCalData"]["Primary_BenefitsAmount"],
        "disability_benefit": raw_data["data"]["SSCalData"][
            "Primary_DisabilityBenefit"
        ],
        "pen_amount": raw_data["data"]["SSCalData"]["Primary_PenAmount"],
        "pen_salary_ss": raw_data["data"]["SSCalData"]["Primary_PenSalarySS"],
        "pia_62": raw_data["data"]["SSCalData"]["Primary_PIA62"],
        "pia_70": raw_data["data"]["SSCalData"]["Primary_PIA70"],
        "qe_avg_salary": raw_data["data"]["SSCalData"]["Primary_QEAvgSalary"],
        "sspia": raw_data["data"]["SSCalData"]["Primary_SSPIA"],
        "ss_earning": raw_data["data"]["SSCalData"]["Primary_SSEarning"],
        "wep_bend_rate": raw_data["data"]["SSCalData"]["Primary_WEPBendRate"],
        "fra_year": raw_data["data"]["SSCalData"]["Primary_FRAYear"],
        "last_year_earnings_age": raw_data["data"]["SSCalData"][
            "Primary_LastYearEarningsAge"
        ],
        "last_year_part_time_earnings_age": raw_data["data"]["SSCalData"][
            "Primary_LastYearPartTimeEarningsAge"
        ],
        "life_expectancy": raw_data["data"]["SSCalData"]["Primary_LifeExpectancy"],
        "qe_years_worked": raw_data["data"]["SSCalData"]["Primary_QEYearsWorked"],
    }


def get_spouse(raw_data: dict):
    return {
        "name": f"{raw_data['data']['Spouse_FirstName']} {raw_data['data']['Spouse_LastName']}",
        "birth_date": datetime.strptime(
            raw_data["data"]["Spouse_BirthDate"], "%Y-%m-%dT%H:%M:%S"
        ),
        "age": raw_data["data"]["Spouse_Age"],
        "gender": raw_data["data"]["Spouse_GenderID"],
        "email": raw_data["data"]["Spouse_Email"],
        "phone": raw_data["data"]["Spouse_Phone"],
        "blind": raw_data["data"]["Spouse_Blind"],
        "pia": raw_data["data"]["SSCalData"]["Spouse_PIA"],
        "fra": datetime.strptime(
            raw_data["data"]["SSCalData"]["Spouse_FRA"], "%Y-%m-%dT%H:%M:%S"
        ),
        "fra_age": raw_data["data"]["SSCalData"]["Spouse_FRAAge"],
        "has_full_coverage": raw_data["data"]["SSCalData"]["Spouse_HasFullCoverage"],
        "is_disabled": raw_data["data"]["SSCalData"]["Spouse_IsDisabled"],
        "has_pension": raw_data["data"]["SSCalData"]["Spouse_HasPension"],
        "is_collecting_benefits": raw_data["data"]["SSCalData"][
            "Spouse_IsCollectingBenefits"
        ],
        "is_living": raw_data["data"]["SSCalData"]["Spouse_IsLiving"],
        "cal_basis": raw_data["data"]["SSCalData"]["Spouse_CalBasis"],
        "est_retirement_age": raw_data["data"]["SSCalData"]["Spouse_EstRetirementAge"],
        "how_cal_benefits": raw_data["data"]["SSCalData"]["Spouse_HowCalBenefits"],
        "benefits_start_date": raw_data["data"]["SSCalData"][
            "Spouse_BenefitsStartDate"
        ],
        "death_date": raw_data["data"]["SSCalData"]["Spouse_DeathDate"],
        "entitlement_date": raw_data["data"]["SSCalData"]["Spouse_EntitlementDate"],
        "annual_earning_rate": raw_data["data"]["SSCalData"]["Spouse_AnualEarningRate"],
        "annual_income": raw_data["data"]["SSCalData"]["Spouse_AnualIncome"],
        "annual_part_time_earning_rate": raw_data["data"]["SSCalData"][
            "Spouse_AnualPartTimeEarningRate"
        ],
        "benefit_amount": raw_data["data"]["SSCalData"]["Spouse_BenefitAmount"],
        "disability_benefit": raw_data["data"]["SSCalData"]["Spouse_DisabilityBenefit"],
        "pen_amount": raw_data["data"]["SSCalData"]["Spouse_PenAmount"],
        "pen_salary_ss": raw_data["data"]["SSCalData"]["Spouse_PenSalarySS"],
        "pia_62": raw_data["data"]["SSCalData"]["Spouse_PIA62"],
        "pia_70": raw_data["data"]["SSCalData"]["Spouse_PIA70"],
        "qe_avg_salary": raw_data["data"]["SSCalData"]["Spouse_QEAvgSalary"],
        "sspia": raw_data["data"]["SSCalData"]["Spouse_SSPIA"],
        "ss_earning": raw_data["data"]["SSCalData"]["Spouse_SSEarning"],
        "wep_bend_rate": raw_data["data"]["SSCalData"]["Spouse_WEPBendRate"],
        "fra_year": raw_data["data"]["SSCalData"]["Spouse_FRAYear"],
        "last_year_earnings_age": raw_data["data"]["SSCalData"][
            "Spouse_LastYearEarningsAge"
        ],
        "last_year_part_time_earnings_age": raw_data["data"]["SSCalData"][
            "Spouse_LastYearPartTimeEarningsAge"
        ],
        "life_expectancy": raw_data["data"]["SSCalData"]["Spouse_LifeExpectancy"],
        "qe_years_worked": raw_data["data"]["SSCalData"]["Spouse_QEYearsWorked"],
    }


def get_children(raw_data: dict):
    children = []
    for child in raw_data["data"]["SSCalData"]["SSCalChildren"]:
        children.append(
            {
                "name": child["Name"],
                "birth_date": datetime.strptime(
                    child["BirthDate"], "%Y-%m-%dT%H:%M:%S"
                ),
                "age": child["Age"],
                "high_school_grad_date": datetime.strptime(
                    child["HighSchoolGradDate"], "%Y-%m-%dT%H:%M:%S"
                ),
                "is_collecting_benefits": child["IsCollectingBenefits"],
                "benefits_start_date": child["BenefitsStartDate"],
                "benefits_amount": child["BenefitsAmount"],
                "is_disabled": child["IsDisabled"],
                "disability_benefit": child["DisabilityBenefit"],
                "supplemental_income": child["SupplementalIncome"],
                "dependent_type": child["DependentType"],
            }
        )
    return children


def calculate_earnings_history(raw_data):
    primary_earnings = {}
    spouse_earnings = {}
    for entry in raw_data["data"]["SSCalData"]["SSCalEarnings"]:
        if entry["IsPrimary"]:
            primary_earnings[entry["YearID"]] = entry["Earning"]
        else:
            spouse_earnings[entry["YearID"]] = entry["Earning"]
    return primary_earnings, spouse_earnings


def preprocess_data_primary_and_spouse(raw_data: dict, primary: dict, spouse: dict):
    primary_earnings, spouse_earnings = calculate_earnings_history(raw_data=raw_data)

    # Calculate total years worked and total earnings
    primary_years_worked = sum(
        1 for earning in primary_earnings.values() if earning > 0
    )
    primary_total_earnings = sum(primary_earnings.values())
    spouse_years_worked = sum(1 for earning in spouse_earnings.values() if earning > 0)
    spouse_total_earnings = sum(spouse_earnings.values())

    preprocessed_data = f"""
Primary Beneficiary:
{format_person_data(primary, primary_years_worked, primary_total_earnings)}

Spouse:
{format_person_data(spouse, spouse_years_worked, spouse_total_earnings)}

Marital Status: {"Married" if raw_data['data']['MaritalStatus'] == 2 else "Other"}

Primary Beneficiary Earnings History:
{format_earnings_history(primary_earnings)}

Spouse Earnings History:
{format_earnings_history(spouse_earnings)}

Children:
{format_children_data(raw_data["data"]["SSCalData"]["SSCalChildren"])}

Pensions:
{format_pension_data(raw_data["data"]["SSCalData"]["SSCalPensions"])}

Settings:
{format_settings(raw_data["data"]["Settings"])}
"""

    return preprocessed_data


def preprocess_data_primary_only(raw_data: dict, primary: dict):
    primary_earnings, _ = calculate_earnings_history(raw_data=raw_data)

    # Calculate total years worked and total earnings
    primary_years_worked = sum(
        1 for earning in primary_earnings.values() if earning > 0
    )
    primary_total_earnings = sum(primary_earnings.values())

    preprocessed_data = f"""
Primary Beneficiary:
{format_person_data(primary, primary_years_worked, primary_total_earnings)}

Marital Status: {"Married" if raw_data['data']['MaritalStatus'] == 2 else "Other"}

Primary Beneficiary Earnings History:
{format_earnings_history(primary_earnings)}

Children:
{format_children_data(raw_data["data"]["SSCalData"]["SSCalChildren"])}

Pensions:
{format_pension_data(raw_data["data"]["SSCalData"]["SSCalPensions"])}

Settings:
{format_settings(raw_data["data"]["Settings"])}
"""

    return preprocessed_data


def format_person_data(person: dict, years_worked: int, total_earnings: float) -> str:
    return f"""Name: {person['name']}
Date of Birth: {person['birth_date'].strftime('%Y-%m-%d')}
Current Age: {person['age']}
Gender: {person['gender']}
Email: {person['email']}
Phone: {person['phone']}
Blind: {person['blind']}
Total Years Worked: {years_worked}
Total Lifetime Earnings: ${total_earnings:,.2f}
Average Annual Earnings: ${total_earnings / years_worked:,.2f}
Primary Insurance Amount (PIA): ${person['pia']:,.2f}
Full Retirement Age (FRA): {person['fra'].strftime('%Y-%m-%d')} (Age {person['fra_age']})
Has Full Coverage: {person['has_full_coverage']}
Is Disabled: {person['is_disabled']}
Has Pension: {person['has_pension']}
Is Collecting Benefits: {person['is_collecting_benefits']}
Estimated Retirement Age: {person['est_retirement_age']}
Life Expectancy: {person['life_expectancy']}
"""


def format_earnings_history(earnings: dict) -> str:
    return "\n".join(
        f"{year}: ${earnings:,.2f}"
        for year, earnings in sorted(earnings.items(), reverse=True)
    )


def format_children_data(children: list) -> str:
    if not children:
        return "No children"

    children_data = []
    for child in children:
        child_info = f"""Name: {child['Name']}
Birth Date: {datetime.strptime(child['BirthDate'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')}
Age: {child['Age']}
High School Graduation Date: {datetime.strptime(child['HighSchoolGradDate'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')}
Is Collecting Benefits: {child['IsCollectingBenefits']}
Is Disabled: {child['IsDisabled']}
"""
        children_data.append(child_info)

    return "\n\n".join(children_data)


def format_pension_data(pensions: list) -> str:
    if not pensions:
        return "No pensions"

    pension_data = []
    for pension in pensions:
        pension_info = f"""Title: {pension['Title']}
Annual Amount: ${pension['AnnualAmount']:,.2f}
Lump Sum Amount: {"$" + f"{pension['LumpSumAmount']:,.2f}" if pension['LumpSumAmount'] else "N/A"}
Start Year: {pension['StartYear']}
Exempt from GPO: {pension['ExemptFromGPO']}
"""
        pension_data.append(pension_info)

    return "\n\n".join(pension_data)


def format_settings(settings: dict) -> str:
    return f"""COLA: {settings['COLA']}%
Inflation Rate: {settings['InflationRate']}%
Nominal Rate of Return: {settings['NominalRateOfReturn']}%
Real Rate of Return: {settings['RealRateOfReturn']}%"""


def preprocess_roadmap_output(raw_data) -> str | None:
    # Extract primary and spouse information
    family = {}
    primary = get_primary(raw_data=raw_data)
    family["primary"] = primary

    if raw_data["data"]["Spouse_FirstName"]:
        spouse = get_spouse(raw_data=raw_data)
        family["spouse"] = spouse

    if raw_data["data"]["SSCalData"]["SSCalChildren"]:
        children = get_children(raw_data=raw_data)
        family["children"] = children

    # Format the preprocessed data
    if "spouse" not in family.keys():
        result = preprocess_data_primary_only(
            raw_data=raw_data, primary=family["primary"]
        )
    else:
        result = preprocess_data_primary_and_spouse(
            raw_data=raw_data, primary=family["primary"], spouse=family["spouse"]
        )

    return result


# Example usage
if __name__ == "__main__":
    file_path = "client-exports/daniels_uphill.json"
    preprocessed_data = preprocess_roadmap_output(file_path)
    print(preprocessed_data)
