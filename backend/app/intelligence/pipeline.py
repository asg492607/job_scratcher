import re
from datetime import datetime, timezone
from typing import Dict, Any, List

class IntelligencePipeline:
    """
    Core pipeline to process and augment raw job data with the 10 intelligence algorithms.
    """
    
    # Algorithm 8: Source Reliability Score Configuration
    RELIABILITY_SCORES = {
        "LinkedIn": 95,
        "Greenhouse": 95,
        "Lever": 95,
        "Wellfound": 90,
        "Himalayas": 90,
        "RemoteOK": 90,
        "The Muse": 85,
        "WeWorkRemotely": 85,
        "Indeed": 75,
        "Internshala": 70,
    }

    def process_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the raw job through all intelligence algorithms."""
        job = raw_job.copy()

        job["normalized_company"] = self.normalize_company(job.get("company_name", ""))
        job["category"] = self.classify_opportunity_type(job.get("raw_title", ""), job.get("job_description", ""))
        job["domain"] = self.classify_design_domain(job.get("raw_title", ""), job.get("job_description", ""))
        job["remote_status"] = self.classify_remote_status(job.get("job_location", ""), job.get("job_description", ""))
        job["experience_level"] = self.extract_experience(job.get("job_description", ""), job.get("raw_title", ""))
        
        salary_info = self.extract_salary(job.get("salary", "") or job.get("job_description", ""))
        job["min_salary"] = salary_info["min"]
        job["max_salary"] = salary_info["max"]
        job["currency"] = salary_info["currency"]
        
        job["source_reliability_score"] = self.calculate_reliability_score(job.get("site", ""))
        job["freshness_score"] = self.calculate_freshness_score(job.get("date_posted", ""))
        job["quality_score"] = self.calculate_quality_score(job)

        return job

    # ---------------------------------------------------------
    # Algorithm 1: Company Normalization
    # ---------------------------------------------------------
    def normalize_company(self, company: str) -> str:
        if not company:
            return ""
        # Remove common corporate suffixes
        normalized = re.sub(r'\b(LLC|Inc\.|Inc|Corp\.|Corp|Ltd\.|Ltd|GmbH)\b', '', company, flags=re.IGNORECASE)
        # Strip extra whitespace and commas at the end
        return normalized.strip(' ,.-')

    # ---------------------------------------------------------
    # Algorithm 3: Opportunity Type Classification
    # ---------------------------------------------------------
    def classify_opportunity_type(self, title: str, description: str) -> str:
        text = f"{title} {description}".lower()
        if "intern" in text or "internship" in text:
            return "internship"
        if "freelance" in text:
            return "freelance"
        if "contract" in text:
            return "contract"
        if "hackathon" in text:
            return "hackathon"
        if "competition" in text:
            return "competition"
        if "fellowship" in text:
            return "fellowship"
        return "job"

    # ---------------------------------------------------------
    # Algorithm 4: Design Domain Classification
    # ---------------------------------------------------------
    def classify_design_domain(self, title: str, description: str) -> str:
        text = f"{title} {description}".lower()
        if any(w in text for w in ["ui/ux", "ui ux", "ux/ui", "ux design", "ui design", "user experience"]):
            return "ux_ui"
        if "product design" in text:
            return "product_design"
        if "graphic design" in text or "visual design" in text or "illustrat" in text:
            return "graphic_design"
        if "motion" in text or "animation" in text or "video" in text:
            return "motion_graphics"
        if "3d" in text or "game design" in text:
            return "3d_game_design"
        if "brand" in text:
            return "brand_design"
        return "other"

    # ---------------------------------------------------------
    # Algorithm 5: Remote Classification
    # ---------------------------------------------------------
    def classify_remote_status(self, location: str, description: str) -> str:
        text = f"{location} {description}".lower()
        if "hybrid" in text:
            return "hybrid"
        if "remote" in text or "worldwide" in text or "anywhere" in text:
            return "remote"
        if location and "remote" not in location.lower():
            return "onsite"
        return "remote" # Default to remote if not specified

    # ---------------------------------------------------------
    # Algorithm 6: Experience Extraction
    # ---------------------------------------------------------
    def extract_experience(self, description: str, title: str) -> str:
        text = f"{title} {description}".lower()
        
        if "intern" in text:
            return "Intern"
        
        # Match patterns like "3-5 years", "3+ years", "1 to 3 years"
        match = re.search(r'(\d+)\s*[-to+]*\s*(\d+)?\s*years?', text)
        if match:
            min_yrs = int(match.group(1))
            if min_yrs == 0 or min_yrs == 1:
                return "0-1 Years"
            elif min_yrs <= 3:
                return "1-3 Years"
            elif min_yrs <= 5:
                return "3-5 Years"
            else:
                return "5+ Years"
                
        if "senior" in text or "lead" in text or "principal" in text:
            return "5+ Years"
        if "junior" in text or "entry level" in text:
            return "0-1 Years"
            
        return "Not Specified"

    # ---------------------------------------------------------
    # Algorithm 7: Salary Extraction
    # ---------------------------------------------------------
    def extract_salary(self, text: str) -> Dict[str, Any]:
        result = {"min": None, "max": None, "currency": None}
        if not text:
            return result
            
        # Very basic regex to catch e.g., "$80k - $100k" or "₹10,00,000 - ₹15,00,000"
        # Extract currency symbol
        curr_match = re.search(r'([$€£₹])', text)
        if curr_match:
            result["currency"] = curr_match.group(1)
            
        # Extract k amounts like 80k
        k_match = re.findall(r'(\d{2,3})[kK]', text)
        if len(k_match) == 2:
            result["min"] = float(k_match[0]) * 1000
            result["max"] = float(k_match[1]) * 1000
            return result
        elif len(k_match) == 1:
            result["min"] = float(k_match[0]) * 1000
            result["max"] = float(k_match[0]) * 1000
            return result
            
        return result

    # ---------------------------------------------------------
    # Algorithm 8: Source Reliability Score
    # ---------------------------------------------------------
    def calculate_reliability_score(self, source: str) -> int:
        return self.RELIABILITY_SCORES.get(source, 80) # default to 80

    # ---------------------------------------------------------
    # Algorithm 9: Freshness Scoring
    # ---------------------------------------------------------
    def calculate_freshness_score(self, posted_date_str: str) -> int:
        if not posted_date_str:
            return 50 # Default middle score if date unknown
            
        try:
            # Simplistic parsing, usually we use dateutil or expect ISO formats
            # For this MVP, if it contains 'hours' or 'days' ago in raw string:
            date_str = str(posted_date_str).lower()
            if "hour" in date_str or "today" in date_str:
                return 100
            if "day" in date_str:
                days = int(re.search(r'\d+', date_str).group()) if re.search(r'\d+', date_str) else 1
                if days <= 3: return 80
                if days <= 7: return 60
                if days <= 14: return 40
                return 20
        except Exception:
            pass
        return 60

    # ---------------------------------------------------------
    # Algorithm 10: Job Quality Score
    # ---------------------------------------------------------
    def calculate_quality_score(self, job: Dict[str, Any]) -> int:
        score = 50 # Base score
        
        # Detailed description
        desc_len = len(job.get("job_description", ""))
        if desc_len > 1000: score += 15
        elif desc_len > 500: score += 10
            
        # Salary Mentioned
        if job.get("min_salary") is not None or job.get("salary"):
            score += 15
            
        # Verified Company
        if job.get("company_name"):
            score += 10
            
        # Remote Option
        if job.get("remote_status") == "remote":
            score += 10
            
        return min(100, score)

