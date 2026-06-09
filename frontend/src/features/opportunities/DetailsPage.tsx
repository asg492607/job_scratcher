import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Opportunity } from '../../types/opportunity';
import { fetchOpportunityById } from '../../services/api/opportunities';
import { motion } from 'framer-motion';

export const DetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [opportunity, setOpportunity] = useState<Opportunity | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadOpportunity = async () => {
      if (!id) return;
      try {
        setIsLoading(true);
        const data = await fetchOpportunityById(id);
        setOpportunity(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch details');
      } finally {
        setIsLoading(false);
      }
    };
    
    loadOpportunity();
  }, [id]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 flex justify-center items-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error || !opportunity) {
    return (
      <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-sm p-8 text-center border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-900 mb-2">Opportunity Not Found</h2>
          <p className="text-slate-600 mb-6">{error || "The opportunity you're looking for doesn't exist or has been removed."}</p>
          <Link to="/opportunities" className="text-indigo-600 hover:text-indigo-500 font-medium">
            &larr; Back to Discovery
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <Link to="/opportunities" className="text-sm font-medium text-slate-500 hover:text-slate-700 transition-colors">
            &larr; Back to all opportunities
          </Link>
        </div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm"
        >
          {/* Header */}
          <div className="border-b border-slate-200 bg-white p-6 sm:p-10">
            <div className="flex flex-col md:flex-row md:justify-between md:items-start gap-6">
              <div>
                <div className="flex flex-wrap gap-2 mb-4">
                  {opportunity.category && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700 capitalize">
                      {opportunity.category}
                    </span>
                  )}
                  {opportunity.domain && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700 capitalize">
                      {opportunity.domain.replace('_', ' ')}
                    </span>
                  )}
                  {opportunity.remote_status && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700 capitalize">
                      {opportunity.remote_status}
                    </span>
                  )}
                </div>
                <h1 className="text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight mb-2">
                  {opportunity.title}
                </h1>
                <p className="text-lg text-slate-600 font-medium">
                  {opportunity.company} &bull; {opportunity.location}
                </p>
              </div>
              
              <div className="flex-shrink-0">
                <a
                  href={opportunity.apply_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full md:w-auto flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-sm transition-all"
                >
                  Apply Now
                </a>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="p-6 sm:p-10 grid grid-cols-1 md:grid-cols-3 gap-10">
            <div className="md:col-span-2 space-y-8">
              <section>
                <h2 className="text-xl font-bold text-slate-900 mb-4">About the Role</h2>
                <div className="prose prose-slate prose-indigo max-w-none text-slate-600 whitespace-pre-wrap">
                  {opportunity.description}
                </div>
              </section>

              {opportunity.skills && opportunity.skills.length > 0 && (
                <section>
                  <h2 className="text-xl font-bold text-slate-900 mb-4">Required Skills</h2>
                  <div className="flex flex-wrap gap-2">
                    {opportunity.skills.map((skill) => (
                      <span key={skill.id} className="inline-flex items-center px-3 py-1.5 rounded-md text-sm font-medium bg-slate-100 text-slate-800">
                        {skill.name}
                      </span>
                    ))}
                  </div>
                </section>
              )}
            </div>

            {/* Sidebar / Intelligence */}
            <div className="space-y-6">
              <div className="bg-slate-50 rounded-xl p-6 border border-slate-200">
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4">Key Details</h3>
                <dl className="space-y-4">
                  {(opportunity.salary || opportunity.stipend) && (
                    <div>
                      <dt className="text-xs text-slate-500 uppercase font-semibold">Compensation</dt>
                      <dd className="mt-1 text-sm text-slate-900 font-medium">{opportunity.salary || opportunity.stipend}</dd>
                    </div>
                  )}
                  {opportunity.experience_level && (
                    <div>
                      <dt className="text-xs text-slate-500 uppercase font-semibold">Experience Level</dt>
                      <dd className="mt-1 text-sm text-slate-900 font-medium capitalize">{opportunity.experience_level}</dd>
                    </div>
                  )}
                  {opportunity.difficulty && (
                    <div>
                      <dt className="text-xs text-slate-500 uppercase font-semibold">Difficulty</dt>
                      <dd className="mt-1 text-sm text-slate-900 font-medium capitalize">{opportunity.difficulty}</dd>
                    </div>
                  )}
                  {opportunity.deadline && (
                    <div>
                      <dt className="text-xs text-slate-500 uppercase font-semibold">Deadline</dt>
                      <dd className="mt-1 text-sm text-red-600 font-medium">
                        {new Date(opportunity.deadline).toLocaleDateString()}
                      </dd>
                    </div>
                  )}
                  <div>
                    <dt className="text-xs text-slate-500 uppercase font-semibold">Source</dt>
                    <dd className="mt-1 text-sm text-slate-900 font-medium capitalize">{opportunity.source}</dd>
                  </div>
                  <div>
                    <dt className="text-xs text-slate-500 uppercase font-semibold">Portfolio Required</dt>
                    <dd className="mt-1 text-sm text-slate-900 font-medium">{opportunity.portfolio_required ? 'Yes' : 'No'}</dd>
                  </div>
                </dl>
              </div>

              {opportunity.growth_potential && (
                <div className="bg-indigo-50 rounded-xl p-6 border border-indigo-100">
                  <h3 className="text-sm font-bold text-indigo-900 uppercase tracking-wider mb-2 flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    Intelligence Insights
                  </h3>
                  <p className="text-sm text-indigo-800">{opportunity.growth_potential}</p>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};
