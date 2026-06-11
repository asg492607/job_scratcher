import React from 'react';
import { useOpportunityStore } from '../../app/store';
import { Category, RemoteStatus, Domain } from '../../types/opportunity';

export const OpportunityFilters: React.FC = () => {
  const { filters, setFilters, clearFilters } = useOpportunityStore();

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters({ search: e.target.value });
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value as Category | '';
    setFilters({ category: value ? [value] : [] });
  };

  const handleRemoteStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value as RemoteStatus | '';
    setFilters({ remote_status: value ? [value] : [] });
  };

  const handleDomainChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value as Domain | '';
    setFilters({ domain: value ? [value] : [] });
  };

  return (
    <div className="sidebar-glass p-6 space-y-6 sticky top-24">
      <div>
        <h3 className="text-xs font-bold uppercase tracking-wider mb-3" style={{ color: 'var(--text-secondary)' }}>Search</h3>
        <div className="relative">
          <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" style={{ color: 'var(--text-muted)' }} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Search keywords..."
            value={filters.search || ''}
            onChange={handleSearchChange}
            className="input-dark pl-9"
          />
        </div>
      </div>

      <div>
        <h3 className="text-xs font-bold uppercase tracking-wider mb-3" style={{ color: 'var(--text-secondary)' }}>Filters</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wider mb-1.5" style={{ color: 'var(--text-muted)' }}>Category</label>
            <select
              value={filters.category?.[0] || ''}
              onChange={handleCategoryChange}
              className="select-dark"
            >
              <option value="">All Categories</option>
              <option value="internship">Internships</option>
              <option value="job">Jobs</option>
              <option value="hackathon">Hackathons</option>
              <option value="fellowship">Fellowships</option>
              <option value="competition">Competitions</option>
              <option value="freelance">Freelance</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wider mb-1.5" style={{ color: 'var(--text-muted)' }}>Work Type</label>
            <select
              value={filters.remote_status?.[0] || ''}
              onChange={handleRemoteStatusChange}
              className="select-dark"
            >
              <option value="">All Types</option>
              <option value="remote">Remote</option>
              <option value="hybrid">Hybrid</option>
              <option value="onsite">On-site</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wider mb-1.5" style={{ color: 'var(--text-muted)' }}>Design Domain</label>
            <select
              value={filters.domain?.[0] || ''}
              onChange={handleDomainChange}
              className="select-dark"
            >
              <option value="">All Domains</option>
              <option value="ux_ui">UI/UX Design</option>
              <option value="product_design">Product Design</option>
              <option value="graphic_design">Graphic Design</option>
              <option value="motion_graphics">Motion Graphics</option>
              <option value="industrial_design">Industrial Design</option>
              <option value="architecture">Architecture</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>
      </div>

      <div className="pt-4 border-t" style={{ borderColor: 'var(--border)' }}>
        <button
          onClick={clearFilters}
          className="btn-outline w-full flex items-center justify-center gap-2"
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Clear Filters
        </button>
      </div>
    </div>
  );
};
