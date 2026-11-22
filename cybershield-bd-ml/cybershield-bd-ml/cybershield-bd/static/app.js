const translations = {
  en: {
    tagline: 'AI-Powered Protection Against Phishing & Scam Messages',
    dashboard: 'Dashboard',
    checkUrl: 'Check a Link',
    checkMessage: 'Check a Message',
    performance: 'Model Performance',
    about: 'How It Works',
    lightMode: 'Light mode',
    darkMode: 'Dark mode',
    heroKicker: 'PRE-CLICK SECURITY CHECK',
    heroTitle: 'Check Before You Trust',
    heroText: 'Analyze a suspicious link or message before entering passwords, OTPs, or financial information.',
    linkType: 'LINK CHECK',
    messageType: 'MESSAGE CHECK',
    urlTitle: 'Check a Link',
    urlIntro: 'Paste a link to check for phishing-related URL patterns. CyberShield does not visit it.',
    urlLabel: 'Link to check',
    urlHint: 'The link is analyzed as text; it is not opened.',
    urlPlaceholder: 'https://example.com/login',
    analyzeUrl: 'Analyze Link',
    messageTitle: 'Check a Message',
    messageIntro: 'Review wording patterns that may be associated with spam or scam messages.',
    messageLabel: 'Message to check',
    messageHint: 'The message model uses generic English SMS spam data.',
    messagePlaceholder: 'Paste a suspicious SMS or message here...',
    analyzeMessage: 'Analyze Message',
    performanceIntro: 'Evaluation results from the existing training pipeline.',
    loadingMetrics: 'Loading model performance…',
    researchResults: 'RESEARCH RESULTS',
    process: 'THE PROCESS',
    aboutTitle: 'How CyberShield BD Works',
    aboutIntro: 'A clear check before you interact with a link or message.',
    stepInputTitle: 'Input',
    stepDetectionTitle: 'AI Detection',
    stepXaiTitle: 'Explainable AI',
    stepWarningTitle: 'Security Warning',
    step1: 'Paste a link or message.',
    step2: 'AI checks suspicious patterns.',
    step3: 'CyberShield explains the decision.',
    step4: 'Get a clear security recommendation.',
    limitationTitle: 'Model scope',
    limitationText: 'The URL model checks phishing-related URL patterns, not malware. The message model uses a generic English SMS spam dataset and was not specifically trained on Bangladeshi scam messages.',
    privacy: 'Inputs are sent to the app for analysis; the app does not save them.',
    privacyTitle: 'Your input stays out of reports',
    privacyDetail: 'Analysis requests are processed by this app. Inputs are not saved by the application.',
    footerDescription: 'AI-assisted phishing and suspicious message detection',
    academicProject: 'Academic Project',
    loading: 'Analyzing…',
    loadingDetail: 'Checking security indicators',
    error: 'Something went wrong.',
    safe: 'Safe',
    lowRisk: 'Low Risk',
    suspicious: 'Suspicious',
    highRisk: 'High Risk',
    dangerous: 'Dangerous',
    recommendation: 'Recommended action',
    warning: 'Warning',
    explanation: 'Why did CyberShield make this decision?',
    factors: 'Indicators returned by the model',
    technicalDetails: 'Technical Details',
    phishingRisk: 'Phishing risk',
    spamRisk: 'Spam-pattern score',
    phishingProbability: 'Phishing probability',
    legitimateProbability: 'Legitimate probability',
    spamProbability: 'Spam probability',
    hamProbability: 'Ham probability',
    prediction: 'Prediction class',
    featureContribution: 'Feature contribution',
    selected: 'Selected model',
    comparison: 'Model comparison',
    accuracy: 'Accuracy',
    precision: 'Precision',
    recall: 'Recall',
    f1Score: 'F1 score',
    urlModels: 'URL Models',
    messageModels: 'Message Models',
    urlEvaluation: 'Official evaluation: domain-grouped split',
    modelUnavailable: 'No saved metrics are available.',
    model: 'Model',
    noTechnicalDetails: 'No additional technical details were returned.',
    whyFactor: 'Influenced toward',
    direction_phishing: 'phishing',
    direction_legitimate: 'legitimate',
    direction_suspicious: 'suspicious',
    direction_benign: 'benign',
    noFactors: 'No factor details available.',
    enterUrl: 'Please enter a URL first.',
    enterMessage: 'Please enter a message first.',
    invalidUrl: 'Please enter a valid URL, such as https://example.com.',
    invalidInput: 'Please provide valid input.',
    urlExample: 'https://example.com/login',
    messageExample: 'Congratulations! You won a free prize. Call now!'
  },
  bn: {
    tagline: 'ফিশিং ও প্রতারণামূলক মেসেজ থেকে এআই-চালিত সুরক্ষা',
    dashboard: 'ড্যাশবোর্ড',
    checkUrl: 'লিংক পরীক্ষা',
    checkMessage: 'মেসেজ পরীক্ষা',
    performance: 'মডেল পারফরম্যান্স',
    about: 'কীভাবে কাজ করে',
    lightMode: 'লাইট মোড',
    darkMode: 'ডার্ক মোড',
    heroKicker: 'ক্লিক করার আগে নিরাপত্তা যাচাই',
    heroTitle: 'বিশ্বাস করার আগে যাচাই করুন',
    heroText: 'পাসওয়ার্ড, OTP বা আর্থিক তথ্য দেওয়ার আগে সন্দেহজনক লিংক বা মেসেজ বিশ্লেষণ করুন।',
    linkType: 'লিংক যাচাই',
    messageType: 'মেসেজ যাচাই',
    urlTitle: 'একটি লিংক যাচাই করুন',
    urlIntro: 'ফিশিং-সম্পর্কিত URL প্যাটার্ন দেখতে লিংক পেস্ট করুন। CyberShield লিংকটি খোলে না।',
    urlLabel: 'যে লিংকটি যাচাই করবেন',
    urlHint: 'লিংকটি টেক্সট হিসেবে বিশ্লেষিত হয়; খোলা হয় না।',
    urlPlaceholder: 'https://example.com/login',
    analyzeUrl: 'লিংক বিশ্লেষণ',
    messageTitle: 'একটি মেসেজ যাচাই করুন',
    messageIntro: 'স্প্যাম বা প্রতারণার সঙ্গে সম্পর্কিত শব্দের ধরন পরীক্ষা করুন।',
    messageLabel: 'যে মেসেজটি যাচাই করবেন',
    messageHint: 'মেসেজ মডেলটি সাধারণ ইংরেজি SMS স্প্যাম ডেটা ব্যবহার করে।',
    messagePlaceholder: 'সন্দেহজনক SMS বা মেসেজ এখানে পেস্ট করুন...',
    analyzeMessage: 'মেসেজ বিশ্লেষণ',
    performanceIntro: 'বিদ্যমান প্রশিক্ষণ প্রক্রিয়ার মূল্যায়ন ফলাফল।',
    loadingMetrics: 'মডেল পারফরম্যান্স লোড হচ্ছে…',
    researchResults: 'গবেষণার ফলাফল',
    process: 'বিশ্লেষণের ধাপ',
    aboutTitle: 'CyberShield BD যেভাবে কাজ করে',
    aboutIntro: 'লিংক বা মেসেজে যুক্ত হওয়ার আগে একটি পরিষ্কার যাচাই।',
    stepInputTitle: 'ইনপুট',
    stepDetectionTitle: 'এআই শনাক্তকরণ',
    stepXaiTitle: 'ব্যাখ্যাযোগ্য এআই',
    stepWarningTitle: 'নিরাপত্তা সতর্কতা',
    step1: 'একটি লিংক বা মেসেজ পেস্ট করুন।',
    step2: 'এআই সন্দেহজনক প্যাটার্ন পরীক্ষা করে।',
    step3: 'CyberShield সিদ্ধান্তের ব্যাখ্যা দেয়।',
    step4: 'নিরাপত্তার জন্য স্পষ্ট পরামর্শ পান।',
    limitationTitle: 'মডেলের সীমা',
    limitationText: 'URL মডেল ফিশিং-সম্পর্কিত URL প্যাটার্ন পরীক্ষা করে, ম্যালওয়্যার নয়। মেসেজ মডেলটি সাধারণ ইংরেজি SMS স্প্যাম ডেটা ব্যবহার করে; এটি বাংলাদেশি প্রতারণামূলক মেসেজে বিশেষভাবে প্রশিক্ষিত নয়।',
    privacy: 'বিশ্লেষণের জন্য ইনপুট অ্যাপে পাঠানো হয়; অ্যাপ ইনপুট সংরক্ষণ করে না।',
    privacyTitle: 'আপনার ইনপুট রিপোর্টে সংরক্ষিত হয় না',
    privacyDetail: 'এই অ্যাপ বিশ্লেষণের অনুরোধ প্রক্রিয়া করে। অ্যাপ ইনপুট সংরক্ষণ করে না।',
    footerDescription: 'ফিশিং ও সন্দেহজনক মেসেজ শনাক্তে এআই সহায়তা',
    academicProject: 'একাডেমিক প্রজেক্ট',
    loading: 'বিশ্লেষণ হচ্ছে…',
    loadingDetail: 'নিরাপত্তা নির্দেশক পরীক্ষা হচ্ছে',
    error: 'কিছু সমস্যা হয়েছে।',
    safe: 'নিরাপদ',
    lowRisk: 'কম ঝুঁকি',
    suspicious: 'সন্দেহজনক',
    highRisk: 'উচ্চ ঝুঁকি',
    dangerous: 'বিপজ্জনক',
    recommendation: 'সুপারিশ',
    warning: 'সতর্কতা',
    explanation: 'CyberShield কেন এই সিদ্ধান্ত নিয়েছে?',
    factors: 'মডেল থেকে পাওয়া নির্দেশক',
    technicalDetails: 'প্রযুক্তিগত তথ্য',
    phishingRisk: 'ফিশিং ঝুঁকি',
    spamRisk: 'স্প্যাম প্যাটার্ন স্কোর',
    phishingProbability: 'ফিশিং সম্ভাবনা',
    legitimateProbability: 'বৈধ হওয়ার সম্ভাবনা',
    spamProbability: 'স্প্যাম সম্ভাবনা',
    hamProbability: 'হ্যাম সম্ভাবনা',
    prediction: 'পূর্বাভাস শ্রেণি',
    featureContribution: 'বৈশিষ্ট্যের অবদান',
    selected: 'নির্বাচিত মডেল',
    comparison: 'মডেলের তুলনা',
    accuracy: 'নির্ভুলতা',
    precision: 'প্রিসিশন',
    recall: 'রিকল',
    f1Score: 'F1 স্কোর',
    urlModels: 'URL মডেল',
    messageModels: 'মেসেজ মডেল',
    urlEvaluation: 'অফিশিয়াল মূল্যায়ন: ডোমেইন-গ্রুপড বিভাজন',
    modelUnavailable: 'সংরক্ষিত কোনো মেট্রিক পাওয়া যায়নি।',
    model: 'মডেল',
    noTechnicalDetails: 'অতিরিক্ত প্রযুক্তিগত তথ্য ফেরত আসেনি।',
    whyFactor: 'প্রভাবিত করেছে',
    direction_phishing: 'ফিশিং',
    direction_legitimate: 'বৈধ',
    direction_suspicious: 'সন্দেহজনক',
    direction_benign: 'নিরাপদ',
    noFactors: 'কোনো বিস্তারিত তথ্য নেই।',
    enterUrl: 'প্রথমে একটি URL লিখুন।',
    enterMessage: 'প্রথমে একটি মেসেজ লিখুন।',
    invalidUrl: 'দয়া করে সঠিক URL দিন, উদাহরণ: https://example.com.',
    invalidInput: 'দয়া করে সঠিক ইনপুট দিন।',
    urlExample: 'https://example.com/login',
    messageExample: 'Congratulations! You won a free prize. Call now!'
  }
};

