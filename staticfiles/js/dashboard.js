$(document).ready(function () {
    $('#apply-filters').click(function () {
        filterItems();
    });

    $('#reset-filters').click(function () {
        $('input[type="checkbox"]').prop('checked', false);
        $('#sort-by').val('date_desc');
        filterItems();
    });

    function filterItems() {
        const examTypes = getSelectedValues('exam_type');
        const locations = getSelectedValues('location');
        const categories = getSelectedValues('category');
        const modes = getSelectedValues('mode');
        const schemeTypes = getSelectedValues('scheme_type');
        const eligibility = getSelectedValues('eligibility');
        const sortBy = $('#sort-by').val();

        filterSection('#exams-container .card', examTypes, locations, categories, modes, eligibility, sortBy, true);
        filterSection('#schemes-container .card', [], locations, categories, [], eligibility, sortBy, false, schemeTypes);
    }

    function getSelectedValues(name) {
        return $('input[name="' + name + '"]:checked').map(function () {
            return normalize($(this).val());
        }).get();
    }

    // --- Normalize values (for consistent matching) ---
    function normalize(value) {
        if (!value) return "";
        value = value.toString().toLowerCase().trim();
        if (value.includes("delhi")) return "delhi"; // handles "delhi ncr"
        if (value.includes("all-india") || value.includes("india")) return "all-india";
        return value;
    }

    function filterSection(selector, examTypes, locations, categories, modes, eligibility, sortBy, isExam, schemeTypes = []) {
        $(selector).each(function () {
            const card = $(this);
            let show = true;

            const cardExamType = normalize(card.data('exam-type'));
            const cardSchemeType = normalize(card.data('scheme-type'));
            const cardLocation = normalize(card.data('location'));
            const cardCategory = normalize(card.data('category'));
            const cardMode = normalize(card.data('mode'));
            const cardEligibility = normalize(card.data('eligibility'));

            if (isExam) {
                if (examTypes.length > 0 && !examTypes.includes(cardExamType)) show = false;
                if (modes.length > 0 && !modes.includes(cardMode)) show = false;
            } else {
                if (schemeTypes.length > 0 && !schemeTypes.includes(cardSchemeType)) show = false;
            }

            // Location filter with "all-india" special case
            if (locations.length > 0) {
                if (cardLocation === "all-india") {
                    // "All India" exams/schemes should always pass location filter
                    show = true;
                } else if (!locations.includes(cardLocation)) {
                    show = false;
                }
            }

            if (categories.length > 0 && !categories.includes(cardCategory)) show = false;
            if (eligibility.length > 0 && !eligibility.includes(cardEligibility)) show = false;

            card.toggle(show);
        });

        sortItems(selector, sortBy);
    }

    function sortItems(selector, sortBy) {
        const container = $(selector).parent();
        const items = $(selector).filter(':visible').get();

        items.sort(function (a, b) {
            const aData = $(a).data();
            const bData = $(b).data();

            switch (sortBy) {
                case 'date_asc': return new Date(aData.date) - new Date(bData.date);
                case 'date_desc': return new Date(bData.date) - new Date(aData.date);
                case 'name_asc': return $(a).find('h3').text().localeCompare($(b).find('h3').text());
                case 'name_desc': return $(b).find('h3').text().localeCompare($(a).find('h3').text());
                default: return 0;
            }
        });

        $.each(items, function (idx, item) {
            container.append(item);
        });
    }
    function toggleMenu() {
        document.querySelector('.nav-left').classList.toggle('show');
        document.querySelector('.nav-right').classList.toggle('show');
    }
});


