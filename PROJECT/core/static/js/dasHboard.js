
    document.addEventListener("DOMContentLoaded", function () {
        const filterCheckboxes = document.querySelectorAll(".filter-section input[type='checkbox']");
        const examCards = document.querySelectorAll(".exam-card");
        const schemeCards = document.querySelectorAll(".scheme-card");
        const applyBtn = document.getElementById("apply-filters");
        const resetBtn = document.getElementById("reset-filters");
        const examsNoResults = document.getElementById("exams-no-results");
        const schemesNoResults = document.getElementById("schemes-no-results");
        const sortSelect = document.getElementById("sort-by");

        // Function to filter cards
        function filterCards() {
            // Collect all selected filters
            const selectedFilters = {};
            filterCheckboxes.forEach(cb => {
                if (cb.checked) {
                    const filterName = cb.getAttribute("name");
                    if (!selectedFilters[filterName]) selectedFilters[filterName] = [];
                    selectedFilters[filterName].push(cb.value);
                }
            });

            // Get sort option
            const sortOption = sortSelect.value;
            
            // Filter exams
            let visibleExams = 0;
            examCards.forEach(card => {
                const examType = card.getAttribute("data-exam-type");
                const location = card.getAttribute("data-location");
                const category = card.getAttribute("data-category");
                const mode = card.getAttribute("data-mode");
                const eligibility = card.getAttribute("data-e_eligibility");
                const date = card.getAttribute("data-date");

                let visible = true;

                // Check each filter - only if the filter has selected values
                if (selectedFilters.exam_type && selectedFilters.exam_type.length > 0 && !selectedFilters.exam_type.includes(examType)) {
                    visible = false;
                }
                if (selectedFilters.location && selectedFilters.location.length > 0 && !selectedFilters.location.includes(location)) {
                    visible = false;
                }
                if (selectedFilters.category && selectedFilters.category.length > 0 && !selectedFilters.category.includes(category)) {
                    visible = false;
                }
                if (selectedFilters.mode && selectedFilters.mode.length > 0 && !selectedFilters.mode.includes(mode)) {
                    visible = false;
                }
                if (selectedFilters.e_eligibility && selectedFilters.e_eligibility.length > 0 && !selectedFilters.e_eligibility.includes(eligibility)) {
                    visible = false;
                }

                card.style.display = visible ? "block" : "none";
                if (visible) visibleExams++;
            });

            // Show/hide exams no results message
            examsNoResults.style.display = visibleExams === 0 ? "block" : "none";

            // Filter schemes
            let visibleSchemes = 0;
            schemeCards.forEach(card => {
                const schemeType = card.getAttribute("data-scheme-type");
                const location = card.getAttribute("data-location");
                const category = card.getAttribute("data-category");
                const eligibility = card.getAttribute("data-s_eligibility");
                const date = card.getAttribute("data-date");

                let visible = true;

                // Check each filter - only if the filter has selected values
                if (selectedFilters.scheme_type && selectedFilters.scheme_type.length > 0 && !selectedFilters.scheme_type.includes(schemeType)) {
                    visible = false;
                }
                if (selectedFilters.location && selectedFilters.location.length > 0 && !selectedFilters.location.includes(location)) {
                    visible = false;
                }
                if (selectedFilters.category && selectedFilters.category.length > 0 && !selectedFilters.category.includes(category)) {
                    visible = false;
                }
                if (selectedFilters.s_eligibility && selectedFilters.s_eligibility.length > 0 && !selectedFilters.s_eligibility.includes(eligibility)) {
                    visible = false;
                }

                card.style.display = visible ? "block" : "none";
                if (visible) visibleSchemes++;
            });

            // Show/hide schemes no results message
            schemesNoResults.style.display = visibleSchemes === 0 ? "block" : "none";

            // Sort the results
            sortCards(sortOption);
        }

        // Function to sort cards
        function sortCards(sortOption) {
            // Sort exams
            const examsContainer = document.getElementById("exams-container");
            const examCardsArray = Array.from(examCards);
            
            examCardsArray.sort((a, b) => {
                switch(sortOption) {
                    case "date_asc":
                        return new Date(a.getAttribute("data-date")) - new Date(b.getAttribute("data-date"));
                    case "date_desc":
                        return new Date(b.getAttribute("data-date")) - new Date(a.getAttribute("data-date"));
                    case "name_asc":
                        return a.querySelector("h3").textContent.localeCompare(b.querySelector("h3").textContent);
                    case "name_desc":
                        return b.querySelector("h3").textContent.localeCompare(a.querySelector("h3").textContent);
                    default:
                        return 0;
                }
            });
            
            // Reappend sorted exams
            examCardsArray.forEach(card => {
                examsContainer.appendChild(card);
            });

            // Sort schemes
            const schemesContainer = document.getElementById("schemes-container");
            const schemeCardsArray = Array.from(schemeCards);
            
            schemeCardsArray.sort((a, b) => {
                switch(sortOption) {
                    case "date_asc":
                        return new Date(a.getAttribute("data-date")) - new Date(b.getAttribute("data-date"));
                    case "date_desc":
                        return new Date(b.getAttribute("data-date")) - new Date(a.getAttribute("data-date"));
                    case "name_asc":
                        return a.querySelector("h3").textContent.localeCompare(b.querySelector("h3").textContent);
                    case "name_desc":
                        return b.querySelector("h3").textContent.localeCompare(a.querySelector("h3").textContent);
                    default:
                        return 0;
                }
            });
            
            // Reappend sorted schemes
            schemeCardsArray.forEach(card => {
                schemesContainer.appendChild(card);
            });
        }

        // Apply Filters button
        applyBtn.addEventListener("click", filterCards);

        // Reset Filters button
        resetBtn.addEventListener("click", () => {
            filterCheckboxes.forEach(cb => cb.checked = false);
            sortSelect.value = "date_desc";
            filterCards();
        });

        // Sort change event
        sortSelect.addEventListener("change", filterCards);

        // Optional: run once at start to show all cards
        filterCards();
    });
