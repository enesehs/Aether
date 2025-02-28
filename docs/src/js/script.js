// Handle header visibility on scroll
window.addEventListener("scroll", () => {
    const header = document.querySelector("header");
    const githubCorner = document.querySelector(".githubcorner");
    const isHidden = window.scrollY > 550;
    
    header.style.opacity = isHidden ? "0" : "1";
    header.style.pointerEvents = isHidden ? "none" : "all";
    
    if (githubCorner) {
        githubCorner.style.opacity = isHidden ? "0" : "1";
        githubCorner.style.pointerEvents = isHidden ? "none" : "all";
    }
});

// Handle scroll image visibility
window.addEventListener("scroll", () => {
    const scrollImg = document.getElementById("scroll");
    if (scrollImg) {
        scrollImg.style.transition = "opacity 0.3s ease";
        scrollImg.style.opacity = window.scrollY > 2 ? "0" : "1";
    }
});

// Card hover effect
document.querySelectorAll('.card').forEach(card => {
    card.onmousemove = e => {
        card.style.setProperty('--x', `${e.pageX - card.offsetLeft}px`);
        card.style.setProperty('--y', `${e.pageY - card.offsetTop}px`);
    };
});

// Heart animation for Support link
document.querySelector('header a[title="Support"]').addEventListener('click', () => {
    if (!document.querySelector('#heart-animation')) {
        const style = document.createElement('style');
        style.id = 'heart-animation';
        style.textContent = `
            @keyframes floatUp {
                0% { transform: translateY(0) scale(1) rotate(0); }
                50% { transform: translateY(-50vh) scale(1.2) rotate(0deg); }
                100% { transform: translateY(-100vh) scale(1) rotate(360deg); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
    
    const createHeart = () => {
        const heart = document.createElement('div');
        const size = Math.random() * 25 + 15;
        const duration = Math.random() * 2 + 1;
        const symbols = ['❤️', '💖', '💝', '💗', '💓'];
        
        heart.innerHTML = symbols[Math.floor(Math.random() * symbols.length)];
        heart.style.cssText = `
            position: fixed;
            bottom: -20px;
            left: ${Math.random() * 100}vw;
            font-size: ${size}px;
            animation: floatUp ${duration}s ease-in-out;
            z-index: 1000;
            transform: rotate(${Math.random() * 90 - 45}deg);
            opacity: ${Math.random() * 0.6 + 0.4};
            pointer-events: none;
            will-change: transform, opacity;
        `;
        
        document.body.appendChild(heart);
        setTimeout(() => heart.remove(), duration * 1000);
    };
    
    const heartCount = Math.min(Math.floor(window.innerWidth / 50), 15);
    for (let i = 0; i < heartCount; i++) {
        setTimeout(createHeart, i * 80);
    }
});

// Message notification function
function showMessage(message) {
    const messageDiv = document.createElement("div");
    Object.assign(messageDiv.style, {
        fontFamily: "Mona Sans Expanded",
        position: "fixed",
        bottom: "20px",
        right: "20px",
        backgroundColor: "#080a0f52",
        backdropFilter: "blur(10px)",
        color: "#fff",
        padding: "10px 20px",
        borderRadius: "5px",
        boxShadow: "0 2px 10px rgba(0, 0, 0, 0.2)",
        zIndex: "1000",
        opacity: "0",
        transition: "opacity 0.5s ease-in-out",
    });
    messageDiv.textContent = message;
    document.body.appendChild(messageDiv);
    
    setTimeout(() => messageDiv.style.opacity = "1", 100);
    setTimeout(() => {
        messageDiv.style.opacity = "0";
        setTimeout(() => document.body.removeChild(messageDiv), 500);
    }, 3000);
}

// Handle download buttons
["mac", "lnx"].forEach(id => {
    document.getElementById(id)?.addEventListener("click", e => {
        e.preventDefault();
        showMessage(`We are sorry, ${id === "mac" ? "MacOS" : "Linux"} port is under development.`);
    });
});

document.getElementById("win")?.addEventListener("click", e => {
    e.preventDefault();
    window.location.href = "https://github.com/enesehs/Aether/releases/download/v0.1-pre-release/AetherSetup.exe";
});
