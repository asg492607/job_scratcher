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
        Extracts a set of skills from the description.
        """
        if not description:
            return set()
            
        desc_lower = description.lower()
        found_skills = set()
        
        # Comprehensive list of common tech/design skills
        common_skills = [
            "python", "javascript", "react", "node", "typescript", "java", "c++", "ruby", "php",
            "aws", "docker", "kubernetes", "sql", "nosql", "postgres", "mongodb",
            "figma", "sketch", "adobe xd", "photoshop", "illustrator", "invision",
            "ui", "ux", "wireframing", "prototyping", "user research", "usability testing",
            "html", "css", "tailwind", "sass",
            "agile", "scrum", "jira", "git", "github", "gitlab"
        ]
        
        for skill in common_skills:
            # Add word boundary to avoid partial matches
            import re
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, desc_lower):
                # Standardize format (e.g. capitalize first letter or keep standard casing)
                found_skills.add(skill.title() if skill not in ["ui", "ux", "aws", "sql", "html", "css", "php"] else skill.upper())
                
        return found_skills
