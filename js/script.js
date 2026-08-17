(function() {
  'use strict';

  let slides = document.querySelectorAll('.slide');
  let currentIndex = -1;
  let totalSlides = slides.length;
  let sidePanelHidden = false;
  let slideTimer = null;

  // Configuration
  const config = {
    showCounter: true,
    showProgress: true,
    autoSlide: false,
    autoSlideDelay: 5000,
    keyboardNav: true
  };

  // Initialize on DOM load
  window.addEventListener('DOMContentLoaded', function() {
    init();
  });

  function init() {
    // Create TOC from slides
    populateTOC();
    
    // Setup event listeners
    setupEventListeners();
    
    // Initial slide
    setActiveSlide(0);
    updateProgress();
  }

  function populateTOC() {
    const tocItems = document.getElementById('slide-toc-visible');
    if (tocItems) {
      slides.forEach((slide, index) => {
        const h2 = slide.querySelector('h2');
        if (h2) {
          const li = document.createElement('li');
          // Create link to the slide
          const a = document.createElement('a');
          a.href = '#' + slide.id;
          a.textContent = h2.textContent;
          a.classList.add('toc-item');
          li.appendChild(a);
          tocItems.appendChild(li);
          // Store reference
          // TODO: add click listeners later
        }
      });
    }
  }

  // Setup all event listeners
  function setupEventListeners() {
    // Keyboard navigation
    if (config.keyboardNav) {
      document.addEventListener('keydown', handleKeydown);
    }
    
    // Window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
        if (sidePanelHidden && window.innerWidth > 768) {
          toggleSidePanel();
        }
      }, 100);
    });
    
    // Auto-slide timer if enabled
    if (config.autoSlide) {
      startAutoSlide();
    }
    
    // Footer buttons
    setupFooterButtons();
    
    // Close side panel button
    const btnCloseSidepanel = document.getElementById('btn-close-sidepanel');
    if (btnCloseSidepanel) {
      btnCloseSidepanel.addEventListener('click', function() {
        closeCurrentSlide();
        stopAutoSlide();
      });
    }
  }

  // Setup footer navigation buttons
  function setupFooterButtons() {
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const btnTop = document.getElementById('btn-top');
    
    if (btnPrev) {
      btnPrev.addEventListener('click', function(e) {
        e.preventDefault();
        if (currentIndex > 0) {
          showSlide(currentIndex - 1);
          stopAutoSlide();
        }
      });
      btnPrev.disabled = true;
    }
    
    if (btnNext) {
      btnNext.addEventListener('click', function(e) {
        e.preventDefault();
        if (currentIndex < totalSlides - 1) {
          showSlide(currentIndex + 1);
          startAutoSlide();
        }
      });
    }
    
    if (btnTop) {
      btnTop.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }
    
    // Auto-slide toggle
    const autoSlideToggle = document.getElementById('auto-slide-toggle');
    if (autoSlideToggle) {
      autoSlideToggle.addEventListener('change', function(e) {
        config.autoSlide = e.target.checked;
        if (config.autoSlide) {
          startAutoSlide();
        } else {
          stopAutoSlide();
        }
      });
    }
  }

  // Handle keyboard events
  function handleKeydown(e) {
    if (!config.keyboardNav) return;
    
    let shouldNavigate = false;
    
    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
      case ' ':
      case 'Enter':
        shouldNavigate = currentIndex < totalSlides - 1;
        break;
        
      case 'ArrowLeft':
      case 'ArrowUp':
        shouldNavigate = currentIndex > 0;
        break;
        
      case 'Home':
        showSlide(0);
        e.preventDefault();
        return;
        
      case 'End':
        showSlide(totalSlides - 1);
        e.preventDefault();
        return;
        
      case 't':
      case 'T':
        toggleSidePanel();
        e.preventDefault();
        return;
        
      case '?':
        showHelp();
        e.preventDefault();
        return;
        
      case 'Escape':
        if (sidePanelHidden) {
          stopAutoSlide();
          closeCurrentSlide();
        }
        return;
        
      case 'k':
      case 'K':
        toggleSidePanel();
        e.preventDefault();
        return;
        
      case 'x':
      case 'X':
        closeCurrentSlide();
        stopAutoSlide();
        e.preventDefault();
        return;
    }
    
    if (shouldNavigate && currentIndex >= 0 && totalSlides > 0) {
      const direction = e.key.includes('ArrowRight') || e.key === ' ' || e.key === 'Enter' || e.key === 'ArrowDown' ? 1 : -1;
      showSlide(currentIndex + direction);
    }
    e.preventDefault();
  }

  // Handle mouse events in slides
  document.body.addEventListener('click', function(e) {
    if (e.target.classList && e.target.classList.contains('slide-link') ||
        e.target.closest('.slide-link')) {
      const href = e.target.classList.contains('slide-link')
        ? e.target.getAttribute('href')
        : e.target.closest('.slide-link').getAttribute('href');
      const id = href.replace('#', '').replace('/#', '');
      const idx = Array.from(slides).findIndex(function(s) {
        return s.id === id;
      });
      if (idx !== -1) {
        e.preventDefault();
        showSlide(idx);
        stopAutoSlide();
      }
    }
  });

  // Show help dialog
  function showHelp() {
    const helpText = "Keyboard controls:\n" +
      "- Arrow keys or Enter: Next slide\n" +
      "- Shift+Arrow: Previous slide\n" +
      "- Home/End: First/Last slide\n" +
      "- T: Toggle TOC sidebar\n" +
      "- Space: Next slide\n" +
      "- X: Close slide\n" +
      "- ?, Escape: Close/Help";
    
    alert(helpText.substring(0, helpText.lastIndexOf('\n')));
  }

  // Show a slide by index
  function showSlide(index) {
    if (index < 0 || index >= totalSlides) return false;
    
    // Clear auto-slide timer
    clearTimeout(slideTimer);
    slideTimer = null;
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Update active slide - clear all, set new active
    slides.forEach(function(slide) {
      slide.classList.remove('active');
    });
    slides[index].classList.add('active');
    
    // Update current index
    currentIndex = index;
    
    // Update UI
    updateNavButtons();
    updateProgress();
    
    // Restart auto-slide if enabled
    if (config.autoSlide) {
      startAutoSlide();
    }
    
    return true;
  }

  // Update navigation button states
  function updateNavButtons() {
    const btnPrev = document.getElementById('btn-prev');
    const btnClose = document.getElementById('btn-close');
    
    if (btnPrev) {
      btnPrev.disabled = currentIndex === 0 || totalSlides <= 1;
    }
    
    const btnNext = document.getElementById('btn-next');
    if (btnNext) {
      btnNext.disabled = currentIndex === totalSlides - 1 || totalSlides <= 1;
    }
    
    if (btnClose) {
      btnClose.disabled = currentIndex === -1;
    }
  }

  // Update progress bar and counter
  function updateProgress() {
    const progressBar = document.getElementById('progress-bar');
    const counter = document.getElementById('slide-counter');
    
    if (config.showProgress && progressBar) {
      const percentage = currentIndex === -1 ? 0 : (currentIndex + 1) / totalSlides * 100;
      progressBar.style.width = percentage.toFixed(1) + '%';
    }
    
    if (config.showCounter && counter && totalSlides > 0) {
      counter.textContent = 'Slide ' + (currentIndex + 1) + ' of ' + totalSlides + ' - ' + 
        slides[currentIndex].querySelector('h2').textContent;
    }
  }

  // Start auto-slide timer
  function startAutoSlide() {
    if (config.autoSlide && !slideTimer) {
      slideTimer = setTimeout(function() {
        if (currentIndex < totalSlides - 1) {
          showSlide(currentIndex + 1);
        } else {
          slideTimer = null;
          clearTimeout(slideTimer);
        }
      }, config.autoSlideDelay);
    }
  }

  // Stop auto-slide timer
  function stopAutoSlide() {
    if (slideTimer) {
      clearTimeout(slideTimer);
      slideTimer = null;
    }
  }

  // Toggle side panel visibility
  function toggleSidePanel() {
    const sidePanel = document.getElementById('side-panel');
    const hiddenNav = document.getElementById('side-panel-toc-hidden-nav');
    
    if (sidePanelHidden) {
      // Show panel
      sidePanel.classList.remove('hidden');
      if (hiddenNav) hiddenNav.style.display = 'none';
      sidePanelHidden = false;
    } else {
      // Hide panel
      sidePanel.classList.add('hidden');
      if (hiddenNav) hiddenNav.style.display = 'block';
      sidePanelHidden = true;
      // Stop auto-slide when TOC is shown
      stopAutoSlide();
    }
  }

  // Close current slide (hide all slides)
  function closeCurrentSlide() {
    slides.forEach(function(slide) {
      slide.classList.remove('active');
    });
    // Hide TOC and close slide
    if (sidePanel) {
      sidePanel.style.display = 'none';
    }
    // Update UI
    if (config.showProgress && document.getElementById('progress-bar')) {
      // Hide or reset progress
    }
    currentIndex = -1;
    
    // Disable buttons
    updateNavButtons();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

})();