const state = {
  language: localStorage.getItem('cybershield-language') || 'en',
  theme: localStorage.getItem('cybershield-theme') || 'dark',
  page: 'dashboard'
};

function t(key) {
  const current = translations[state.language] || translations.en;
  return current[key] || translations.en[key] || key;
}

async function callApi(url, payload) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'Request failed');
  }
  return data;
}

function setTheme(theme) {
  state.theme = theme === 'light' ? 'light' : 'dark';
  document.body.dataset.theme = state.theme;
  localStorage.setItem('cybershield-theme', state.theme);

  const themeButton = document.getElementById('themeToggle');
  if (themeButton) {
    themeButton.querySelector('[data-theme-icon]').textContent = state.theme === 'dark' ? '☼' : '☾';
    themeButton.querySelector('[data-i18n]').textContent = state.theme === 'dark' ? t('lightMode') : t('darkMode');
  }
}

function setLanguage(language) {
  state.language = language;
  localStorage.setItem('cybershield-language', language);

  document.documentElement.lang = language === 'bn' ? 'bn' : 'en';
  document.querySelectorAll('[data-i18n]').forEach((element) => {
    const key = element.dataset.i18n;
    if (translations[language] && translations[language][key]) {
      element.textContent = translations[language][key];
    }
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
    const key = element.dataset.i18nPlaceholder;
    if (translations[language]?.[key]) element.placeholder = translations[language][key];
  });

  const languageButton = document.getElementById('languageToggle');
  if (languageButton) {
    languageButton.textContent = language === 'en' ? 'বাংলা' : 'English';
  }

  const pageTitle = document.getElementById('pageTitle');
  if (pageTitle) {
    const pageMap = {
      dashboard: t('dashboard'),
      url: t('checkUrl'),
      message: t('checkMessage'),
      performance: t('performance'),
      about: t('about')
    };
    pageTitle.textContent = pageMap[state.page] || t('dashboard');
  }
  setTheme(state.theme);
}

