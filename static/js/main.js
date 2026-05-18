// 🔊 SOUND ALERT
function playSOSSound() {
    let sound = new Audio("https://www.soundjay.com/buttons/sounds/beep-07.mp3");
    sound.play();
}

// 🚨 SEND SOS WITH HIGH ACCURACY + PRIVACY CONFIRM
function sendSOS(event) {
    event.preventDefault();

    // ⚠️ Privacy Confirmation
    let confirmAction = confirm("⚠️ Share your LIVE location with police?\n\nThis will send your current GPS location.");

    if (!confirmAction) return;

    let btn = document.querySelector(".btn-sos");
    btn.disabled = true;
    btn.innerText = "Getting location...";

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(
            function(position) {

                let lat = position.coords.latitude;
                let lon = position.coords.longitude;
                let accuracy = position.coords.accuracy;

                console.log("LAT:", lat);
                console.log("LON:", lon);
                console.log("Accuracy:", accuracy);

                document.getElementById("lat").value = lat;
                document.getElementById("lon").value = lon;

                btn.innerText = "Sending...";

                // 🔊 play sound
                playSOSSound();

                // submit form
                document.getElementById("sosForm").submit();
            },
            function(error) {
                alert("❌ Please allow location access");

                btn.disabled = false;
                btn.innerText = "🚨";
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );

    } else {
        alert("❌ Geolocation not supported");

        btn.disabled = false;
        btn.innerText = "🚨";
    }
}


// 📍 LIVE LOCATION PREVIEW
function showLocationPreview() {
    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(
            function(position) {

                let lat = position.coords.latitude;
                let lon = position.coords.longitude;
                let accuracy = position.coords.accuracy;

                let preview = document.getElementById("locationPreview");

                if (preview) {
                    preview.innerHTML =
                        "📍 Lat: " + lat +
                        " | Lon: " + lon +
                        " (Accuracy: " + Math.round(accuracy) + "m)";
                }
            },
            function() {
                let preview = document.getElementById("locationPreview");
                if (preview) {
                    preview.innerHTML = "❌ Location permission denied";
                }
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    }
}


// ⏱ AUTO HIDE ALERT MESSAGES
setTimeout(function() {
    let alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(a) {
        a.style.opacity = "0";
        setTimeout(() => a.style.display = "none", 500);
    });
}, 3000);


// ⚠️ CONFIRM ACTION (POLICE)
function confirmAction(action) {
    return confirm("Are you sure you want to " + action + "?");
}


// 🌙 DARK MODE TOGGLE
function toggleTheme() {
    let body = document.body;
    let btn = document.getElementById("themeBtn");

    body.classList.toggle("dark-mode");

    if (body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
        if (btn) btn.innerText = "☀️";
    } else {
        localStorage.setItem("theme", "light");
        if (btn) btn.innerText = "🌙";
    }
}


// 🔁 LOAD SAVED SETTINGS
window.onload = function () {

    // THEME LOAD
    let savedTheme = localStorage.getItem("theme");
    let btn = document.getElementById("themeBtn");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
        if (btn) btn.innerText = "☀️";
    }

    // LOAD LOCATION
    showLocationPreview();
};


// ✨ SCROLL ANIMATION
window.addEventListener("scroll", function () {
    let elements = document.querySelectorAll(".fade-up");

    elements.forEach(function (el) {
        let position = el.getBoundingClientRect().top;
        let screenHeight = window.innerHeight;

        if (position < screenHeight - 100) {
            el.classList.add("show");
        }
    });
});