
    // Function to toggle radio buttons visibility in SORT page
    function toggleRadioGroupVisibility() {
    const colorRadio = document.getElementById("colorRadio");
    const sizeRadio = document.getElementById("sizeRadio");
    const cp1 = document.getElementById("cp1");
    const sp1 = document.getElementById("sp1");
    const cp2 = document.getElementById("cp2");
    const sp2 = document.getElementById("sp2");
    const cp3 = document.getElementById("cp3");
    const sp3 = document.getElementById("sp3");
    if (colorRadio.checked) {
    cp1.style.display = "block"; // Show color parameters
    cp2.style.display = "block";
    cp3.style.display = "block";
    sp1.style.display = "none";   // Hide size parameters
    sp2.style.display = "none";
    sp3.style.display = "none";
    } else if (sizeRadio.checked) {
    cp1.style.display = "none";   // Hide color parameters
    cp2.style.display = "none";
    cp3.style.display = "none";
    sp1.style.display = "block";  // Show size parameters
    sp2.style.display = "block";
    sp3.style.display = "block";
    } else {
    cp1.style.display = "block"; // Show both color and size parameters
    cp2.style.display = "block";
    cp3.style.display = "block";
    sp1.style.display = "block";
    sp2.style.display = "block";
    sp3.style.display = "block";
    }
}
document.getElementById("myForm").addEventListener("change", toggleRadioGroupVisibility);
