const API_BASE_URL = '/api/v1';

// DOM Elements
const elements = {
  searchInput: document.getElementById('search-input'),
  categorySelect: document.getElementById('category-select'),
  remoteSelect: document.getElementById('remote-select'),
  domainSelect: document.getElementById('domain-select'),
  clearFiltersBtn: document.getElementById('clear-filters-btn'),
  refreshBtn: document.getElementById('refresh-btn'),
  scrapeMessage: document.getElementById('scrape-message'),
  opportunitiesGrid: document.getElementById('opportunities-grid'),
  loadingSpinner: document.getElementById('loading-spinner'),
  errorMessage: document.getElementById('error-message'),
  errorText: document.getElementById('error-text'),
  emptyState: document.getElementById('empty-state'),
  
  // Modal Elements
  modal: document.getElementById('detail-modal'),
  modalCloseBtn: document.getElementById('close-modal-btn'),
  modalLoading: document.getElementById('modal-loading'),
  modalContent: document.getElementById('modal-content'),
};

// State
let opportunities = [];
let filters = {
  search: '',
  category: '',
  remote_status: '',
  domain: '',
  sort: ''
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  loadOpportunities();
});

function setupEventListeners() {
  // Filters
  elements.searchInput.addEventListener('input', debounce((e) => {
    filters.search = e.target.value;
    loadOpportunities();
  }, 500));

  elements.categorySelect.addEventListener('change', (e) => {
    filters.category = e.target.value;
    loadOpportunities();
  });

  elements.remoteSelect.addEventListener('change', (e) => {
    filters.remote_status = e.target.value;
    loadOpportunities();
  });

  elements.domainSelect.addEventListener('change', (e) => {
    filters.domain = e.target.value;
    loadOpportunities();
  });

  document.getElementById('sort-select').addEventListener('change', (e) => {
    filters.sort = e.target.value;
    loadOpportunities();
  });

  elements.clearFiltersBtn.addEventListener('click', () => {
    filters = { search: '', category: '', remote_status: '', domain: '', sort: '' };
    elements.searchInput.value = '';
    elements.categorySelect.value = '';
    elements.remoteSelect.value = '';
    elements.domainSelect.value = '';
    document.getElementById('sort-select').value = '';
    loadOpportunities();
  });

  // Refresh Jobs
  elements.refreshBtn.addEventListener('click', async () => {
    try {
      const btnIcon = elements.refreshBtn.querySelector('svg');
      btnIcon.classList.add('pulse-dot'); // Temporary loading effect
      elements.refreshBtn.disabled = true;
      elements.refreshBtn.querySelector('span').textContent = 'Scraping...';

      const res = await fetch(`${API_BASE_URL}/opportunities/scrape`, { 
        method: 'POST',
        headers: { 'X-API-Key': 'opportunity_intelligence_admin_key_2026' }
      });
      if (!res.ok) throw new Error('Scrape failed');
      
      elements.scrapeMessage.classList.remove('hidden');
      setTimeout(() => elements.scrapeMessage.classList.add('hidden'), 5000);
      
      await loadOpportunities();
    } catch (err) {
      console.error(err);
      alert('Failed to run scrape.');
    } finally {
      elements.refreshBtn.disabled = false;
      elements.refreshBtn.querySelector('svg').classList.remove('pulse-dot');
      elements.refreshBtn.querySelector('span').textContent = 'Refresh Latest Jobs';
    }
  });

  // Modal
  elements.modalCloseBtn.addEventListener('click', closeModal);
  elements.modal.addEventListener('click', (e) => {
    if (e.target === elements.modal) closeModal();
  });
}

async function loadOpportunities() {
  try {
    showState('loading');
    
    // Build query params
    const params = new URLSearchParams();
    if (filters.search) params.append('search', filters.search);
    if (filters.category) params.append('category', filters.category);
    if (filters.remote_status) params.append('remote_status', filters.remote_status);
    if (filters.domain) params.append('domain', filters.domain);

    const url = `${API_BASE_URL}/opportunities?${params.toString()}`;
    const res = await fetch(url);
    
    if (!res.ok) throw new Error('Failed to fetch data');
    let fetchedOps = await res.json();
    
    // Sort logic
    opportunities = fetchedOps.sort((a, b) => {
      if (filters.sort === 'quality') {
        return (b.quality_score || 0) - (a.quality_score || 0);
      } else if (filters.sort === 'freshness') {
        return (b.freshness_score || 0) - (a.freshness_score || 0);
      } else {
        // Default: LinkedIn first
        const isALinkedIn = a.source && a.source.toLowerCase().includes('linkedin');
        const isBLinkedIn = b.source && b.source.toLowerCase().includes('linkedin');
        if (isALinkedIn && !isBLinkedIn) return -1;
        if (!isALinkedIn && isBLinkedIn) return 1;
        return 0;
      }
    });
    
    if (opportunities.length === 0) {
      showState('empty');
    } else {
      renderOpportunities();
      showState('grid');
    }
  } catch (err) {
    elements.errorText.textContent = err.message;
    showState('error');
  }
}

