function toggleSubcategories(categoryId, subcategoryDivId) {
    var categoryCheckbox = document.getElementById(categoryId);
    var subcategoriesDiv = document.getElementById(subcategoryDivId);
    subcategoriesDiv.style.display = categoryCheckbox.checked ? "block" : "none";
}

document.getElementById("communication").addEventListener("change", function() {
    toggleSubcategories("communication", "communication-subcategories");
});
document.getElementById("religious").addEventListener("change", function() {
    toggleSubcategories("religious", "religious-subcategories");
});

document.getElementById("inscriptions").addEventListener("change", function() {
    toggleSubcategories("inscriptions", "inscriptions-subcategories");
});

document.getElementById("fortifications").addEventListener("change", function() {
    toggleSubcategories("fortifications", "fortifications-subcategories");
});

document.getElementById("settlements").addEventListener("change", function() {
    toggleSubcategories("settlements", "settlements-subcategories");
});

document.getElementById("manuscripts").addEventListener("change", function() {
    toggleSubcategories("manuscripts", "manuscripts-subcategories");
});

document.getElementById("economy").addEventListener("change", function() {
    toggleSubcategories("economy", "economy-subcategories");
});
document.getElementById("other").addEventListener("change", function() {
    toggleSubcategories("other", "other-subcategories");
});
document.getElementById("linear").addEventListener("change", function() {
    toggleSubcategories("linear", "linear-subcategories");
});
document.getElementById("burials").addEventListener("change", function() {
    toggleSubcategories("burials", "burials-subcategories");
});
document.getElementById("water").addEventListener("change", function() {
    toggleSubcategories("water", "water-subcategories");
});

function updateHoriSelector() {
    var tabs = $('#navbarSupportedContent');
    var activeTab = tabs.find('.active');
    var activeWidth = activeTab.innerWidth();
    var activePosition = activeTab.position();

    var horiSelector = $(".hori-selector");
    horiSelector.css({
        "width": activeWidth + "px",
        "left": activePosition.left + "px"
    });
}

$(document).ready(function() {
    updateHoriSelector();
});

$(window).on('resize', function() {
    updateHoriSelector();
});

$("#navbarSupportedContent").on("click", "li", function(e) {
    $('#navbarSupportedContent ul li').removeClass("active");
    $(this).addClass('active');
    updateHoriSelector();
});

$("#navbarSupportedContent ul li").hover(
    function () { 
        var width = $(this).innerWidth();
        var left = $(this).position().left;
        $(".hori-selector").css({ "width": width + "px", "left": left + "px" });
    },
    function () { 
        var activeTab = $('#navbarSupportedContent ul li.active');
        var activeWidth = activeTab.innerWidth();
        var activePosition = activeTab.position();
        $(".hori-selector").css({ "width": activeWidth + "px", "left": activePosition.left + "px" });
    }
); 

document.getElementById("completeForm").addEventListener("submit", function (e) {
    var checked = false;

    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            checked = true;
        }
    });

    if (!checked) {
        alert("Please select at least one checkbox in the category selection.");
        e.preventDefault(); // Prevent form submission
    }
});
