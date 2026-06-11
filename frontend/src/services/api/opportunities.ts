import { Opportunity, OpportunityFilters } from '../../types/opportunity';

const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || '/api/v1';

export const fetchOpportunities = async (filters?: OpportunityFilters): Promise<Opportunity[]> => {
  try {
    const params = new URLSearchParams();
    if (filters?.search) params.append('search', filters.search);
    if (filters?.category) filters.category.forEach(c => params.append('category', c));
    if (filters?.remote_status) filters.remote_status.forEach(r => params.append('remote_status', r));
    if (filters?.domain) filters.domain.forEach(d => params.append('domain', d));
    if (filters?.difficulty) filters.difficulty.forEach(d => params.append('difficulty', d));
    if (filters?.portfolio_required !== undefined) params.append('portfolio_required', String(filters.portfolio_required));

    const url = `${API_BASE_URL}/opportunities?${params.toString()}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching opportunities:', error);
    throw error;
  }
};

export const fetchOpportunityById = async (id: string): Promise<Opportunity> => {
  try {
    const response = await fetch(`${API_BASE_URL}/opportunities/${id}`);
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Error fetching opportunity with id ${id}:`, error);
    throw error;
  }
};

export interface ScrapeResult {
  created: number;
  updated: number;
  results?: Array<{
    source: string;
    fetched: number;
    created: number;
    updated: number;
    error?: string;
  }>;
}

export const scrapeOpportunities = async (): Promise<ScrapeResult> => {
  const response = await fetch(`${API_BASE_URL}/opportunities/scrape`, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error('Failed to scrape opportunities');
  }

  return response.json();
};
