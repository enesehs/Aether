window.addEventListener("scroll", () => {
    const header = document.querySelector("header");
    const githubCorner = document.querySelector(".githubcorner");
    if (window.scrollY > 550) {
        header.style.opacity = "0";
        header.style.pointerEvents = "none";
        if (githubCorner) {
            githubCorner.style.opacity = "0";
            githubCorner.style.pointerEvents = "none";
        }
    } else {
        header.style.opacity = "1";
        if (githubCorner) {
            githubCorner.style.opacity = "1";
            githubCorner.style.pointerEvents = "auto";
        }
    }
});


window.addEventListener("scroll", () => {
    const scrollImg = document.getElementById("scroll");
    if (scrollImg) {
        scrollImg.style.transition = "opacity 0.3s ease";
        scrollImg.style.opacity = window.scrollY > 2 ? "0" : "1";
    }
});

let cards = document.querySelectorAll('.card');
cards.forEach(card => {
    card.onmousemove = function(e){
        let x = e.pageX - card.offsetLeft;
        let y = e.pageY - card.offsetTop;

        card.style.setProperty('--x', x + 'px');
        card.style.setProperty('--y', y + 'px');
    }
})

document.querySelector('header a[title="Support"]').addEventListener('click', function(e) {
    const createHeart = () => {
        const heart = document.createElement('div');
        const size = Math.random() * 25 + 15; // More varied sizes
        const duration = Math.random() * 2 + 1; // More varied durations
        const symbols = ['❤️', '💖', '💝', '💗', '💓']; // Different heart styles
        
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
        setTimeout(() => heart.remove(), duration * 1000); // Clean up based on duration
    };

    // Create hearts with dynamic count based on screen size
    const heartCount = Math.min(Math.floor(window.innerWidth / 50), 15);
    for (let i = 0; i < heartCount; i++) {
        setTimeout(() => createHeart(), i * 80);
    }
});

if (!document.querySelector('#heart-animation')) {
    const style = document.createElement('style');
    style.id = 'heart-animation';
    style.textContent = `
        @keyframes floatUp {
            0% { transform: translateY(0) scale(1) rotate(0); }
            50% { transform: translateY(-50vh) scale(1.2) rotate(0deg); }
            100% { 
                transform: translateY(-100vh) scale(1) rotate(360deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}


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
        setTimeout(() => { messageDiv.style.opacity = "1"; }, 100);
        setTimeout(() => {
        messageDiv.style.opacity = "0";
        setTimeout(() => { document.body.removeChild(messageDiv); }, 500);
        }, 3000);
    }
    
    ["mac"].forEach(id => {
        document.getElementById(id).addEventListener("click", function(event) {
        event.preventDefault();
        showMessage("We are sorry, MacOS port is under development.");
        });
    });
    ["lnx"].forEach(id => {
        document.getElementById(id).addEventListener("click", function(event) {
        event.preventDefault();
        showMessage("We are sorry, Linux port is under development.");
        });
    });
    