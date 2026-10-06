(function () {
    const btn = document.getElementById('hamburgerBtn');
    const nav = document.getElementById('navbarMain');
    if (!btn || !nav) return;

    btn.addEventListener('click', function () {
        const isOpen = nav.classList.toggle('is-open');
        btn.classList.toggle('is-active', isOpen);
        btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    nav.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () {
            if (window.innerWidth <= 1024) {
                nav.classList.remove('is-open');
                btn.classList.remove('is-active');
                btn.setAttribute('aria-expanded', 'false');
            }
        });
    });
})();