function switchPage(page) {
  state.page = page;
  document.querySelectorAll('.nav-link').forEach((button) => {
    button.classList.toggle('active', button.dataset.page === page);
  });
  document.querySelectorAll('.page').forEach((section) => {
    section.classList.toggle('active', section.id === page);
  });
  document.getElementById('sidebar')?.classList.remove('mobile-open');
  document.getElementById('menuButton')?.setAttribute('aria-expanded', 'false');

  const pageTitle = document.getElementById('pageTitle');
  if (pageTitle) {
    pageTitle.textContent = {
      dashboard: t('dashboard'),
      url: t('checkUrl'),
      message: t('checkMessage'),
      performance: t('performance'),
      about: t('about')
    }[page] || t('dashboard');
  }
}

function renderStatus(status) {
  const normalized = String(status || '').toUpperCase();
  const statuses = {
    SAFE: { label: t('safe'), className: 'safe', icon: '✓' },
    LOW_RISK: { label: t('lowRisk'), className: 'low-risk', icon: '·' },
    SUSPICIOUS: { label: t('suspicious'), className: 'suspicious', icon: '!' },
    HIGH_RISK: { label: t('highRisk'), className: 'high-risk', icon: '!' },
    DANGEROUS: { label: t('dangerous'), className: 'dangerous', icon: '!' }
  };
  return statuses[normalized] || statuses.SAFE;
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[character]);
}

