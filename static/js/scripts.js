// Product details
document.addEventListener("DOMContentLoaded", function() {
    const toggleButton = document.getElementById("toggleDetails");
    const productDetails = document.getElementById("productDetails");
    const closeButton = document.getElementById("closeDetails");

    toggleButton.addEventListener("click", function() {
        alert("ok")
        if (productDetails.style.display === "none") {
            productDetails.style.display = "block"; 
        } else {
            productDetails.style.display = "none"; 
        }
    });

    closeButton.addEventListener("click", function() {
        productDetails.style.display = "none"; 
    });
});
// Product details