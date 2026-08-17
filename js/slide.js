/**
 * SlideShow Navigation and Interactivity
 * Handles slide navigation, state management, and DOM updates
 */

//(function() {
'use strict';

// Configuration
const CONFIG = {
    totalSlides: 6,
    slideHeight: 600,
    defaultView: 'all',
    autoScroll: false,
    sidebarDefault: false,
};

// DOM Elements container defined at module scope
const elements = {};

// State
let state = {
    currentSlide: 0,
    viewMode: CONFIG.defaultView,
    slidesToc: [],
    containerHeight: 0,
    isMobile: false,
    sidebarOpen: false,
};

// Initialize
function cacheDOM() {
    elements.app = document.querySelector('.app');
    elements.main = document.querySelector('.main');
    elements.sidebar = document.querySelector('.sidebar');
    elements.slidesTocList = document.querySelector('#toc-list');
    elements.header = document.querySelector('.header');
    elements.pager = document.querySelector('.pager');
    elements.logo = document.querySelector('.logo');
    elements.prevBtn = document.querySelector('#prev');
    elements.themeBtn = document.querySelector('#theme-toggle');
    elements.nextBtn = document.querySelector('#next');
    elements.counter = document.querySelector('.pager');
    elements.sidebarToggle = document.querySelector('#change-content');
    elements.viewModeToggle = document.querySelector('#change-viewMode');
    elements.slides = [];
}
// Determine slides
function determineSlides() {
    const contentSection = document.querySelector('.outline-2');
    //const outlineSections = contentSection.querySelectorAll('.outline-2');
    const outlineSections = Array.from(document.querySelectorAll('.outline-2'));
    if (!contentSection) return;
    outlineSections.forEach((section, idx) => {
        const h2 = section.querySelector('h2');
        const title = h2 ? h2.textContent.trim() : 'Slide ' + (idx);
        const tag = section.querySelector('.tag .tag') || section.querySelector('.tag');
        const tagType = tag ? tag.textContent.trim() : '';
        elements.slides[idx ] = {
            element: section,
            title: title,
            tagType: tagType,
        };
    });
    CONFIG.totalSlides = elements.slides.length;
}
// Setup keyboard navigation
function handleKeydown(e) {
    if (e.target.tagName === 'INPUT') return;
    e.preventDefault();
    switch(e.key) {
    case 'ArrowRight':
        e.preventDefault();
        navigateTo(state.currentSlide + 1);
	break;
    case 'ArrowLeft':
	e.preventDefault();
        navigateTo(state.currentSlide-1);
	break;
    case 'Enter':
    case ' ':
        advance();
        break;
    case 'ArrowLeft':
        retreat();
        break;
    case 'Home':
        goToSlide(0);
        break;
    case 'End':
        goToSlide(slides.length - 1);
        break;
    case 't':
        toggleTOC();
        break;
    case 'T':
        e.stopPropagation();
        toggleTOC();
        //showHelp();
        break;
    case 'x':
    case 'Escape':
        window.close();
        break;
    case 'F5':
	window.location.reload();
        break;
    case '?':
        showHelp();
        break;
    }
}

function toggleTheme() {
    var isDark = document.body.dataset.theme === 'dark';
    var html = document.documentElement;
    console.log('ciccia');
    if (!isDark) {
	// Switch to dark theme
	document.body.dataset.theme = 'dark';
	html.setAttribute('data-theme', 'dark');
	if (elements.themeBtn) {
            elements.themeBtn.textContent = '☀️ Dark';
	}
	if (elements.themeBtn) {
            elements.themeBtn.textContent = '☀️';
	}
    } else {
	// Switch to light theme
	document.body.dataset.theme = 'light';
	html.setAttribute('data-theme', 'light');
	if (elements.themeBtn) {
            elements.themeBtn.textContent = '🌙 Light';
	}
	if (elements.themeBtn) {
            elements.themeBtn.textContent = '🌙';
	}
    }
}

function toggleViewMode() {
    var mode = "one";
    if(state.viewMode == "one"){mode = "all";}
    console.log(mode);
    setViewMode(mode);
    navigateTo(state.currentSlide);
    updateSlideContents();
    updateCounter();
    updateSlideClasses();
    toggleSidebar();
}    