function displayFeatureName(name) {
  const labels = {
    URLLength: 'URL length', DomainLength: 'Domain length', IsDomainIP: 'IP address in domain',
    TLDLength: 'Domain suffix length', NoOfSubDomain: 'Subdomain count',
    NoOfLettersInURL: 'Letters in URL', LetterRatioInURL: 'Letter ratio',
    NoOfDegitsInURL: 'Digits in URL', DegitRatioInURL: 'Digit ratio',
    NoOfEqualsInURL: 'Equals signs', NoOfQMarkInURL: 'Question marks',
    NoOfAmpersandInURL: 'Ampersands', NoOfOtherSpecialCharsInURL: 'Other special characters',
    SpacialCharRatioInURL: 'Special-character ratio', IsHTTPS: 'HTTPS',
    NoOfObfuscatedChar: 'Encoded characters', ObfuscationRatio: 'Encoded-character ratio',
    HasObfuscation: 'URL encoding'
  };
  return labels[name] || name;
}

function renderResult(container, result) {
  const status = renderStatus(result.status);
  const factors = Array.isArray(result.top_factors) ? result.top_factors : [];
  const isUrl = result.type === 'url';
  const riskScore = Number(result.risk_score ?? 0);
  const scoreDigits = isUrl ? 6 : 2;
  const factorsHtml = factors.length
    ? `<ul class="factor-list">${factors.map((item) => {
        const factorName = item.term || (item.feature ? displayFeatureName(item.feature) : '');
        const direction = item.direction ? `${t('whyFactor')} ${t(`direction_${item.direction}`)}` : '';
        const marker = item.direction === 'phishing' || item.direction === 'suspicious' ? '!' : '•';
        return `<li><span class="factor-mark" aria-hidden="true">${marker}</span><span><strong>${escapeHtml(factorName)}</strong>${direction ? `<small>${escapeHtml(direction)}</small>` : ''}</span></li>`;
      }).join('')}</ul>`
    : `<p class="empty-note">${t('noFactors')}</p>`;

  const technicalRows = [
    [t('prediction'), result.prediction],
    ...(isUrl ? [
      [t('phishingProbability'), `${Number(result.phishing_probability ?? riskScore).toFixed(scoreDigits)}%`],
      [t('legitimateProbability'), `${Number(result.legitimate_probability ?? 0).toFixed(scoreDigits)}%`],
      ['Status basis', result.status_basis]
    ] : [
      [t('spamRisk'), `${riskScore.toFixed(2)}%`],
      [t('spamProbability'), `${Number(result.spam_probability ?? riskScore).toFixed(2)}%`],
      [t('hamProbability'), `${Number(result.ham_probability ?? 0).toFixed(2)}%`],
      ['Status basis', result.status_basis]
    ])
  ].filter(([, value]) => value !== undefined && value !== null);
  const technicalFactors = factors.map((item) => `
    <li><code>${escapeHtml(item.term || item.feature || 'factor')}</code>
      <span>${escapeHtml(item.direction || '')}</span>
      ${item.value !== undefined ? `<span>value: ${escapeHtml(item.value)}</span>` : ''}
      ${item.contribution !== undefined ? `<span>${t('featureContribution')}: ${Number(item.contribution).toFixed(4)}</span>` : ''}
      ${item.explanation ? `<span>${escapeHtml(item.explanation)}</span>` : ''}
    </li>`).join('');

  container.innerHTML = `
    <article class="result-card ${status.className}">
      <header class="result-banner">
        <div class="status-heading"><span class="status-icon" aria-hidden="true">${status.icon}</span><div><span class="status-label">${status.label}</span><h3>${escapeHtml(result.label || 'Result')}</h3></div></div>
        <div class="score-display"><strong>${riskScore.toFixed(scoreDigits)}<small>%</small></strong><span>${isUrl ? t('phishingRisk') : t('spamRisk')}</span></div>
      </header>
      <div class="result-body">
        <div class="risk-track" role="img" aria-label="${escapeHtml(t(isUrl ? 'phishingRisk' : 'spamRisk'))}: ${riskScore.toFixed(scoreDigits)} out of 100"><span style="width:${Math.max(0, Math.min(100, riskScore))}%"></span></div>
        <p class="result-warning">${escapeHtml(result.warning || '')}</p>
        <div class="recommendation-box"><strong>${t('recommendation')}</strong><p>${escapeHtml(result.recommendation || '')}</p></div>
        <section class="why-section">
          <h4>${t('explanation')}</h4>
          <p class="model-explanation">${escapeHtml(result.explanation || '')}</p>
          <h5>${t('factors')}</h5>
          ${factorsHtml}
        </section>
        <details class="technical-details">
          <summary>${t('technicalDetails')}</summary>
          ${technicalRows.length ? `<dl>${technicalRows.map(([key, value]) => `<div><dt>${escapeHtml(key)}</dt><dd>${escapeHtml(value)}</dd></div>`).join('')}</dl>` : `<p>${t('noTechnicalDetails')}</p>`}
          ${technicalFactors ? `<ul class="technical-factor-list">${technicalFactors}</ul>` : ''}
        </details>
      </div>
    </article>
  `;
}