function showState(state) {
  elements.loadingSpinner.classList.add('hidden');
  elements.errorMessage.classList.add('hidden');
  elements.emptyState.classList.add('hidden');
  elements.opportunitiesGrid.classList.add('hidden');

  if (state === 'loading') elements.loadingSpinner.classList.remove('hidden');
  if (state === 'error') elements.errorMessage.classList.remove('hidden');
  if (state === 'empty') elements.emptyState.classList.remove('hidden');
  if (state === 'grid') elements.opportunitiesGrid.classList.remove('hidden');
}

function renderOpportunities() {
  elements.opportunitiesGrid.innerHTML = '';
  
  opportunities.forEach(opp => {
    const isNew = new Date(opp.created_at).getTime() > Date.now() - 3 * 24 * 60 * 60 * 1000;
    
    // Build badges
    let badgesHTML = '';
    if (isNew) badgesHTML += `<span class="badge badge-new"><span class="pulse-dot"></span>New</span>`;
    
    // Quality Score Badge
    if (opp.quality_score) {
      let qClass = 'badge-quality-medium';
      if (opp.quality_score >= 80) qClass = 'badge-quality-high';
      else if (opp.quality_score < 50) qClass = 'badge-quality-low';
      badgesHTML += `<span class="badge ${qClass}">⚡ Q: ${opp.quality_score}</span>`;
    }

    if (opp.category) badgesHTML += `<span class="badge badge-${opp.category.replace(' ', '-')}">${opp.category}</span>`;
    if (opp.remote_status) badgesHTML += `<span class="badge badge-${opp.remote_status}">${opp.remote_status}</span>`;
    if (opp.experience_level && opp.experience_level !== "Not Specified") badgesHTML += `<span class="badge badge-experience">${opp.experience_level}</span>`;
    if (opp.source) badgesHTML += `<span class="badge badge-source">${opp.source}</span>`;
    
    // Formatting Salary
    let displaySalary = opp.salary || opp.stipend;
    if (!displaySalary && opp.min_salary) {
      const curr = opp.currency || '$';
      displaySalary = `${curr}${Math.round(opp.min_salary/1000)}k`;
      if (opp.max_salary && opp.max_salary !== opp.min_salary) {
        displaySalary += ` - ${Math.round(opp.max_salary/1000)}k`;
      }
    }
    if (displaySalary) badgesHTML += `<span class="badge badge-salary">${displaySalary}</span>`;

    // Build skills
    let skillsHTML = '';
    if (opp.skills && opp.skills.length > 0) {
      const displaySkills = opp.skills.slice(0, 3);
      skillsHTML = displaySkills.map(s => `<span class="skill-tag">${s.name}</span>`).join('');
      if (opp.skills.length > 3) {
        skillsHTML += `<span class="skill-tag" style="opacity:0.7">+${opp.skills.length - 3}</span>`;
      }
    }

    const card = document.createElement('a');
    card.href = '#';
    card.className = 'opp-card';
    card.onclick = (e) => {
      e.preventDefault();
      openModal(opp.id);
    };

    card.innerHTML = `
      <div class="card-header">
        <div>
          <h3 class="card-title">${opp.title}</h3>
          <div class="card-subtitle">
            ${opp.normalized_company || opp.company || 'Unknown Company'} 
            ${opp.location ? `<span class="dot">•</span> <span class="card-loc">${opp.location}</span>` : ''}
          </div>
        </div>
      </div>
      <div class="badges-container">${badgesHTML}</div>
      <div class="card-desc">${opp.description}</div>
      <div class="card-footer">
        <div class="skills-list">${skillsHTML}</div>
        <div class="view-btn">
          View
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </div>
      </div>
    `;
    
    elements.opportunitiesGrid.appendChild(card);
  });
}

// Modal Logic
async function openModal(id) {
  elements.modal.classList.remove('hidden');
  elements.modalLoading.classList.remove('hidden');
  elements.modalContent.classList.add('hidden');
  document.body.style.overflow = 'hidden';

  try {
    const res = await fetch(`${API_BASE_URL}/opportunities/${id}`);
    if (!res.ok) throw new Error('Not found');
    const opp = await res.json();
    renderModalContent(opp);
  } catch (err) {
    elements.modalContent.innerHTML = `<div style="padding: 40px; text-align: center;">Error loading opportunity details.</div>`;
    elements.modalContent.classList.remove('hidden');
    elements.modalLoading.classList.add('hidden');
  }
}

function closeModal() {
  elements.modal.classList.add('hidden');
  document.body.style.overflow = '';
}

