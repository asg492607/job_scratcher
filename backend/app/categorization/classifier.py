from typing import Dict, Any

class OpportunityClassifier:
    """
    Categorization Engine.
    Classifies an opportunity into categories (Internship, Job, Hackathon, etc.)
    and domains (UX/UI, Graphic Design, etc.).
    """
    
    def __init__(self):
        pass
        
    def classify(self, title: str, description: str) -> Dict[str, str]:
        """
        Classifies the opportunity based on title and description.
        Returns a dictionary with 'category' and 'domain'.
        """
        # Stub implementation
        title_lower = title.lower() if title else ""
        desc_lower = description.lower() if description else ""
        combined_text = title_lower + " " + desc_lower
        
        # Determine category
        category = "job"
        if "internship" in combined_text or "intern" in combined_text:
            category = "internship"
        elif "hackathon" in combined_text:
            category = "hackathon"
        elif "fellowship" in combined_text:
            category = "fellowship"
        elif "competition" in combined_text:
            category = "competition"
        elif "freelance" in combined_text or "contract" in combined_text:
            category = "freelance"
            
        # Determine domain
        domain = "other"
        if "ux" in combined_text or "ui" in combined_text or "product design" in combined_text:
            domain = "ux_ui" if "ux" in combined_text or "ui" in combined_text else "product_design"
        elif "graphic" in combined_text or "visual" in combined_text:
            domain = "graphic_design"
        elif "motion" in combined_text or "animation" in combined_text:
            domain = "motion_graphics"
        elif "industrial" in combined_text:
            domain = "industrial_design"
        elif "architecture" in combined_text:
            domain = "architecture"
            
        return {
            "category": category,
            "domain": domain
        }

    def classify_skills(self, description: str) -> set:
        """
        Extracts a set of skills from the description using a comprehensive design skills dictionary.
        """
        if not description:
            return set()
            
        desc_lower = description.lower()
        found_skills = set()
        
        from app.categorization.design_skills import DESIGN_SKILLS
        
        import re
        for skill in DESIGN_SKILLS:
            # Escape regex characters in the skill (e.g., c++, p5.js)
            # Add word boundary to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, desc_lower):
                # Standardize format: Title Case unless it's an acronym
                acronyms = {"ui", "ux", "ui/ux", "html", "css", "sql", "aws", "php", "ia", "ixd", "hci", "ucd", "cx", "vfx", "cmyk", "rgb", "cad", "leed", "dfm", "ar/vr", "xr", "vui", "pwa", "spa", "b2b", "b2c", "saas", "swot", "rfp", "sow", "nda", "sus", "csat", "ces", "cro"}
                if skill in acronyms:
                    found_skills.add(skill.upper())
                else:
                    found_skills.add(skill.title())
                
        return found_skills