async function analyzeForm({ inputId, resultId, buttonId, endpoint, field, emptyMessage }) {
  const input = document.getElementById(inputId);
  const resultEl = document.getElementById(resultId);
  const button = document.getElementById(buttonId);
  const value = input.value.trim();
  if (button.disabled) return;

  if (!value) {
    input.setAttribute('aria-invalid', 'true');
    input.focus();
    resultEl.innerHTML = `<p class="form-error" role="alert">${t(emptyMessage)}</p>`;
    return;
  }
  input.removeAttribute('aria-invalid');

  const buttonLabel = button.innerHTML;
  button.disabled = true;
  button.setAttribute('aria-busy', 'true');
  resultEl.innerHTML = `<div class="loading-card" role="status"><span class="spinner" aria-hidden="true"></span><div><strong>${t('loading')}</strong><span>${t('loadingDetail')}</span></div></div>`;

  try {
    const response = await callApi(endpoint, { [field]: value });
    renderResult(resultEl, response);
  } catch (error) {
    resultEl.innerHTML = `<p class="form-error" role="alert">${escapeHtml(error.message || t('error'))}</p>`;
  } finally {
    button.disabled = false;
    button.removeAttribute('aria-busy');
    button.innerHTML = buttonLabel;
  }
}

function analyzeUrl() {
  return analyzeForm({ inputId: 'urlInput', resultId: 'urlResult', buttonId: 'urlButton', endpoint: '/api/analyze/url', field: 'url', emptyMessage: 'enterUrl' });
}

