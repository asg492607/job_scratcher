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
      <div className="min-h-screen flex justify-center items-center">
        <div className="flex flex-col items-center gap-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2" style={{ borderColor: 'var(--accent-purple)' }}></div>
          <p style={{ color: 'var(--text-muted)' }}>Loading opportunity details...</p>
        </div>
      </div>
    );
  }

  if (error || !opportunity) {
    return (
      <div className="py-12 px-4 sm:px-6 lg:px-8 max-w-3xl mx-auto">
        <div className="glass-card p-12 text-center flex flex-col items-center">
          <div className="w-16 h-16 rounded-full flex items-center justify-center mb-4 bg-red-500/10 border border-red-500/20">
            <svg className="h-8 w-8 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold mb-2" style={{ color: 'var(--text-primary)' }}>Opportunity Not Found</h2>
          <p className="mb-8" style={{ color: 'var(--text-secondary)' }}>{error || "The opportunity you're looking for doesn't exist or has been removed."}</p>
          <Link to="/opportunities" className="btn-primary">
            &larr; Back to Discovery
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <div className="mb-6">
          <Link to="/opportunities" className="inline-flex items-center gap-2 text-sm font-medium transition-colors" style={{ color: 'var(--text-secondary)' }}>
            <span className="p-1.5 rounded-md" style={{ background: 'rgba(255,255,255,0.05)' }}>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            </span>
            Back to Discovery
          </Link>
        </div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card overflow-hidden"
        >
          {/* Header */}
          <div className="p-8 sm:p-12 relative overflow-hidden" style={{ borderBottom: '1px solid var(--border)' }}>
            {/* Background gradient for header */}
            <div className="absolute top-0 right-0 w-full h-full opacity-10 pointer-events-none" style={{ background: 'linear-gradient(135deg, transparent 50%, var(--accent-purple) 100%)' }}></div>
            
            <div className="relative z-10 flex flex-col md:flex-row md:justify-between md:items-start gap-8">
              <div className="flex-1 min-w-0">
                <div className="flex flex-wrap gap-2 mb-6">
                  {opportunity.category && (
                    <span className={`badge badge-${opportunity.category.replace(' ', '-')}`}>
                      {opportunity.category}
                    </span>
                  )}
                  {opportunity.domain && (
                    <span className="badge badge-source">
                      {opportunity.domain.replace('_', ' ')}
                    </span>
                  )}
                  {opportunity.remote_status && (
                    <span className={`badge badge-${opportunity.remote_status}`}>
                      {opportunity.remote_status}
                    </span>
                  )}
                </div>
                
                <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight mb-4 leading-tight" style={{ color: 'var(--text-primary)', fontFamily: 'Syne, sans-serif' }}>
                  {opportunity.title}
                </h1>
                
                <div className="flex items-center flex-wrap gap-y-2 gap-x-4 text-lg font-medium" style={{ color: 'var(--text-secondary)' }}>
                  <span className="flex items-center gap-1.5 text-white">
                    <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                    {opportunity.company || 'Unknown Company'}
                  </span>
                  {opportunity.location && (
                    <>
                      <span className="opacity-30">•</span>
                      <span className="flex items-center gap-1.5">
                        <svg className="w-5 h-5 text-pink-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                        {opportunity.location}
                      </span>
                    </>
                  )}
                </div>
              </div>
              
              <div className="flex-shrink-0">
                <a
                  href={opportunity.apply_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary w-full md:w-auto flex items-center justify-center gap-2 px-8 py-4 text-base"
                >
                  Apply for Role
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                </a>
                <p className="text-center text-xs mt-3 opacity-60">Redirects to {opportunity.source}</p>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="p-8 sm:p-12 grid grid-cols-1 lg:grid-cols-3 gap-12">
            <div className="lg:col-span-2 space-y-10">
              <section>
                <h2 className="text-xl font-bold mb-5 flex items-center gap-2" style={{ color: 'var(--text-primary)', fontFamily: 'Syne, sans-serif' }}>
                  <div className="w-2 h-6 rounded-full bg-gradient-to-b from-purple-400 to-pink-500"></div>
                  About the Role
                </h2>
                <div className="text-base leading-relaxed whitespace-pre-wrap" style={{ color: 'var(--text-secondary)' }}>
                  {opportunity.description}
                </div>
              </section>

              {opportunity.skills && opportunity.skills.length > 0 && (
                <section>
                  <h2 className="text-xl font-bold mb-5 flex items-center gap-2" style={{ color: 'var(--text-primary)', fontFamily: 'Syne, sans-serif' }}>
                    <div className="w-2 h-6 rounded-full bg-gradient-to-b from-cyan-400 to-blue-500"></div>
                    Required Skills
                  </h2>
                  <div className="flex flex-wrap gap-2.5">
                    {opportunity.skills.map((skill) => (
                      <span key={skill.id} className="px-3.5 py-1.5 rounded-lg text-sm font-medium border" style={{ background: 'rgba(255,255,255,0.03)', borderColor: 'var(--border)', color: 'var(--text-primary)' }}>
                        {skill.name}
                      </span>
                    ))}
                  </div>
                </section>
              )}
            </div>

            {/* Sidebar / Intelligence */}
            <div className="space-y-6">
              <div className="sidebar-glass p-6">
                <h3 className="text-xs font-bold uppercase tracking-wider mb-5" style={{ color: 'var(--text-muted)' }}>Overview</h3>
                <dl className="space-y-4">
                  {(opportunity.salary || opportunity.stipend) && (
                    <div className="flex flex-col gap-1">
                      <dt className="text-[11px] uppercase tracking-wider font-semibold" style={{ color: 'var(--text-muted)' }}>Compensation</dt>
                      <dd className="text-sm font-medium text-emerald-400">{opportunity.salary || opportunity.stipend}</dd>
                    </div>
                  )}
                  {opportunity.experience_level && (
                    <div className="flex flex-col gap-1">
                      <dt className="text-[11px] uppercase tracking-wider font-semibold" style={{ color: 'var(--text-muted)' }}>Experience Level</dt>
                      <dd className="text-sm font-medium capitalize" style={{ color: 'var(--text-primary)' }}>{opportunity.experience_level}</dd>
                    </div>
                  )}
                  {opportunity.difficulty && (
                    <div className="flex flex-col gap-1">
                      <dt className="text-[11px] uppercase tracking-wider font-semibold" style={{ color: 'var(--text-muted)' }}>Difficulty</dt>
                      <dd className="text-sm font-medium capitalize" style={{ color: 'var(--text-primary)' }}>{opportunity.difficulty}</dd>
                    </div>
                  )}
                  {opportunity.deadline && (
                    <div className="flex flex-col gap-1">
                      <dt className="text-[11px] uppercase tracking-wider font-semibold" style={{ color: 'var(--text-muted)' }}>Deadline</dt>
                      <dd className="text-sm font-medium text-red-400">
                        {new Date(opportunity.deadline).toLocaleDateString(undefined, { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' })}
                      </dd>
                    </div>
                  )}
                  <div className="flex flex-col gap-1">
                    <dt className="text-[11px] uppercase tracking-wider font-semibold" style={{ color: 'var(--text-muted)' }}>Source</dt>
                    <dd className="text-sm font-medium capitalize" style={{ color: 'var(--text-primary)' }}>{opportunity.source}</dd>
                  </div>
                  <div className="flex flex-col gap-1">
                    <dt className="text-[11px] uppercase tracking-wider font-semibold" style={{ color: 'var(--text-muted)' }}>Portfolio Required</dt>
                    <dd className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>{opportunity.portfolio_required ? 'Yes' : 'Not explicitly stated'}</dd>
                  </div>
                </dl>
              </div>

              {opportunity.growth_potential && (
                <div className="rounded-xl p-6 relative overflow-hidden" style={{ background: 'rgba(124,58,237,0.1)', border: '1px solid rgba(124,58,237,0.2)' }}>
                  <div className="absolute -right-4 -top-4 w-24 h-24 bg-purple-500 rounded-full mix-blend-screen filter blur-3xl opacity-20"></div>
                  <h3 className="text-xs font-bold uppercase tracking-wider mb-3 flex items-center text-purple-400">
                    <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    Intelligence Insights
                  </h3>
                  <p className="text-sm leading-relaxed" style={{ color: 'var(--text-primary)' }}>{opportunity.growth_potential}</p>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};
