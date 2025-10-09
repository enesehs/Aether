// Optimized scroll handler - combine multiple scroll listeners for better performance
let ticking = false;
const header = document.querySelector("header");
const githubCorner = document.querySelector(".githubcorner");
const scrollImg = document.getElementById("scroll");

function updateScroll() {
    const scrollY = window.scrollY;
    const isHidden = scrollY > 550;
    
    // Handle header and github corner visibility
    if (header) {
        header.style.opacity = isHidden ? "0" : "1";
        header.style.pointerEvents = isHidden ? "none" : "all";
    }
    
    if (githubCorner) {
        githubCorner.style.opacity = isHidden ? "0" : "1";
        githubCorner.style.pointerEvents = isHidden ? "none" : "all";
    }
    
    // Handle scroll image visibility
    if (scrollImg) {
        scrollImg.style.transition = "opacity 0.3s ease";
        scrollImg.style.opacity = scrollY > 2 ? "0" : "1";
    }
    
    ticking = false;
}

window.addEventListener("scroll", () => {
    if (!ticking) {
        requestAnimationFrame(updateScroll);
        ticking = true;
    }
});

// Optimized card hover effect with throttling
const cards = document.querySelectorAll('.card');
cards.forEach(card => {
    let throttleTimer = null;
    card.addEventListener('mousemove', e => {
        if (!throttleTimer) {
            throttleTimer = setTimeout(() => {
                const rect = card.getBoundingClientRect();
                card.style.setProperty('--x', `${e.clientX - rect.left}px`);
                card.style.setProperty('--y', `${e.clientY - rect.top}px`);
                throttleTimer = null;
            }, 16); // ~60fps
        }
    });
});