function analyzeMessage() {
  return analyzeForm({ inputId: 'messageInput', resultId: 'messageResult', buttonId: 'messageButton', endpoint: '/api/analyze/message', field: 'message', emptyMessage: 'enterMessage' });
}

async function loadMetrics() {
  const metricsContainer = document.getElementById('metricsContent');
  if (!metricsContainer) return;

  metricsContainer.innerHTML = '<div class="loading-card"><p>' + t('loadingMetrics') + '</p></div>';

  try {
    const response = await fetch('/api/metrics');
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Metric load failed');
    }

    const urlData = data.url || {};
    const urlMetrics = urlData.domain_grouped_split || {};
    const messageMetrics = data.message || {};
    const urlSelected = urlData.selected_model || '';
    const messageSelected = messageMetrics.selected_model || '';
    const displayModelName = (name) => ({ LogisticRegression: 'Logistic Regression', RandomForest: 'Random Forest' }[name] || name);
    const metricCards = (metrics, selectedModel) => {
      const entries = Object.entries(metrics).filter(([, values]) => values && typeof values === 'object');
      if (!entries.length) return `<p class="empty-note">${t('modelUnavailable')}</p>`;
      return entries.map(([name, values]) => `
        <article class="metric-card ${name === selectedModel ? 'is-selected' : ''}">
          <div class="metric-card-heading"><h4>${escapeHtml(displayModelName(name))}</h4>${name === selectedModel ? `<span class="selected-badge">${t('selected')}</span>` : ''}</div>
          <dl class="metric-values">
            <div><dt>${t('accuracy')}</dt><dd>${values.accuracy !== undefined ? `${(Number(values.accuracy) * 100).toFixed(2)}%` : '—'}</dd></div>
            <div><dt>${t('precision')}</dt><dd>${values.precision !== undefined ? `${(Number(values.precision) * 100).toFixed(2)}%` : '—'}</dd></div>
            <div><dt>${t('recall')}</dt><dd>${values.recall !== undefined ? `${(Number(values.recall) * 100).toFixed(2)}%` : '—'}</dd></div>
            <div><dt>${t('f1Score')}</dt><dd>${values.f1_score !== undefined ? `${(Number(values.f1_score) * 100).toFixed(2)}%` : '—'}</dd></div>
          </dl>
        </article>
      `).join('');
    };

    metricsContainer.innerHTML = `
      <section class="metric-panel">
        <div class="metric-panel-heading"><div><p class="section-kicker">${t('selected')}</p><h3>${t('urlModels')}</h3></div><span class="model-chip">${escapeHtml(displayModelName(urlSelected || 'XGBoost'))}</span></div>
        <p class="small-note">${t('urlEvaluation')}</p>
        <h4 class="comparison-heading">${t('comparison')}</h4>
        <div class="metric-grid">${metricCards(urlMetrics, urlSelected)}</div>
      </section>
      <section class="metric-panel">
        <div class="metric-panel-heading"><div><p class="section-kicker">${t('selected')}</p><h3>${t('messageModels')}</h3></div><span class="model-chip">${escapeHtml(displayModelName(messageSelected || 'LogisticRegression'))}</span></div>
        <p class="small-note">${escapeHtml(t('messageHint'))}</p>
        <h4 class="comparison-heading">${t('comparison')}</h4>
        <div class="metric-grid">${metricCards(messageMetrics, messageSelected)}</div>
      </section>
    `;
  } catch (error) {
    metricsContainer.innerHTML = `<p class="form-error" role="alert">${escapeHtml(error.message || t('error'))}</p>`;
  }
}

