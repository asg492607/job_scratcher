import React, { useEffect } from 'react';
import { useOpportunityStore } from '../../app/store';
import { OpportunityCard } from '../../components/cards/OpportunityCard';
import { OpportunityFilters } from '../../components/filters/OpportunityFilters';

export const DiscoveryPage: React.FC = () => {
  const {
    opportunities,
    isLoading,
    isScraping,
    error,
    scrapeMessage,
    loadOpportunities,
    scrapeAndReload,
  } = useOpportunityStore();

  useEffect(() => {
    loadOpportunities();
  }, [loadOpportunities]);

  return (
    <div className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="mb-10 flex flex-col gap-6 md:flex-row md:items-end md:justify-between relative z-10">
        <div>
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-2" style={{ fontFamily: 'Syne, sans-serif' }}>
            Discover <span className="gradient-text">Opportunities</span>
          </h1>
          <p className="text-base" style={{ color: 'var(--text-secondary)' }}>
            Curated internships, jobs, and hackathons tailored for designers.
          </p>
          {scrapeMessage && (
            <p className="mt-2 text-sm font-medium text-emerald-400 bg-emerald-400/10 inline-block px-3 py-1 rounded-md border border-emerald-400/20">{scrapeMessage}</p>
          )}
        </div>
        <button
          type="button"
          onClick={scrapeAndReload}
          disabled={isScraping}
          className="btn-primary flex items-center justify-center gap-2"
        >
          {isScraping ? (
            <>
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Scraping jobs...
            </>
          ) : (
            <>
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Refresh Latest Jobs
            </>
          )}
        </button>
      </div>

      <div className="flex flex-col lg:flex-row gap-8 relative z-10">
        <aside className="w-full lg:w-72 flex-shrink-0">
          <OpportunityFilters />
        </aside>

        <main className="flex-1">
          {isLoading ? (
            <div className="flex flex-col justify-center items-center h-64 gap-4">
              <div className="animate-spin rounded-full h-10 w-10 border-b-2" style={{ borderColor: 'var(--accent-purple)' }}></div>
              <p style={{ color: 'var(--text-muted)' }}>Loading opportunities...</p>
            </div>
          ) : error ? (
            <div className="glass-card p-6 border-red-500/20 bg-red-500/5">
              <h3 className="text-sm font-medium text-red-400">Error loading opportunities</h3>
              <p className="text-sm text-red-300/70 mt-1">{error}</p>
            </div>
          ) : opportunities.length === 0 ? (
            <div className="glass-card p-12 text-center flex flex-col items-center justify-center">
              <div className="w-16 h-16 rounded-full flex items-center justify-center mb-4" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border)' }}>
                <svg className="h-8 w-8 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-bold" style={{ color: 'var(--text-primary)' }}>No opportunities found</h3>
              <p className="mt-2 text-sm" style={{ color: 'var(--text-muted)' }}>Try adjusting your filters or clear them to see more results.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {opportunities.map((opportunity) => (
                <OpportunityCard key={opportunity.id} opportunity={opportunity} />
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};
