$(document).ready(function() {
    // Handle view details click - simpler version
    $('.view-details').on('click', function(e) {
        e.preventDefault();
        const type = $(this).data('type');
        const id = $(this).data('id');
        
        // Hide all details first
        $('.exam-details, .scheme-details').hide();
        
        // Show the selected details
        $('#' + type + '-' + id).show();
        
        // Update title
        $('#detailsTitle').text($('#' + type + '-' + id + ' h4').text());
        
        // Show the details panel
        $('#detailsPanel').addClass('active');
        $('#overlay').addClass('active');
    });
    
    // Close details panel
    $('#closeDetails, #overlay').on('click', function() {
        $('#detailsPanel').removeClass('active');
        $('#overlay').removeClass('active');
    });
    
    // Prevent closing when clicking inside the panel
    $('#detailsPanel').on('click', function(e) {
        e.stopPropagation();
    });
    
    // Remove filter buttons since we're using instant filtering
    $('.filter-buttons').remove();
    
    // Add onchange event to all filter inputs for instant filtering
    $('input[type="checkbox"], #sort-by').on('change', function() {
        applyFilters();
    });
    
    // Add a reset link in the filter header
    $('.sidebar h3').after('<div class="filter-header"><span>Filters</span><a href="#" id="reset-link" style="color: #1a73e8; font-size: 14px;">Reset All</a></div>');
    
    // Handle reset link click
    $('#reset-link').on('click', function(e) {
        e.preventDefault();
        $('input[type="checkbox"]').prop('checked', false);
        $('#sort-by').val('date_desc');
        applyFilters();
    });
    
    function applyFilters() {
        // Get selected filters
        const examTypeFilters = getSelectedValues('exam_type');
        const categoryFilters = getSelectedValues('category');
        const eligibilityFilters = getSelectedValues('e_eligibility');
        const modeFilters = getSelectedValues('mode');
        const schemeTypeFilters = getSelectedValues('scheme_type');
        const schemeEligibilityFilters = getSelectedValues('s_eligibility');
        const locationFilters = getSelectedValues('location');
        const sortBy = $('#sort-by').val();
        
        // Filter and sort exams
        filterAndSortItems('.exam-card', examTypeFilters, categoryFilters, eligibilityFilters, modeFilters, locationFilters, 'exams-no-results', 'exams-container', sortBy);
        
        // Filter and sort schemes
        filterAndSortItems('.scheme-card', schemeTypeFilters, categoryFilters, schemeEligibilityFilters, [], locationFilters, 'schemes-no-results', 'schemes-container', sortBy);
    }
    
    function getSelectedValues(name) {
        return $('input[name="' + name + '"]:checked').map(function() {
            return this.value;
        }).get();
    }
    
    function filterAndSortItems(selector, typeFilters, categoryFilters, eligibilityFilters, modeFilters, locationFilters, noResultsId, containerId, sortBy) {
        let visibleItems = [];
        
        // First filter the items
        $(selector).each(function() {
            const type = $(this).data('exam-type') || $(this).data('scheme-type') || '';
            const category = $(this).data('category') || '';
            const eligibility = $(this).data('e_eligibility') || $(this).data('s_eligibility') || '';
            const mode = $(this).data('mode') || '';
            const location = $(this).data('location') || '';
            const date = $(this).data('date') || '';
            const name = $(this).find('.card-header h3').text().trim();
            
            const typeMatch = typeFilters.length === 0 || typeFilters.includes(type);
            const categoryMatch = categoryFilters.length === 0 || categoryFilters.includes(category);
            const eligibilityMatch = eligibilityFilters.length === 0 || eligibilityFilters.includes(eligibility);
            const modeMatch = modeFilters.length === 0 || modeFilters.includes(mode);
            const locationMatch = locationFilters.length === 0 || locationFilters.includes(location);
            
            if (typeMatch && categoryMatch && eligibilityMatch && modeMatch && locationMatch) {
                // Store the element along with data needed for sorting
                visibleItems.push({
                    element: $(this),
                    date: date,
                    name: name
                });
            } else {
                $(this).hide();
            }
        });
        
        // Sort the visible items based on the selected option
        visibleItems.sort(function(a, b) {
            switch(sortBy) {
                case 'date_asc':
                    return new Date(a.date) - new Date(b.date);
                case 'date_desc':
                    return new Date(b.date) - new Date(a.date);
                case 'name_asc':
                    return a.name.localeCompare(b.name);
                case 'name_desc':
                    return b.name.localeCompare(a.name);
                default:
                    return 0;
            }
        });
        
        // Reorder the elements in the DOM based on the sorted array
        const container = $('#' + containerId);
        $.each(visibleItems, function(index, item) {
            container.append(item.element);
            item.element.show();
        });
        
        // Show/hide no results message
        if (visibleItems.length === 0) {
            $('#' + noResultsId).show();
        } else {
            $('#' + noResultsId).hide();
        }
    }
    
    // Apply filters on page load to ensure initial state
    applyFilters();
});