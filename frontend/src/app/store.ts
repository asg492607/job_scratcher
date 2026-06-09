import { create } from 'zustand';
import { Opportunity, OpportunityFilters } from '../types/opportunity';
import { fetchOpportunities } from '../services/api/opportunities';

interface OpportunityState {
  opportunities: Opportunity[];
  isLoading: boolean;
  error: string | null;
  filters: OpportunityFilters;
  
  setFilters: (filters: Partial<OpportunityFilters>) => void;
  loadOpportunities: () => Promise<void>;
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
  error: null,
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
}));
