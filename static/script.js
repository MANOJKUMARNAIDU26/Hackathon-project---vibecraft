document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const filePreview = document.getElementById('file-preview');
    const fileNameDisplay = document.querySelector('.file-name');
    const removeBtn = document.getElementById('remove-file');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingState = document.getElementById('loading-state');
    const resultsSection = document.getElementById('results-section');
    const resultsGrid = document.getElementById('results-grid');
    const analysisTableBody = document.querySelector('#analysis-table tbody');
    const extractedTextPre = document.getElementById('extracted-text-view');
    const sideNav = document.getElementById('side-nav');

    let selectedFile = null;

    // --- Drag and Drop Logic ---

    if (dropZone) {
        dropZone.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.style.borderColor = '#0f172a';
            dropZone.style.background = '#f8fafc';
        });
        dropZone.addEventListener('dragleave', () => {
            dropZone.style.borderColor = '#e2e8f0';
            dropZone.style.background = 'white';
        });
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.style.borderColor = '#e2e8f0';
            dropZone.style.background = 'white';
            if (e.dataTransfer.files.length) {
                handleFileSelect(e.dataTransfer.files[0]);
            }
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                handleFileSelect(e.target.files[0]);
            }
        });
    }

    function handleFileSelect(file) {
        const allowedTypes = ['pdf', 'docx', 'txt'];
        const extension = file.name.split('.').pop().toLowerCase();
        if (!allowedTypes.includes(extension)) {
            alert('Please upload a PDF, DOCX, or TXT file.');
            return;
        }
        selectedFile = file;
        fileNameDisplay.textContent = file.name;
        filePreview.classList.remove('hidden');
        dropZone.classList.add('hidden');
        resultsSection.classList.add('hidden');
        sideNav.classList.add('hidden');
    }

    if (removeBtn) {
        removeBtn.addEventListener('click', () => {
            selectedFile = null;
            fileInput.value = '';
            filePreview.classList.add('hidden');
            dropZone.classList.remove('hidden');
            sideNav.classList.add('hidden');
        });
    }

    // --- API Integration ---

    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', async () => {
            if (!selectedFile) return;
            filePreview.classList.add('hidden');
            loadingState.classList.remove('hidden');
            const formData = new FormData();
            formData.append('file', selectedFile);
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Analysis failed');
                }
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                alert('Error: ' + error.message);
                filePreview.classList.remove('hidden');
            } finally {
                loadingState.classList.add('hidden');
            }
        });
    }

    function displayResults(data) {
        resultsGrid.innerHTML = '';
        analysisTableBody.innerHTML = '';
        document.getElementById('suggestions-list').innerHTML = '';
        document.getElementById('skills-list').innerHTML = '';
        document.getElementById('projects-list').innerHTML = '';
        document.getElementById('experience-list').innerHTML = '';

        // ATS Score Animation
        const atsValue = document.getElementById('ats-score-value');
        const atsMeter = document.getElementById('ats-meter-fill');
        let currentScore = 0;
        const targetScore = parseInt(data.ats_score) || 0;
        const duration = 1500;
        const startTime = performance.now();

        function animateATS(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            currentScore = Math.floor(progress * targetScore);
            atsValue.textContent = `${currentScore}%`;
            atsMeter.style.width = `${currentScore}%`;
            if (progress < 1) requestAnimationFrame(animateATS);
        }
        requestAnimationFrame(animateATS);

        // Detected Skills
        const skillsList = document.getElementById('skills-list');
        data.detected_skills?.forEach(skill => {
            const tag = document.createElement('span');
            tag.className = 'skill-tag';
            tag.textContent = skill;
            skillsList.appendChild(tag);
        });

        // Insights
        const projectsList = document.getElementById('projects-list');
        const experienceList = document.getElementById('experience-list');
        data.deep_intelligence?.projects?.forEach(p => {
            const li = document.createElement('li');
            li.textContent = p;
            projectsList.appendChild(li);
        });
        data.deep_intelligence?.experience?.forEach(e => {
            const li = document.createElement('li');
            li.textContent = e;
            experienceList.appendChild(li);
        });

        // Job Suggestions
        const suggestionsList = document.getElementById('suggestions-list');
        data.job_suggestions?.forEach(job => {
            const link = document.createElement('a');
            link.href = job.url;
            link.target = '_blank';
            link.className = 'job-link';
            link.innerHTML = `<div><strong>${job.title}</strong><span>${job.company} • ${job.platform}</span></div><strong>Apply →</strong>`;
            suggestionsList.appendChild(link);
        });

        // Match Cards
        data.role_matches?.forEach((res, index) => {
            const card = document.createElement('div');
            card.className = 'match-card animate-in';
            card.style.animationDelay = `${index * 0.1}s`;
            card.innerHTML = `
                <h3>AI Suitability</h3>
                <div class="score clickable">${Math.round(res.score * 100)}%</div>
                <div style="font-weight: 800; margin-top: 1rem; color: var(--text-muted)">${res.role}</div>
                <small style="color: var(--accent-blue); font-weight: 600; cursor: pointer; display: block; margin-top: 10px;">Visual breakdown →</small>
            `;
            card.querySelector('.score').onclick = card.querySelector('small').onclick = () => showSuitabilityVisualizer(res.role, res.score);
            resultsGrid.appendChild(card);

            const row = document.createElement('tr');
            row.innerHTML = `<td>${res.role}</td><td style="color: var(--accent-blue); font-weight: 800">${Math.round(res.score * 100)}%</td><td style="font-size: 0.85rem; color: var(--text-muted)">${res.description}</td>`;
            analysisTableBody.appendChild(row);
        });

        // Roadmap
        const roadmapList = document.getElementById('skill-roadmap');
        roadmapList.innerHTML = '';
        data.skill_roadmap?.forEach((item, index) => {
            const card = document.createElement('div');
            card.className = `roadmap-card ${item.status} animate-in`;
            card.style.animationDelay = `${index * 0.1}s`;
            card.innerHTML = `<span class="status-badge">${item.status === 'learned' ? '✓ Mastered' : '! Missing'}</span><h4>${item.skill}</h4>${item.status === 'missing' ? '<small style="color: #ef4444; font-weight: 500">Tap to learn →</small>' : ''}`;
            if (item.status === 'missing') card.addEventListener('click', () => openLearningModal(item.skill));
            roadmapList.appendChild(card);
        });

        extractedTextPre.textContent = data.extracted_text || "No text extracted.";
        resultsSection.classList.remove('hidden');
        sideNav.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        initScrollSpy();
    }

    // Modal Logic
    const learningModal = document.getElementById('learning-modal');
    const visualizerModal = document.getElementById('visualizer-modal');
    const closeBtns = document.querySelectorAll('.close-modal');
    let currentSkill = '';

    function openLearningModal(skill) {
        currentSkill = skill;
        document.getElementById('modal-skill-name').textContent = `Master "${skill}" with top-tier resources:`;
        learningModal.classList.remove('hidden');
    }

    const btnFree = document.getElementById('btn-free');
    const btnPaid = document.getElementById('btn-paid');

    if (btnFree) {
        btnFree.onclick = () => {
            window.open(`https://www.youtube.com/results?search_query=${encodeURIComponent(currentSkill + ' tutorial full course')}`, '_blank');
            learningModal.classList.add('hidden');
        };
    }

    if (btnPaid) {
        btnPaid.onclick = () => {
            window.open(`https://www.google.com/search?q=best+professional+courses+for+${encodeURIComponent(currentSkill)}`, '_blank');
            learningModal.classList.add('hidden');
        };
    }

    function showSuitabilityVisualizer(role, score) {
        const pieChart = document.getElementById('pie-chart');
        const percentage = Math.round(score * 100);
        document.getElementById('visualizer-role-name').textContent = `${role} Suitability`;
        document.getElementById('legend-suit-text').textContent = `Suit: ${percentage}%`;
        document.getElementById('legend-not-suit-text').textContent = `Not Suit: ${100 - percentage}%`;
        pieChart.style.background = `conic-gradient(var(--primary-charcoal) 0% ${percentage}%, #f1f5f9 ${percentage}% 100%)`;
        visualizerModal.classList.remove('hidden');
    }

    closeBtns.forEach(btn => btn.onclick = () => {
        learningModal.classList.add('hidden');
        visualizerModal.classList.add('hidden');
    });

    window.onclick = (e) => {
        if (e.target == learningModal) learningModal.classList.add('hidden');
        if (e.target == visualizerModal) visualizerModal.classList.add('hidden');
    };

    // --- Side Nav & Scroll Spy ---

    function initScrollSpy() {
        const observerOptions = { root: null, rootMargin: '0px', threshold: 0.4 };
        const sectionObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    let id = entry.target.id || 'hero';
                    // Unified highlight for Dot 1
                    if (id === 'results-section') id = 'hero';

                    document.querySelectorAll('.side-link').forEach(link => {
                        const href = link.getAttribute('href').substring(1);
                        link.classList.toggle('active', href === id || (id === 'hero' && href === ''));
                    });
                }
            });
        }, observerOptions);

        document.querySelectorAll('section[id], header.hero').forEach(section => sectionObserver.observe(section));
    }

    document.querySelectorAll('.side-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId) || document.querySelector('header.hero');
            if (targetElement) targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    // --- UI Interactions ---
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            content.classList.toggle('active');
        });
    });
});
