document.addEventListener("DOMContentLoaded", function () {
    const colorRadio = document.getElementById("colorRadio");
    const sizeRadio = document.getElementById("sizeRadio");
    const colorsizeRadio = document.getElementById("colorsize");
    const colorRadios = document.querySelectorAll(".colorRadios");
    const sizeRadios = document.querySelectorAll(".sizeRadios");

    colorRadio.addEventListener("change", toggleRadioGroupVisibility);
    sizeRadio.addEventListener("change", toggleRadioGroupVisibility);
    colorsizeRadio.addEventListener("change", toggleRadioGroupVisibility);

    colorRadios.forEach(radio => {
        radio.addEventListener("change", () => {
            handleColorRadioChange(radio);
        });
    });

    sizeRadios.forEach(radio => {
        radio.addEventListener("change", () => {
            handleSizeRadioChange(radio);
        });
    });

    toggleRadioGroupVisibility();
});

function toggleRadioGroupVisibility() {
    const colorRadio = document.getElementById("colorRadio");
    const sizeRadio = document.getElementById("sizeRadio");
    const colorsizeRadio = document.getElementById("colorsize");
    const gates = document.querySelectorAll(".gate-color-size");

    if (colorRadio.checked) {
        handleColorScenario(gates);
    } else if (sizeRadio.checked) {
        handleSizeScenario(gates);
    } else if (colorsizeRadio.checked) {
        handleColorSizeScenario(gates);
    }
}

function handleColorRadioChange(selectedRadio) {
    const gateId = selectedRadio.getAttribute("data-gate");
    const otherGates = document.querySelectorAll(`.gate-color-size:not([data-gate="${gateId}"])`);
    const selectedColor = selectedRadio.value;
    
    otherGates.forEach(gate => {
        const otherColorRadios = gate.querySelectorAll(".colorRadios");
        otherColorRadios.forEach(radio => {
            if (radio.value === selectedColor) {
                radio.disabled = true;
            } else {
                radio.disabled = false;
            }
        });
    });
}

function handleSizeRadioChange(selectedRadio) {
    const gateId = selectedRadio.getAttribute("data-gate");
    const otherGates = document.querySelectorAll(`.gate-color-size:not([data-gate="${gateId}"])`);
    const selectedSize = selectedRadio.value;

    otherGates.forEach(gate => {
        const otherSizeRadios = gate.querySelectorAll(".sizeRadios");
        otherSizeRadios.forEach(radio => {
            if (radio.value === selectedSize) {
                radio.disabled = true;
            } else {
                radio.disabled = false;
            }
        });
    });
}

function handleColorScenario(gates) {
    gates.forEach(gate => {
        const colorOptions = gate.querySelectorAll(".colorRadios");
        const sizeOptions = gate.querySelectorAll(".sizeRadios");
        colorOptions.forEach(option => {
            option.style.display = "block";
            option.disabled = false;
        });
        sizeOptions.forEach(option => {
            option.style.display = "none";
            option.disabled = true;
        });
    });
}

function handleSizeScenario(gates) {
    gates.forEach(gate => {
        const colorOptions = gate.querySelectorAll(".colorRadios");
        const sizeOptions = gate.querySelectorAll(".sizeRadios");
        colorOptions.forEach(option => {
            option.style.display = "none";
            option.disabled = true;
        });
        sizeOptions.forEach(option => {
            option.style.display = "block";
            option.disabled = false;
        });
    });
}

function handleColorSizeScenario(gates) {
    gates.forEach(gate => {
        const colorOptions = gate.querySelectorAll(".colorRadios");
        const sizeOptions = gate.querySelectorAll(".sizeRadios");
        colorOptions.forEach(option => {
            option.style.display = "block";
            option.disabled = false;
        });
        sizeOptions.forEach(option => {
            option.style.display = "block";
            option.disabled = false;
        });
    });
    
    // Handle default sizes for colorsize scenario
    const sizeRadios1 = document.querySelectorAll("[name='sizeRadios1']");
    const sizeRadios2 = document.querySelectorAll("[name='sizeRadios2']");
    
    sizeRadios1.forEach(radio => {
        if (radio.value === "big") {
            radio.checked = true;
        }
    });

    sizeRadios2.forEach(radio => {
        if (radio.value === "small") {
            radio.checked = true;
        }
    });
}
