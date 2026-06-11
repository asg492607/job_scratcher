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
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-6">
      <div>
        <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-3">Search</h3>
        <input
          type="text"
          placeholder="Search opportunities..."
          value={filters.search || ''}
          onChange={handleSearchChange}
          className="w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
        />
      </div>

      <div>
        <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-3">Filters</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Category</label>
            <select
              value={filters.category?.[0] || ''}
              onChange={handleCategoryChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm bg-white"
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
            <label className="block text-sm font-medium text-slate-700 mb-1">Work Type</label>
            <select
              value={filters.remote_status?.[0] || ''}
              onChange={handleRemoteStatusChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm bg-white"
            >
              <option value="">All Types</option>
              <option value="remote">Remote</option>
              <option value="hybrid">Hybrid</option>
              <option value="onsite">On-site</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Design Domain</label>
            <select
              value={filters.domain?.[0] || ''}
              onChange={handleDomainChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm bg-white"
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

      <div className="pt-4 border-t border-slate-100">
        <button
          onClick={clearFilters}
          className="w-full px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
        >
          Clear All Filters
        </button>
      </div>
    </div>
  );
};
