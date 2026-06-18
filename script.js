const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebarNav = document.getElementById('sidebarNav');
const searchInput = document.getElementById('searchInput');
const scrollTop = document.getElementById('scrollTop');
const navItems = sidebarNav.querySelectorAll('.nav-item');
const sections = document.querySelectorAll('.manual-section[id]');

sidebarToggle.addEventListener('click', () => {
  sidebar.classList.toggle('open');
});

navItems.forEach(item => {
  item.addEventListener('click', () => sidebar.classList.remove('open'));
});

document.addEventListener('click', e => {
  if (sidebar.classList.contains('open') &&
      !sidebar.contains(e.target) &&
      e.target !== sidebarToggle) {
    sidebar.classList.remove('open');
  }
});

const observer = new IntersectionObserver(
  entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navItems.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
        });
      }
    });
  },
  { rootMargin: '-30% 0px -60% 0px' }
);

sections.forEach(section => observer.observe(section));

window.addEventListener('scroll', () => {
  scrollTop.classList.toggle('visible', window.scrollY > 400);
});

scrollTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightboxImg');
const lightboxCaption = document.getElementById('lightboxCaption');
const lightboxClose = document.getElementById('lightboxClose');

function openLightbox(src, caption) {
  lightboxImg.src = src;
  lightboxImg.alt = caption;
  lightboxCaption.textContent = caption;
  lightbox.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  lightbox.classList.remove('open');
  document.body.style.overflow = '';
  lightboxImg.src = '';
}

document.querySelectorAll('.screenshot-trigger').forEach(btn => {
  btn.addEventListener('click', () => {
    openLightbox(btn.dataset.src, btn.dataset.caption);
  });
});

lightboxClose.addEventListener('click', closeLightbox);
lightbox.addEventListener('click', e => {
  if (e.target === lightbox) closeLightbox();
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeLightbox();
});

searchInput.addEventListener('input', () => {
  const query = searchInput.value.trim().toLowerCase();
  if (!query) {
    navItems.forEach(item => item.classList.remove('hidden'));
    sections.forEach(section => section.classList.remove('search-hidden'));
    return;
  }

  const matchedIds = new Set();

  sections.forEach(section => {
    const keywords = (section.dataset.keywords || '').toLowerCase();
    const text = section.textContent.toLowerCase();
    const match = keywords.includes(query) || text.includes(query);
    section.classList.toggle('search-hidden', !match);
    if (match) matchedIds.add(section.id);
  });

  navItems.forEach(item => {
    const href = item.getAttribute('href').slice(1);
    if (href === 'intro') {
      item.classList.toggle('hidden', !('시작하기'.includes(query) || 'intro'.includes(query) || matchedIds.has('intro')));
    } else {
      item.classList.toggle('hidden', !matchedIds.has(href));
    }
  });
});