// Setup view buttons
function setupViewButtons() {
    const viewBtns = document.querySelectorAll('a[data-view]');
    viewBtns.forEach((btn, idx) => {
        btn.addEventListener('click', () => {
            const viewModes = ['all', 'one'];
            const newMode = viewModes[idx % viewModes.length];
            setViewMode(newMode);
        });
    });
}

// Setup slider buttons (prev/next)
function setupSliderButtons() {
    elements.prevBtn?.addEventListener('click', () => navigatePrev());
    elements.nextBtn?.addEventListener('click', () => navigateNext());
    elements.sidebarToggle?.addEventListener('click', toggleSidebar);
    elements.viewModeToggle?.addEventListener('click', toggleViewMode);
}

// Navigate to specific slide
function navigateTo(slideNum) {
    console.log(slideNum);
    if (slideNum < 0 ) slideNum = CONFIG.totalSlides;
    if (slideNum > CONFIG.totalSlides) slideNum = 0;
    state.currentSlide = slideNum;
    const section = elements.slides[slideNum]?.element;
    if (section) {
        const rect = section.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        const middleOfWindow = windowHeight / 2;
        if (CONFIG.autoScroll) {
            const slideFromTop = rect.top + rect.height / 2 - middleOfWindow;
            window.scrollTo({
                top: window.scrollY + slideFromTop,
                behavior: 'smooth'
            });
        }
    }
    updateSlideContents();
    updateCounter();
    updateSlideClasses();
    
    // Auto-collapse sidebar on mobile when sliding
    if (state.isMobile && CONFIG.viewMode === 'one') {
        toggleSidebar();
    }
}

// Navigate to next slide
function navigateNext() {
    navigateTo(state.currentSlide + 1);
}

// Navigate to previous slide
function navigatePrev() {
    navigateTo(state.currentSlide - 1);
}

// Set view mode
function setViewMode(mode) {
    state.viewMode = mode;
    
    // Update button states
    document.querySelectorAll('a[data-view]').forEach((btn, idx) => {
        const modeName = ['all', 'one'][idx];
        btn.classList.toggle('active', mode === modeName);
    });
    
    // Toggle sidebar on mode change
    if (CONFIG.sidebarDefault && mode === 'all') {
        state.sidebarOpen = true;
        elements.sidebarToggle?.classList.toggle('expanded', true);
    } else if (mode === 'one') {
        state.sidebarOpen = false;
        elements.sidebarToggle?.classList.toggle('expanded', false);
    }
    
    toggleSidebar();
}

// Toggle sidebar
function toggleSidebar() {
    const wasOpen = state.sidebarOpen;
    state.sidebarOpen = !wasOpen;
    const isMobile = window.innerWidth <= 768;
    state.isMobile = isMobile;
    CONFIG.viewMode = wasOpen ? 'all' : (state.sidebarOpen ? 'all' : 'one');
    // Update sidebar toggle button
    //elements.sidebarToggle?.classList.toggle('expanded', state.sidebarOpen);
    // Update header display
    // elements.header?.classList.toggle('no-sidebar', !state.sidebarOpen && state.isMobile);
    // Update body scrolling
    // document.body.style.overflow = state.sidebarOpen ? 'auto' : 'hidden';
    // document.body.style.paddingRight = state.sidebarOpen ? '' : '180px';
    // Update sidebar visibility
    elements.sidebar?.classList.toggle('expanded', !state.sidebarOpen);
    // Update view button visibility
    elements.prevBtn?.classList.toggle('slider-btn', state.sidebarOpen);
    elements.nextBtn?.classList.toggle('slider-btn', state.sidebarOpen);
    // Refresh pager
    if (elements.pager && state.viewMode === 'all') {
        updatePager();
    }
}

// Update slide contents (show/hide slides)
function updateSlideContents() {
    for (const numStr in elements.slides) {
        const num = parseInt(numStr);
        const slide = elements.slides[num];
        
        if (!slide) continue;
        
        const isCurrent = num === state.currentSlide;
        
        if (state.viewMode === 'one') {
            if (isCurrent) {
                slide.element.style.display = 'block';
            } else {
                slide.element.style.display = 'none';
            }
        } else {
            slide.element.style.display = 'block';
            
            // Add/remove opacity and highlight classes
            if (isCurrent) {
                slide.element.classList.add('is-current');
                slide.element.classList.remove('previous', 'next');
            } else {
                slide.element.classList.remove('is-current');
                
                if (num < state.currentSlide) {
                    slide.element.classList.add('previous');
                    slide.element.classList.remove('next');
                } else {
                    slide.element.classList.add('next');
                    slide.element.classList.remove('previous');
                }
            }
        }
    }
    
    // Scroll to current slide
    if (!state.sidebarOpen && CONFIG.autoScroll) {
        const section = elements.slides[state.currentSlide]?.element;
        if (section) {
            section.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }
    }
}

