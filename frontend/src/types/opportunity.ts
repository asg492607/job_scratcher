export type RemoteStatus = 'remote' | 'hybrid' | 'onsite';

export type Category = 'internship' | 'job' | 'hackathon' | 'fellowship' | 'competition' | 'freelance';

export type Domain = 'ux_ui' | 'graphic_design' | 'product_design' | 'motion_graphics' | 'industrial_design' | 'architecture' | 'other';

export type Difficulty = 'beginner' | 'intermediate' | 'advanced';

export interface Skill {
  id: string;
  name: string;
}

export interface Opportunity {
  id: string;
  title: string;
  company: string;
  description: string;
  location: string;
  remote_status?: RemoteStatus;
  salary?: string;
  stipend?: string;
  experience_level?: string;
  deadline?: string;
  source: string;
  apply_url: string;
  category?: Category;
  domain?: Domain;
  difficulty?: Difficulty;
  industry?: string;
  quality_score?: number;
  growth_potential?: string;
  portfolio_required: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  skills?: Skill[];
}

export interface OpportunityFilters {
  search?: string;
  category?: Category[];
  remote_status?: RemoteStatus[];
  domain?: Domain[];
  difficulty?: Difficulty[];
  portfolio_required?: boolean;
}
