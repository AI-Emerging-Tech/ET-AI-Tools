from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


class CyberInsuranceApplication(BaseModel):
    """Information specific to Cyber Insurance applications."""
    applicant_details: Optional[Dict[str, Any]] = Field(description="Details about the applicant's company name, location and any basic information.")
    cybersecurity_practices: Optional[Dict[str, Any]] = Field(description="Summary of cybersecurity controls and practices in place")
    claims_history: Optional[List[Dict[str, str]]] = Field(description="List of previous cyber claims including type, date, loss amount, and resolution")
    regulatory_compliance: Optional[Dict[str, bool]] = Field(description="Compliance status with regulations such as GDPR, HIPAA, and CCPA")
    requested_coverage: Optional[Dict[str, Any]] = Field(description="Requested coverage details including limits, retentions, and optional endorsements")

class AutoInsuranceApplication(BaseModel):
    """Information specific to Auto Insurance applications."""
    applicant_details: Optional[Dict[str, Any]] = Field(description="Applicant’s personal or business details.")
    vehicle_details: Optional[Dict[str, Any]] = Field(description="Details about the insured vehicles: make, model, year, VIN, usage.")
    driver_history: Optional[List[Dict[str, str]]] = Field(description="Driving history, violations, accidents for listed drivers.")
    coverage_needs: Optional[Dict[str, Any]] = Field(description="Coverage types requested: liability, collision, comprehensive, etc.")
    prior_insurance: Optional[Dict[str, Any]] = Field(description="Previous insurer, policy duration, claims made.")