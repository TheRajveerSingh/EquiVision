/* ═══════════════════════════════════════════════════════════════
   EquiVision — Premium Interactive Animations
   Canvas particles, 3D tilt, cursor glow, confetti, typewriter
   ═══════════════════════════════════════════════════════════════ */

(function () {
    // Guard: only init once per Streamlit rerun
    if (window.__equivisionInitialized) return;
    window.__equivisionInitialized = true;

    /* ────────── 1. CANVAS STARFIELD + PARTICLES + SHOOTING STARS ────────── */
    function initParticles() {
        // Remove old canvas if present
        const old = document.getElementById('ev-particles');
        if (old) old.remove();

        const canvas = document.createElement('canvas');
        canvas.id = 'ev-particles';
        Object.assign(canvas.style, {
            position: 'fixed', top: '0', left: '0', width: '100%', height: '100%',
            zIndex: '1', pointerEvents: 'none'
        });
        // Insert canvas INSIDE .stApp as its first child — above background, below content (z-index:2)
        const stApp = document.querySelector('.stApp');
        if (stApp) {
            stApp.prepend(canvas);
        } else {
            document.body.prepend(canvas);
        }
        const ctx = canvas.getContext('2d');

        let W, H;
        function resize() {
            W = canvas.width = window.innerWidth;
            H = canvas.height = window.innerHeight;
            // Reposition any stars that fell outside
            for (const s of stars) { if (s.x > W) s.x = Math.random() * W; if (s.y > H) s.y = Math.random() * H; }
        }
        resize();
        window.addEventListener('resize', resize);

        /* ── Drifting particles (existing) ── */
        const PARTICLE_COUNT = 90;
        const particles = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            particles.push({
                x: Math.random() * W,
                y: Math.random() * H,
                r: Math.random() * 1.8 + 0.3,
                dx: (Math.random() - 0.5) * 0.3,
                dy: (Math.random() - 0.5) * 0.15 - 0.1,
                opacity: Math.random() * 0.6 + 0.2,
                pulse: Math.random() * Math.PI * 2
            });
        }

        /* ── Twinkling fixed stars ── */
        const STAR_COUNT = 70;
        const stars = [];
        const starColors = [
            [255, 255, 255],   // white
            [200, 220, 255],   // cool blue-white
            [255, 240, 220],   // warm white
            [180, 200, 255],   // blue
            [255, 220, 180],   // amber
        ];
        for (let i = 0; i < STAR_COUNT; i++) {
            stars.push({
                x: Math.random() * W,
                y: Math.random() * H,
                r: Math.random() * 1.6 + 0.4,
                baseOpacity: Math.random() * 0.5 + 0.3,
                twinkleSpeed: Math.random() * 0.04 + 0.01,
                twinklePhase: Math.random() * Math.PI * 2,
                color: starColors[Math.floor(Math.random() * starColors.length)]
            });
        }

        /* ── Shooting stars ── */
        const shootingStars = [];
        let nextShootTime = performance.now() + 1500 + Math.random() * 2000;

        function spawnShootingStar() {
            // Start from top or left edge, streak diagonally
            const fromTop = Math.random() > 0.3;
            const sx = fromTop ? Math.random() * W * 0.8 + W * 0.1 : -20;
            const sy = fromTop ? -20 : Math.random() * H * 0.4;
            const angle = (Math.random() * 30 + 15) * Math.PI / 180; // 15-45 degrees
            const speed = 8 + Math.random() * 7;

            shootingStars.push({
                x: sx, y: sy,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: 1.0,
                decay: 0.012 + Math.random() * 0.008,
                length: 60 + Math.random() * 80,
                width: 1.2 + Math.random() * 1.2
            });
        }

        let mouseX = W / 2, mouseY = H / 2;
        document.addEventListener('mousemove', e => { mouseX = e.clientX; mouseY = e.clientY; });

        function render() {
            ctx.clearRect(0, 0, W, H);

            /* ── Draw twinkling stars (stationary, behind everything) ── */
            for (const s of stars) {
                s.twinklePhase += s.twinkleSpeed;
                // Multi-frequency twinkle for realism
                const twinkle = 0.5
                    + 0.3 * Math.sin(s.twinklePhase)
                    + 0.2 * Math.sin(s.twinklePhase * 2.7 + 1.3);
                const alpha = s.baseOpacity * twinkle;
                const [cr, cg, cb] = s.color;

                // Outer glow
                const glowSize = s.r * 4;
                const grd = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, glowSize);
                grd.addColorStop(0, `rgba(${cr},${cg},${cb},${alpha * 0.5})`);
                grd.addColorStop(0.4, `rgba(${cr},${cg},${cb},${alpha * 0.15})`);
                grd.addColorStop(1, `rgba(${cr},${cg},${cb},0)`);
                ctx.fillStyle = grd;
                ctx.beginPath();
                ctx.arc(s.x, s.y, glowSize, 0, Math.PI * 2);
                ctx.fill();

                // Bright core
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(${cr},${cg},${cb},${alpha})`;
                ctx.fill();

                // Cross sparkle on brighter stars
                if (s.r > 1.0 && alpha > 0.5) {
                    const sparkleLen = s.r * 3 * alpha;
                    ctx.strokeStyle = `rgba(${cr},${cg},${cb},${alpha * 0.3})`;
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(s.x - sparkleLen, s.y);
                    ctx.lineTo(s.x + sparkleLen, s.y);
                    ctx.moveTo(s.x, s.y - sparkleLen);
                    ctx.lineTo(s.x, s.y + sparkleLen);
                    ctx.stroke();
                }
            }

            /* ── Draw drifting particles ── */
            for (const p of particles) {
                p.pulse += 0.015;
                const flicker = 0.5 + 0.5 * Math.sin(p.pulse);
                const alpha = p.opacity * flicker;

                const px = p.x + (mouseX - W / 2) * 0.01 * p.r;
                const py = p.y + (mouseY - H / 2) * 0.01 * p.r;

                ctx.beginPath();
                ctx.arc(px, py, p.r, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255,255,255,${alpha})`;
                ctx.shadowBlur = p.r * 6;
                ctx.shadowColor = `rgba(127,90,240,${alpha * 0.5})`;
                ctx.fill();
                ctx.shadowBlur = 0;

                p.x += p.dx;
                p.y += p.dy;
                if (p.x < -10) p.x = W + 10;
                if (p.x > W + 10) p.x = -10;
                if (p.y < -10) p.y = H + 10;
                if (p.y > H + 10) p.y = -10;
            }

            // Connecting lines between close particles
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 120) {
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = `rgba(127,90,240,${0.08 * (1 - dist / 120)})`;
                        ctx.lineWidth = 0.5;
                        ctx.stroke();
                    }
                }
            }

            /* ── Draw shooting stars ── */
            const now = performance.now();
            if (now >= nextShootTime) {
                spawnShootingStar();
                nextShootTime = now + 2000 + Math.random() * 3000;  // every 2-5s
            }

            for (let i = shootingStars.length - 1; i >= 0; i--) {
                const ss = shootingStars[i];
                ss.x += ss.vx;
                ss.y += ss.vy;
                ss.life -= ss.decay;

                if (ss.life <= 0 || ss.x > W + 100 || ss.y > H + 100) {
                    shootingStars.splice(i, 1);
                    continue;
                }

                // Tail: a gradient line from current pos back along its path
                const tailX = ss.x - (ss.vx / Math.sqrt(ss.vx * ss.vx + ss.vy * ss.vy)) * ss.length * ss.life;
                const tailY = ss.y - (ss.vy / Math.sqrt(ss.vx * ss.vx + ss.vy * ss.vy)) * ss.length * ss.life;

                const grad = ctx.createLinearGradient(ss.x, ss.y, tailX, tailY);
                grad.addColorStop(0, `rgba(255,255,255,${ss.life * 0.9})`);
                grad.addColorStop(0.3, `rgba(200,220,255,${ss.life * 0.5})`);
                grad.addColorStop(1, `rgba(127,90,240,0)`);

                ctx.beginPath();
                ctx.moveTo(ss.x, ss.y);
                ctx.lineTo(tailX, tailY);
                ctx.strokeStyle = grad;
                ctx.lineWidth = ss.width * ss.life;
                ctx.lineCap = 'round';
                ctx.stroke();

                // Bright head glow
                const headGlow = ctx.createRadialGradient(ss.x, ss.y, 0, ss.x, ss.y, 4);
                headGlow.addColorStop(0, `rgba(255,255,255,${ss.life})`);
                headGlow.addColorStop(1, `rgba(200,220,255,0)`);
                ctx.fillStyle = headGlow;
                ctx.beginPath();
                ctx.arc(ss.x, ss.y, 4, 0, Math.PI * 2);
                ctx.fill();
            }

            requestAnimationFrame(render);
        }
        render();
    }

    /* ────────── 2. CURSOR GLOW ────────── */
    function initCursorGlow() {
        const glow = document.createElement('div');
        glow.id = 'ev-cursor-glow';
        Object.assign(glow.style, {
            position: 'fixed', width: '350px', height: '350px',
            borderRadius: '50%', pointerEvents: 'none', zIndex: 1,
            background: 'radial-gradient(circle, rgba(127,90,240,0.08) 0%, transparent 70%)',
            transform: 'translate(-50%,-50%)', transition: 'opacity 0.3s'
        });
        document.body.appendChild(glow);

        document.addEventListener('mousemove', e => {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        });
    }

    /* ────────── 3. SCROLL PROGRESS BAR ────────── */
    function initScrollProgress() {
        const bar = document.createElement('div');
        bar.id = 'ev-scroll-progress';
        Object.assign(bar.style, {
            position: 'fixed', top: 0, left: 0, height: '3px', zIndex: 9999,
            background: 'linear-gradient(90deg, #7F5AF0, #2CB67D, #FF8906)',
            width: '0%', transition: 'width 0.1s ease-out'
        });
        document.body.appendChild(bar);

        function update() {
            // Streamlit uses a scrollable main section
            const main = document.querySelector('section.main');
            if (main) {
                const scrollTop = main.scrollTop;
                const scrollHeight = main.scrollHeight - main.clientHeight;
                const pct = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
                bar.style.width = pct + '%';
            }
            requestAnimationFrame(update);
        }
        update();
    }

    /* ────────── 4. 3D TILT ON GLASS CARDS ────────── */
    function initTiltCards() {
        function applyTilt() {
            document.querySelectorAll('.glass-card, [data-testid="stMetric"]').forEach(card => {
                if (card.__tiltBound) return;
                card.__tiltBound = true;

                card.addEventListener('mousemove', e => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    const tiltX = ((y - centerY) / centerY) * -5;
                    const tiltY = ((x - centerX) / centerX) * 5;
                    card.style.transform = `perspective(800px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateY(-5px)`;
                });

                card.addEventListener('mouseleave', () => {
                    card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) translateY(0)';
                });
            });
        }

        // Re-apply on DOM changes (Streamlit rerenders)
        const observer = new MutationObserver(applyTilt);
        observer.observe(document.body, { childList: true, subtree: true });
        applyTilt();
    }

    /* ────────── 5. MAGNETIC HOVER ON BUTTONS ────────── */
    function initMagneticButtons() {
        function applyMagnetic() {
            document.querySelectorAll('div.stButton > button').forEach(btn => {
                if (btn.__magneticBound) return;
                btn.__magneticBound = true;

                btn.addEventListener('mousemove', e => {
                    const rect = btn.getBoundingClientRect();
                    const x = e.clientX - rect.left - rect.width / 2;
                    const y = e.clientY - rect.top - rect.height / 2;
                    btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px) scale(1.03)`;
                });

                btn.addEventListener('mouseleave', () => {
                    btn.style.transform = 'translate(0,0) scale(1)';
                });

                // Ripple on click
                btn.addEventListener('click', e => {
                    const ripple = document.createElement('span');
                    const rect = btn.getBoundingClientRect();
                    const size = Math.max(rect.width, rect.height);
                    Object.assign(ripple.style, {
                        position: 'absolute', borderRadius: '50%',
                        width: size + 'px', height: size + 'px',
                        left: (e.clientX - rect.left - size / 2) + 'px',
                        top: (e.clientY - rect.top - size / 2) + 'px',
                        background: 'rgba(255,255,255,0.35)',
                        transform: 'scale(0)', animation: 'ev-ripple 0.6s ease-out',
                        pointerEvents: 'none'
                    });
                    btn.style.position = 'relative';
                    btn.style.overflow = 'hidden';
                    btn.appendChild(ripple);
                    setTimeout(() => ripple.remove(), 700);
                });
            });
        }

        const observer = new MutationObserver(applyMagnetic);
        observer.observe(document.body, { childList: true, subtree: true });
        applyMagnetic();
    }

    /* ────────── 6. TYPEWRITER EFFECT ────────── */
    function initTypewriter() {
        function apply() {
            document.querySelectorAll('.ev-typewriter').forEach(el => {
                if (el.__twDone) return;
                el.__twDone = true;
                const text = el.getAttribute('data-text') || el.textContent;
                el.textContent = '';
                el.style.borderRight = '2px solid rgba(255,255,255,0.6)';
                let i = 0;
                const interval = setInterval(() => {
                    el.textContent += text.charAt(i);
                    i++;
                    if (i >= text.length) {
                        clearInterval(interval);
                        // Blink cursor a few times then hide
                        setTimeout(() => { el.style.borderRight = 'none'; }, 2500);
                    }
                }, 45);
            });
        }
        const observer = new MutationObserver(apply);
        observer.observe(document.body, { childList: true, subtree: true });
        apply();
    }

    /* ────────── 7. ANIMATED COUNTERS ────────── */
    function initCounters() {
        function apply() {
            document.querySelectorAll('[data-testid="stMetricValue"]').forEach(el => {
                if (el.__counterDone) return;
                el.__counterDone = true;
                const text = el.textContent.trim();
                const num = parseFloat(text);
                if (isNaN(num) || num === 0) return;

                const isFloat = text.includes('.');
                const decimals = isFloat ? (text.split('.')[1] || '').length : 0;
                const suffix = text.replace(/[\d.,]/g, '');
                const duration = 1200;
                const start = performance.now();

                function tick(now) {
                    const elapsed = now - start;
                    const progress = Math.min(elapsed / duration, 1);
                    // Ease out cubic
                    const eased = 1 - Math.pow(1 - progress, 3);
                    const current = eased * num;
                    el.textContent = (isFloat ? current.toFixed(decimals) : Math.round(current)) + suffix;
                    if (progress < 1) requestAnimationFrame(tick);
                }
                requestAnimationFrame(tick);
            });
        }
        const observer = new MutationObserver(apply);
        observer.observe(document.body, { childList: true, subtree: true });
        setTimeout(apply, 300);
    }

    /* ────────── 8. CONFETTI BURST ────────── */
    window.evConfetti = function () {
        const colors = ['#7F5AF0', '#2CB67D', '#FF8906', '#E53170', '#FFD700'];
        const container = document.createElement('div');
        Object.assign(container.style, {
            position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
            pointerEvents: 'none', zIndex: 99999, overflow: 'hidden'
        });
        document.body.appendChild(container);

        for (let i = 0; i < 80; i++) {
            const piece = document.createElement('div');
            const size = Math.random() * 8 + 4;
            const color = colors[Math.floor(Math.random() * colors.length)];
            const startX = 40 + Math.random() * 20; // center-ish
            Object.assign(piece.style, {
                position: 'absolute',
                left: startX + '%',
                top: '-10px',
                width: size + 'px',
                height: size * (Math.random() > 0.5 ? 1 : 0.6) + 'px',
                backgroundColor: color,
                borderRadius: Math.random() > 0.5 ? '50%' : '2px',
                opacity: 1,
                transform: `rotate(${Math.random() * 360}deg)`
            });
            container.appendChild(piece);

            const angle = Math.random() * Math.PI * 2;
            const velocity = 3 + Math.random() * 5;
            let vx = Math.cos(angle) * velocity;
            let vy = -Math.abs(Math.sin(angle) * velocity) - 2;
            const gravity = 0.12;
            let opacity = 1;
            let rotation = Math.random() * 360;
            const rotSpeed = (Math.random() - 0.5) * 15;
            let x = parseFloat(piece.style.left);
            let y = -10;

            function animate() {
                vy += gravity;
                x += vx;
                y += vy;
                rotation += rotSpeed;
                opacity -= 0.008;
                piece.style.left = x + '%';
                piece.style.top = y + 'px';
                piece.style.transform = `rotate(${rotation}deg)`;
                piece.style.opacity = opacity;
                if (opacity > 0 && y < window.innerHeight + 50) {
                    requestAnimationFrame(animate);
                } else {
                    piece.remove();
                }
            }
            setTimeout(() => requestAnimationFrame(animate), Math.random() * 200);
        }
        setTimeout(() => container.remove(), 5000);
    };

    /* ────────── 9. WELCOME ANIMATION ────────── */
    window.evWelcome = function (name) {
        const overlay = document.createElement('div');
        overlay.id = 'ev-welcome-overlay';
        Object.assign(overlay.style, {
            position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
            zIndex: 100000, display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexDirection: 'column',
            background: 'radial-gradient(ellipse at center, rgba(22,22,26,0.97) 0%, rgba(22,22,26,1) 100%)',
            opacity: 0, transition: 'opacity 0.5s ease'
        });
        overlay.innerHTML = `
      <div style="text-align:center;">
        <div style="font-size:3rem; font-weight:800; font-family:'Inter',sans-serif;
          background: linear-gradient(135deg, #7F5AF0, #2CB67D, #FF8906);
          -webkit-background-clip:text; -webkit-text-fill-color:transparent;
          animation: ev-welcome-scale 1s ease-out forwards;
          opacity:0; transform:scale(0.5);">
          Welcome back, ${name} ✨
        </div>
        <div style="font-size:1.1rem; color:rgba(255,255,255,0.5); margin-top:12px;
          font-family:'Outfit',sans-serif; opacity:0; animation: ev-welcome-fade 0.8s 0.6s ease-out forwards;">
          Let's build something amazing
        </div>
      </div>
    `;
        document.body.appendChild(overlay);
        requestAnimationFrame(() => { overlay.style.opacity = 1; });

        setTimeout(() => {
            overlay.style.opacity = 0;
            setTimeout(() => overlay.remove(), 600);
        }, 2200);
    };

    /* ────────── INITIALIZE ALL ────────── */
    function boot() {
        initParticles();
        initCursorGlow();
        initScrollProgress();
        initTiltCards();
        initMagneticButtons();
        initTypewriter();
        initCounters();
    }

    // Streamlit may not have fully rendered yet
    if (document.readyState === 'complete') {
        boot();
    } else {
        window.addEventListener('load', boot);
    }
})();