function renderModalContent(opp) {
  let skillsHTML = '';
  if (opp.skills && opp.skills.length > 0) {
    skillsHTML = `
      <div class="detail-section">
        <h2 class="detail-section-title">Required Skills</h2>
        <div style="display:flex; flex-wrap:wrap; gap:8px;">
          ${opp.skills.map(s => `<span class="skill-tag" style="font-size:0.75rem; padding:6px 12px;">${s.name}</span>`).join('')}
        </div>
      </div>
    `;
  }

  let aiInsightHTML = '';
  if (opp.growth_potential) {
    aiInsightHTML = `
      <div class="ai-insight">
        <div class="ai-title">
          <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          Intelligence Insights
        </div>
        <div class="ai-text">${opp.growth_potential}</div>
      </div>
    `;
  }

  elements.modalContent.innerHTML = `
    <div class="detail-header">
      <div class="detail-header-bg"></div>
      <div class="detail-flex">
        <div>
          <div class="badges-container" style="margin-bottom: 12px;">
            ${opp.category ? `<span class="badge badge-${opp.category.replace(' ','-')}">${opp.category}</span>` : ''}
            ${opp.remote_status ? `<span class="badge badge-${opp.remote_status}">${opp.remote_status}</span>` : ''}
          </div>
          <h1 class="detail-title">${opp.title}</h1>
          <div class="detail-company">
            ${opp.normalized_company || opp.company || 'Unknown Company'}
            ${opp.location ? `<span>•</span> <span>${opp.location}</span>` : ''}
          </div>
        </div>
        <div>
          <a href="${opp.apply_url}" target="_blank" class="btn-primary" style="padding: 14px 24px; font-size: 1rem;">
            Apply for Role
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
          </a>
        </div>
      </div>
    </div>
    <div class="detail-body">
      <div>
        <div class="detail-section">
          <h2 class="detail-section-title">About the Role</h2>
          <div class="detail-text">${opp.description}</div>
        </div>
        ${skillsHTML}
      </div>
      <div>
        <div class="sidebar-panel">
          <h3 class="panel-title">Overview</h3>
          ${(opp.min_salary || opp.salary || opp.stipend) ? `
            <div class="dl-group"><div class="dl-dt">Compensation</div><div class="dl-dd highlight">${opp.min_salary ? (opp.currency || '$') + Math.round(opp.min_salary/1000) + 'k' + (opp.max_salary && opp.max_salary !== opp.min_salary ? ' - ' + Math.round(opp.max_salary/1000) + 'k' : '') : (opp.salary || opp.stipend)}</div></div>
          ` : ''}
          ${opp.experience_level && opp.experience_level !== "Not Specified" ? `
            <div class="dl-group"><div class="dl-dt">Experience</div><div class="dl-dd">${opp.experience_level}</div></div>
          ` : ''}
          ${opp.difficulty ? `
            <div class="dl-group"><div class="dl-dt">Difficulty</div><div class="dl-dd">${opp.difficulty}</div></div>
          ` : ''}
          ${opp.deadline ? `
            <div class="dl-group"><div class="dl-dt">Deadline</div><div class="dl-dd" style="color:#f87171">${new Date(opp.deadline).toLocaleDateString()}</div></div>
          ` : ''}
          <div class="dl-group"><div class="dl-dt">Source</div><div class="dl-dd">${opp.source}</div></div>
          <div class="dl-group"><div class="dl-dt">Portfolio Req.</div><div class="dl-dd">${opp.portfolio_required ? 'Yes' : 'Not stated'}</div></div>
        </div>
        
        <div class="sidebar-panel">
          <h3 class="panel-title">Intelligence Scores</h3>
          <div class="dl-group">
            <div class="dl-dt">Quality Score</div>
            <div class="dl-dd" style="display:flex; align-items:center; gap:8px;">
              <div style="flex:1; background:rgba(255,255,255,0.1); height:6px; border-radius:3px; overflow:hidden;">
                <div style="width:${opp.quality_score || 0}%; height:100%; background:${(opp.quality_score || 0) >= 80 ? '#34d399' : '#fcd34d'};"></div>
              </div>
              <span>${opp.quality_score || 0}</span>
            </div>
          </div>
          <div class="dl-group">
            <div class="dl-dt">Freshness Score</div>
            <div class="dl-dd" style="display:flex; align-items:center; gap:8px;">
              <div style="flex:1; background:rgba(255,255,255,0.1); height:6px; border-radius:3px; overflow:hidden;">
                <div style="width:${opp.freshness_score || 0}%; height:100%; background:#60a5fa;"></div>
              </div>
              <span>${opp.freshness_score || 0}</span>
            </div>
          </div>
          <div class="dl-group">
            <div class="dl-dt">Source Reliability</div>
            <div class="dl-dd" style="display:flex; align-items:center; gap:8px;">
              <div style="flex:1; background:rgba(255,255,255,0.1); height:6px; border-radius:3px; overflow:hidden;">
                <div style="width:${opp.source_reliability_score || 0}%; height:100%; background:#c084fc;"></div>
              </div>
              <span>${opp.source_reliability_score || 0}</span>
            </div>
          </div>
        </div>

        ${aiInsightHTML}
      </div>
    </div>
  `;

  elements.modalLoading.classList.add('hidden');
  elements.modalContent.classList.remove('hidden');
}

// Utils
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}
