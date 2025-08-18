// Wait for the document to be fully loaded
$(document).ready(function() {
    // Apply filters when button is clicked
    $('#apply-filters').click(function() {
        filterItems();
    });

    // Reset filters
    $('#reset-filters').click(function() {
        $('input[type="checkbox"]').prop('checked', false);
        $('#sort-by').val('date_desc');
        filterItems();
    });

    // Main filtering function
    function filterItems() {
        // Get selected filters
        const examTypes = getSelectedValues('exam_type');
        const locations = getSelectedValues('location');
        const categories = getSelectedValues('category');
        const modes = getSelectedValues('mode');
        const schemeTypes = getSelectedValues('scheme_type');
        const eligibility = getSelectedValues('eligibility');
        const sortBy = $('#sort-by').val();

        // Filter exams
        filterSection('#exams-container .card', examTypes, locations, categories, modes, eligibility, sortBy, true);
        
        // Filter schemes
        filterSection('#schemes-container .card', [], locations, categories, [], eligibility, sortBy, false, schemeTypes);
    }

    // Helper function to get checked values
    function getSelectedValues(name) {
        return $('input[name="' + name + '"]:checked').map(function() {
            return $(this).val();
        }).get();
    }

    // Filter a specific section (exams or schemes)
    function filterSection(selector, examTypes, locations, categories, modes, eligibility, sortBy, isExam, schemeTypes = []) {
        $(selector).each(function() {
            const card = $(this);
            let show = true;

            // Check exam filters
            if (isExam) {
                if (examTypes.length > 0 && !arrayContains(examTypes, card.data('exam-type'))) {
                    show = false;
                }
                if (modes.length > 0 && !arrayContains(modes, card.data('mode'))) {
                    show = false;
                }
            } else {
                // Check scheme filters
                if (schemeTypes.length > 0 && !arrayContains(schemeTypes, card.data('scheme-type'))) {
                    show = false;
                }
            }

            // Check common filters
            if (locations.length > 0 && !arrayContains(locations, card.data('location'))) {
                show = false;
            }
            if (categories.length > 0 && !arrayContains(categories, card.data('category'))) {
                show = false;
            }
            if (eligibility.length > 0 && !arrayContains(eligibility, card.data('eligibility'))) {
                show = false;
            }

            // Show/hide card based on filters
            card.toggle(show);
        });

        // Sort the visible items
        sortItems(selector, sortBy, isExam);
    }

    // Check if an array contains a value (with partial matching)
    function arrayContains(arr, value) {
        if (!value) return false;
        return arr.some(item => value.includes(item));
    }

    // Sort items based on selected criteria
    function sortItems(selector, sortBy, isExam) {
        const container = $(selector).parent();
        const items = $(selector).filter(':visible').get();

        items.sort(function(a, b) {
            const aData = $(a).data();
            const bData = $(b).data();
            
            switch(sortBy) {
                case 'date_asc':
                    return new Date(aData.date) - new Date(bData.date);
                case 'date_desc':
                    return new Date(bData.date) - new Date(aData.date);
                case 'name_asc':
                    return $(a).find('h3').text().localeCompare($(b).find('h3').text());
                case 'name_desc':
                    return $(b).find('h3').text().localeCompare($(a).find('h3').text());
                default:
                    return 0;
            }
        });

        // Re-append sorted items
        $.each(items, function(idx, item) {
            container.append(item);
        });
    }
});