import React, { useEffect } from 'react';
import { useOpportunityStore } from '../../app/store';
import { OpportunityCard } from '../../components/cards/OpportunityCard';
import { OpportunityFilters } from '../../components/filters/OpportunityFilters';
import { motion } from 'framer-motion';

export const DiscoveryPage: React.FC = () => {
  const { opportunities, isLoading, error, loadOpportunities } = useOpportunityStore();

  useEffect(() => {
    loadOpportunities();
  }, [loadOpportunities]);

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Design Opportunities</h1>
          <p className="mt-2 text-sm text-slate-600">Discover internships, jobs, and hackathons tailored for designers.</p>
        </div>

        <div className="flex flex-col md:flex-row gap-8">
          <aside className="w-full md:w-64 flex-shrink-0">
            <OpportunityFilters />
          </aside>

          <main className="flex-1">
            {isLoading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
              </div>
            ) : error ? (
              <div className="bg-red-50 p-4 rounded-md">
                <h3 className="text-sm font-medium text-red-800">Error loading opportunities</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            ) : opportunities.length === 0 ? (
              <div className="bg-white rounded-xl border border-slate-200 p-12 text-center shadow-sm">
                <svg className="mx-auto h-12 w-12 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path vectorEffect="non-scaling-stroke" strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-slate-900">No opportunities found</h3>
                <p className="mt-1 text-sm text-slate-500">Try adjusting your filters to see more results.</p>
              </div>
            ) : (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="grid grid-cols-1 gap-6"
              >
                {opportunities.map((opportunity) => (
                  <OpportunityCard key={opportunity.id} opportunity={opportunity} />
                ))}
              </motion.div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};