function bindEvents() {
  document.querySelectorAll('.nav-link').forEach((button) => {
    button.addEventListener('click', () => switchPage(button.dataset.page));
  });

  document.getElementById('themeToggle')?.addEventListener('click', () => {
    setTheme(state.theme === 'dark' ? 'light' : 'dark');
  });

  document.getElementById('languageToggle')?.addEventListener('click', () => {
    setLanguage(state.language === 'en' ? 'bn' : 'en');
  });

  document.getElementById('menuButton')?.addEventListener('click', () => {
    const sidebar = document.querySelector('.sidebar');
    const isOpen = sidebar?.classList.toggle('mobile-open') || false;
    document.getElementById('menuButton')?.setAttribute('aria-expanded', String(isOpen));
  });

  document.getElementById('urlForm')?.addEventListener('submit', (event) => {
    event.preventDefault();
    analyzeUrl();
  });
  document.getElementById('messageForm')?.addEventListener('submit', (event) => {
    event.preventDefault();
    analyzeMessage();
  });
  document.getElementById('messageInput')?.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
      event.preventDefault();
      analyzeMessage();
    }
  });
}

function init() {
  setTheme(state.theme);
  setLanguage(state.language);
  switchPage(state.page);
  bindEvents();
  loadMetrics();
}

document.addEventListener('DOMContentLoaded', init);
