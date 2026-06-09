import { create } from 'zustand';
import { Opportunity, OpportunityFilters } from '../types/opportunity';
import { fetchOpportunities, scrapeOpportunities } from '../services/api/opportunities';

interface OpportunityState {
  opportunities: Opportunity[];
  isLoading: boolean;
  isScraping: boolean;
  error: string | null;
  scrapeMessage: string | null;
  filters: OpportunityFilters;
  
  setFilters: (filters: Partial<OpportunityFilters>) => void;
  loadOpportunities: () => Promise<void>;
  scrapeAndReload: () => Promise<void>;
  clearFilters: () => void;
}

const defaultFilters: OpportunityFilters = {
  search: '',
  category: [],
  remote_status: [],
  domain: [],
  difficulty: [],
};

export const useOpportunityStore = create<OpportunityState>((set, get) => ({
  opportunities: [],
  isLoading: false,
  isScraping: false,
  error: null,
  scrapeMessage: null,
  filters: defaultFilters,

  setFilters: (newFilters) => {
    set((state) => ({
      filters: { ...state.filters, ...newFilters },
    }));
    get().loadOpportunities();
  },

  clearFilters: () => {
    set({ filters: defaultFilters });
    get().loadOpportunities();
  },

  loadOpportunities: async () => {
    set({ isLoading: true, error: null });
    try {
      const { filters } = get();
      const data = await fetchOpportunities(filters);
      set({ opportunities: data, isLoading: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to fetch opportunities';
      set({ error: errorMessage, isLoading: false });
    }
  },

  scrapeAndReload: async () => {
    set({ isScraping: true, error: null, scrapeMessage: null });
    try {
      const result = await scrapeOpportunities();
      await get().loadOpportunities();
      set({
        isScraping: false,
        scrapeMessage: `Scrape complete: ${result.created} new, ${result.updated} updated.`,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to scrape opportunities';
      set({ error: errorMessage, isScraping: false });
    }
  },
}));
