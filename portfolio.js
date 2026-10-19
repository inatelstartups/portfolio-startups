document.addEventListener('DOMContentLoaded', () => {
    /* ================= STARTUP PORTFOLIO FILTER & SLIDER ================= */
    const portfolioTrack = document.getElementById('portfolio-track');
    if (portfolioTrack) {
        const filterButtons = document.querySelectorAll('.filter-btn');
        const portfolioCards = document.querySelectorAll('.portfolio-card');
        const portfolioPrev = document.getElementById('portfolio-prev');
        const portfolioNext = document.getElementById('portfolio-next');
        const portfolioProgressBar = document.getElementById('portfolio-progress-bar');

        let activeFilter = 'incubated';
        let currentIndex = 0;
        let visibleCards = [];

        function getCardsPerView() {
            if (window.innerWidth > 1024) return 4;
            if (window.innerWidth > 768) return 3;
            if (window.innerWidth > 640) return 2;
            return 1;
        }

        function updatePortfolioSlider() {
            const cardsPerView = getCardsPerView();
            const maxIndex = Math.max(0, visibleCards.length - cardsPerView);
            
            if (currentIndex > maxIndex) {
                currentIndex = maxIndex;
            }

            // Apply slide animation using layout-independent CSS calculation
            if (visibleCards.length > 0) {
                const gap = window.innerWidth > 640 ? 24 : 16;
                const pct = (currentIndex / cardsPerView) * 100;
                const px = currentIndex * (gap / cardsPerView);
                portfolioTrack.style.transform = `translateX(calc(-${pct}% - ${px}px))`;
            } else {
                portfolioTrack.style.transform = 'translateX(0)';
            }

            // Show/hide arrows
            if (portfolioPrev && portfolioNext) {
                if (visibleCards.length <= cardsPerView) {
                    portfolioPrev.style.display = 'none';
                    portfolioNext.style.display = 'none';
                } else {
                    portfolioPrev.style.display = 'flex';
                    portfolioNext.style.display = 'flex';
                    portfolioPrev.style.opacity = currentIndex === 0 ? '0.3' : '1';
                    portfolioPrev.style.pointerEvents = currentIndex === 0 ? 'none' : 'auto';
                    portfolioNext.style.opacity = currentIndex === maxIndex ? '0.3' : '1';
                    portfolioNext.style.pointerEvents = currentIndex === maxIndex ? 'none' : 'auto';
                }
            }

            updatePortfolioProgress();
        }

        function updatePortfolioProgress() {
            if (!portfolioProgressBar) return;
            
            const cardsPerView = getCardsPerView();
            const maxIndex = Math.max(0, visibleCards.length - cardsPerView);
            const progressContainer = portfolioProgressBar.parentElement;
            
            if (maxIndex <= 0) {
                if (progressContainer) progressContainer.style.display = 'none';
                return;
            }
            
            if (progressContainer) progressContainer.style.display = 'block';
            
            // Progress bar width represents percentage of visible cards relative to total
            const percentageVisible = (cardsPerView / visibleCards.length) * 100;
            portfolioProgressBar.style.width = `${percentageVisible}%`;
            
            // Scroll offset represents active index relative to maximum index
            const scrollPercentage = maxIndex > 0 ? (currentIndex / maxIndex) * (100 - percentageVisible) : 0;
            portfolioProgressBar.style.left = `${scrollPercentage}%`;

            // Dynamic color based on active filter
            if (activeFilter === 'graduated') {
                portfolioProgressBar.style.background = 'var(--text-blue)';
            } else if (activeFilter === 'pre-incubated') {
                portfolioProgressBar.style.background = '#C084FC';
            } else if (activeFilter === 'ideation') {
                portfolioProgressBar.style.background = '#FACC15';
            } else {
                portfolioProgressBar.style.background = 'var(--brand-orange)';
            }
        }

        const airtableLinks = {
            'ideation': 'https://airtable.com/app9mAZl7zLu7zeZb/shr6lGlyWE9395CtX/tblAEZQFetlB1ThTe',
            'pre-incubated': 'https://airtable.com/app9mAZl7zLu7zeZb/shrQMcUOOgtk19ydG/tblAEZQFetlB1ThTe',
            'incubated': 'https://airtable.com/app9mAZl7zLu7zeZb/shrd6rAzCsgZv2elr/tblAEZQFetlB1ThTe',
            'graduated': 'https://airtable.com/app45MMiNeduNXvUx/shrHu5Ku1Q5Phv7WP/tblAEZQFetlB1ThTe'
        };

        function filterPortfolio() {
            visibleCards = Array.from(portfolioCards).filter(card => {
                const matches = (activeFilter === 'all' || card.classList.contains(activeFilter));
                if (matches) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
                return matches;
            });

            // Update Airtable CTA Link dynamically
            const ctaContainer = document.querySelector('.portfolio-cta-container');
            const ctaLink = ctaContainer ? ctaContainer.querySelector('a') : null;
            if (ctaContainer && ctaLink) {
                const link = airtableLinks[activeFilter];
                if (link) {
                    ctaLink.href = link;
                    ctaContainer.style.display = 'block';
                } else {
                    ctaContainer.style.display = 'none';
                }
            }

            currentIndex = 0;
            portfolioTrack.style.transform = 'translateX(0)';
            updatePortfolioSlider();
        }

        // Filter Buttons Listeners
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                activeFilter = btn.getAttribute('data-filter');
                filterPortfolio();
            });
        });

        // Arrow Buttons Listeners
        if (portfolioPrev) {
            portfolioPrev.addEventListener('click', () => {
                const cardsPerView = getCardsPerView();
                currentIndex = Math.max(0, currentIndex - cardsPerView);
                updatePortfolioSlider();
            });
        }

        if (portfolioNext) {
            portfolioNext.addEventListener('click', () => {
                const cardsPerView = getCardsPerView();
                const maxIndex = Math.max(0, visibleCards.length - cardsPerView);
                currentIndex = Math.min(maxIndex, currentIndex + cardsPerView);
                updatePortfolioSlider();
            });
        }

        // Dragging Progress Bar Logic
        let isDragging = false;
        const progressContainer = portfolioProgressBar ? portfolioProgressBar.parentElement : null;

        function handleDrag(clientX) {
            if (!isDragging || !progressContainer) return;
            const rect = progressContainer.getBoundingClientRect();
            
            // Calculate relative offset X within container
            let offsetX = clientX - rect.left;
            if (offsetX < 0) offsetX = 0;
            if (offsetX > rect.width) offsetX = rect.width;
            
            const cardsPerView = getCardsPerView();
            const maxIndex = Math.max(0, visibleCards.length - cardsPerView);
            if (maxIndex <= 0) return;
            
            const percentageVisible = (cardsPerView / visibleCards.length) * 100;
            const containerWidth = rect.width;
            const barWidth = (percentageVisible / 100) * containerWidth;
            const scrollableWidth = containerWidth - barWidth;
            
            let leftX = offsetX - barWidth / 2;
            if (leftX < 0) leftX = 0;
            if (leftX > scrollableWidth) leftX = scrollableWidth;
            
            const ratio = scrollableWidth > 0 ? leftX / scrollableWidth : 0;
            const targetIndex = Math.min(maxIndex, Math.max(0, Math.round(ratio * maxIndex)));
            
            if (targetIndex !== currentIndex) {
                currentIndex = targetIndex;
                updatePortfolioSlider();
            }
        }

        if (progressContainer) {
            progressContainer.addEventListener('mousedown', e => {
                isDragging = true;
                portfolioTrack.classList.add('dragging');
                portfolioProgressBar.classList.add('dragging');
                handleDrag(e.clientX);
                e.preventDefault();
            });

            progressContainer.addEventListener('touchstart', e => {
                isDragging = true;
                portfolioTrack.classList.add('dragging');
                portfolioProgressBar.classList.add('dragging');
                handleDrag(e.touches[0].clientX);
            }, { passive: true });
        }

        window.addEventListener('mousemove', e => {
            if (isDragging) {
                handleDrag(e.clientX);
            }
        });

        window.addEventListener('touchmove', e => {
            if (isDragging) {
                handleDrag(e.touches[0].clientX);
            }
        }, { passive: true });

        const endDrag = () => {
            if (isDragging) {
                isDragging = false;
                portfolioTrack.classList.remove('dragging');
                portfolioProgressBar.classList.remove('dragging');
            }
        };

        window.addEventListener('mouseup', endDrag);
        window.addEventListener('touchend', endDrag);

        // Touch Swipe Gestures
        let touchStartX = 0;
        let touchEndX = 0;

        portfolioTrack.addEventListener('touchstart', e => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        portfolioTrack.addEventListener('touchend', e => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });

        function handleSwipe() {
            const swipeThreshold = 50;
            const diff = touchStartX - touchEndX;
            const cardsPerView = getCardsPerView();
            const maxIndex = Math.max(0, visibleCards.length - cardsPerView);

            if (diff > swipeThreshold) {
                if (currentIndex < maxIndex) {
                    currentIndex = Math.min(maxIndex, currentIndex + 1);
                    updatePortfolioSlider();
                }
            } else if (diff < -swipeThreshold) {
                if (currentIndex > 0) {
                    currentIndex = Math.max(0, currentIndex - 1);
                    updatePortfolioSlider();
                }
            }
        }

        // Resize Event
        window.addEventListener('resize', () => {
            updatePortfolioSlider();
        });

        // Initialize
        filterPortfolio();
    }
});