// Extra-cool heart and confetti animation for Support link
(() => {
    const supportLink = document.querySelector('header a[title="Support"]');
    if (!supportLink) return;


    if (!document.querySelector('#support-fx')) {
        const style = document.createElement('style');
        style.id = 'support-fx';
        style.textContent = `
            @keyframes floatUp {
                0%   { transform: translate3d(0, 5vh, 0) scale(0.8) rotate(0deg);   opacity: 0;   filter: drop-shadow(0 0 0 rgba(255,0,90,0)); }
                15%  { opacity: 1; }
                50%  { transform: translate3d(calc(var(--drift) * 0.6), -45vh, 0) scale(1.08) rotate(180deg); filter: drop-shadow(0 6px 16px rgba(255,0,90,0.35)); }
                100% { transform: translate3d(var(--drift), -100vh, 0) scale(0.95) rotate(360deg); opacity: 0; filter: drop-shadow(0 2px 6px rgba(255,0,90,0)); }
            }
            @keyframes miniFloat {
                0%   { transform: translate3d(0, 0, 0) scale(0.6); opacity: 0; }
                20%  { opacity: 1; }
                100% { transform: translate3d(var(--dx), calc(var(--dy) - 120px), 0) scale(1); opacity: 0; }
            }
            @keyframes sparkle {
                0%   { transform: translate3d(0,0,0) scale(0); opacity: 0; }
                30%  { opacity: 1; }
                100% { transform: translate3d(var(--sx), var(--sy), 0) scale(0); opacity: 0; }
            }
            @keyframes confettiBurst {
                0%   { transform: translate3d(0,0,0) rotate(0deg);   opacity: 1; }
                100% { transform: translate3d(var(--tx), var(--ty), 0) rotate(var(--rot)); opacity: 0; }
            }
            @keyframes linkPulse {
                0% { text-shadow: 0 0 0 rgba(255, 77, 148, 0); }
                50% { text-shadow: 0 0 12px rgba(255, 77, 148, 0.85), 0 0 24px rgba(255, 179, 215, 0.6); }
                100% { text-shadow: 0 0 0 rgba(255, 77, 148, 0); }
            }
            @media (prefers-reduced-motion: reduce) {
                .support-heart, .support-mini, .support-sparkle, .support-confetti { animation-duration: 600ms !important; }
            }
        `;
        document.head.appendChild(style);
    }

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function rand(min, max) { return Math.random() * (max - min) + min; }
    function choice(arr) { return arr[(Math.random() * arr.length) | 0]; }

    function createHeart() {
        const heart = document.createElement('div');
        const size = rand(18, 36);
        const duration = rand(1.1, 2.2);
        const drift = `${(Math.random() < 0.5 ? -1 : 1) * rand(5, 22)}vw`;
        const symbols = ['❤️', '💖', '💝', '💗', '💘', '💓', '💕'];

        heart.className = 'support-heart';
        heart.textContent = choice(symbols);
        heart.style.cssText = `
            position: fixed;
            bottom: -24px;
            left: ${rand(4, 96)}vw;
            font-size: ${size}px;
            line-height: 1;
            z-index: 1000;
            pointer-events: none;
            will-change: transform, opacity, filter;
            animation: floatUp ${duration}s ease-in-out forwards;
            --drift: ${drift};
            filter: saturate(1.15);
            user-select: none;
        `;
        document.body.appendChild(heart);
        setTimeout(() => heart.remove(), duration * 1000 + 50);

        // Add a couple sparkles per heart
        for (let i = 0; i < 2; i++) {
            const sp = document.createElement('div');
            sp.className = 'support-sparkle';
            sp.textContent = choice(['✦','✧','❥','•']);
            sp.style.cssText = `
                position: fixed;
                bottom: -20px;
                left: calc(${heart.style.left} + ${rand(-20, 20)}px);
                font-size: ${rand(10, 16)}px;
                color: rgba(255, 255, 255, ${rand(0.6, 0.95)});
                text-shadow: 0 0 8px rgba(255, 169, 206, 0.8);
                pointer-events: none;
                z-index: 999;
                animation: sparkle ${rand(0.8, 1.6)}s ease-out forwards;
                --sx: ${rand(-40, 40)}px;
                --sy: ${rand(-120, -40)}px;
            `;
            document.body.appendChild(sp);
            setTimeout(() => sp.remove(), 1600);
        }
    }

    function createMiniHeartBurst(x, y) {
        const n = reduced ? 5 : 10;
        for (let i = 0; i < n; i++) {
            const h = document.createElement('div');
            h.className = 'support-mini';
            h.textContent = choice(['💗', '💖', '💞', '💓', '💘']);
            const dx = rand(-80, 80);
            const dy = rand(-60, -140);
            h.style.cssText = `
                position: fixed;
                left: ${x}px;
                top: ${y}px;
                font-size: ${rand(12, 18)}px;
                pointer-events: none;
                z-index: 1001;
                will-change: transform, opacity;
                animation: miniFloat ${rand(0.7, 1.2)}s cubic-bezier(.17,.67,.29,1.2) forwards;
                --dx: ${dx}px;
                --dy: ${dy}px;
                text-shadow: 0 0 10px rgba(255, 120, 170, 0.7);
            `;
            document.body.appendChild(h);
            setTimeout(() => h.remove(), 1300);
        }
    }

    function confettiBurst(x, y) {
        const count = reduced ? 10 : 18;
        for (let i = 0; i < count; i++) {
            const c = document.createElement('div');
            const sz = rand(5, 9);
            c.className = 'support-confetti';
            c.style.cssText = `
                position: fixed;
                left: ${x}px;
                top: ${y}px;
                width: ${sz}px;
                height: ${sz * 1.6}px;
                background: hsl(${(i * (360 / count) + rand(-10, 10)) % 360}deg 85% 62%);
                border-radius: 2px;
                pointer-events: none;
                z-index: 1002;
                will-change: transform, opacity;
                transform-origin: center;
                box-shadow: 0 0 8px rgba(255,255,255,0.4);
                animation: confettiBurst ${rand(0.6, 0.95)}s ease-out forwards;
                --tx: ${rand(-140, 140)}px;
                --ty: ${rand(-160, 120)}px;
                --rot: ${rand(-540, 540)}deg;
            `;
            document.body.appendChild(c);
            setTimeout(() => c.remove(), 1000);
        }
    }

    supportLink.addEventListener('click', (e) => {
        // Pulse link text
        supportLink.style.animation = 'linkPulse 650ms ease';
        setTimeout(() => { supportLink.style.animation = ''; }, 700);

        // Global floaters
        if (!reduced) {
            const heartCount = Math.min(Math.floor(window.innerWidth / 40), 24);
            for (let i = 0; i < heartCount; i++) {
                setTimeout(createHeart, i * 60);
            }
        } else {
            // Fewer, shorter motion for reduced-motion users
            for (let i = 0; i < 6; i++) setTimeout(createHeart, i * 80);
        }

        // Local burst at click or link center (if coordinates unavailable)
        const x = e.clientX || (supportLink.getBoundingClientRect().left + supportLink.offsetWidth / 2);
        const y = e.clientY || (supportLink.getBoundingClientRect().top + supportLink.offsetHeight / 2);
        createMiniHeartBurst(x, y);
        if (!reduced) confettiBurst(x, y);
    });
})();

// Message notification function
function showMessage(message) {
    const messageDiv = document.createElement("div");
    Object.assign(messageDiv.style, {
        fontFamily: "'MonaSansExpanded', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
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