// Update pager
function updatePager() {
    if (!elements.pager) return;
    
    const progress = ((state.currentSlide - 1) / (CONFIG.totalSlides - 1)) * 100;
    elements.pager.innerHTML = `
            <span class="counter">${state.currentSlide}</span>
            <span class="of">${CONFIG.totalSlides}</span>
            ${CONFIG.viewMode === 'one' ? `<span class="progress" style="color:var(--primary)">${Math.round(progress)}%</span>` : ''}
        `;
}

// Update slide classes
function updateSlideClasses() {
    for (const numStr in elements.slides) {
        const num = parseInt(numStr);
        const slide = elements.slides[num];
        
        if (!slide) continue;
        
        const isCurrent = num === state.currentSlide;
        const container = slide.element;
        
        if (num > 1) {
            container.classList.add('is-current');
        }
        
        if (isCurrent) {
            container.classList.add('current');
            container.classList.remove('previous', 'next');
        } else if (num < state.currentSlide) {
            container.classList.add('previous');
            container.classList.remove('next');
        } else {
            container.classList.add('next');
            container.classList.remove('previous');
        }
    }
}

// Update counter
function updateCounter() {
    elements.counter.textContent = `${state.currentSlide} / ${CONFIG.totalSlides}`;
    updatePager();
}

// Update sidebar
function updateSidebar() {
    elements.slidesTocList.innerHTML = '';
    
    for (const numStr in elements.slides) {
        const num = parseInt(numStr);
        const slide = elements.slides[num];
        
        if (!slide) continue;
        
        const link = document.createElement('a');
        link.className = 'sidebar-link';
        link.setAttribute('data-slide', num);
        link.setAttribute('href', `#slide-${num}`);
        
        link.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="4"/>
                </svg>
                <span>${slide.title}</span>`;
        
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo(num);
        });
        
        elements.slidesTocList.appendChild(link);
    }
    
    state.slidesToc = Object.keys(elements.slides).map((n) => parseInt(n));
}

// Setup outline links within each slide
function setupOutlineLinks() {
    const allH2sWithClass = document.querySelectorAll('.outline-2 h2');
    
    allH2sWithClass.forEach((h2) => {
        const tag = h2.querySelector('.tag');
        // if (!tag) return;
        
        // const tagType = tag.textContent;
        // if (tagType !== 'SLIDE') return;
        
        const num = parseInt(h2.parentElement.getAttribute('data-slide-num')) || state.currentSlide;
        if (num === state.currentSlide) return;
        
        const link = document.createElement('a');
        link.className = 'slide-link';
        link.href = `#slide-${num}`;
        link.innerHTML = `
                <svg viewBox="0 0 24 24" width="14" height="14">
                    <path fill="currentColor" d="M8.59 16.59 13.17 11 8.59 6.41 10 5l6 6-6 6-1.41-1.41z"/>
                </svg>
            `;
        
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo(num);
        });
        
        h2.appendChild(link);
    });
}

// Update state
function updateState() {
    const headerHeight = elements.header?.offsetHeight || 60;
    state.containerHeight = window.innerHeight - headerHeight;
}

// Initialize everything
function init() {
    cacheDOM();
    determineSlides();
    document.addEventListener('keydown', handleKeydown);
    setupViewButtons();
    setupSliderButtons();
    updateState();
    updateCounter();
    updateSlideContents();
    setupOutlineLinks();
    updateSidebar();
    elements.themeBtn.addEventListener('click', toggleTheme);
}

// Expose to window for testing/debugging
window.SlideShow = {
    init,
    navigateTo,
    navigateNext,
    navigatePrev,
    setViewMode,
    toggleSidebar,
    getState: () => ({ ...state }),
    debug: {
        state,
        elements,
        CONFIG,
    },
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
//})();
