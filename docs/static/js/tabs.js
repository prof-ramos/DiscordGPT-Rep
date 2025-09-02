document.addEventListener('DOMContentLoaded', () => {
  const allTabs = document.querySelectorAll('.tabs');
  allTabs.forEach((container, containerIndex) => {
    const containerId = container.getAttribute('data-tabs-id') || `tabs-${Date.now()}-${containerIndex}`;

    // Build from simple tab blocks
    const tabs = Array.from(container.querySelectorAll(':scope > .tab'));
    const nav = document.createElement('div');
    nav.className = 'tabs-nav';
    nav.setAttribute('role', 'tablist');
    const content = document.createElement('div');
    content.className = 'tabs-content';

    const buttons = [];
    const panels = [];

    tabs.forEach((tabEl, idx) => {
      const title = tabEl.getAttribute('data-title') || `Tab ${idx + 1}`;
      const tabId = `${containerId}-tab-${idx}`;
      const panelId = `${containerId}-panel-${idx}`;

      const btn = document.createElement('button');
      btn.className = 'tab-link' + (idx === 0 ? ' is-active' : '');
      btn.type = 'button';
      btn.id = tabId;
      btn.setAttribute('role', 'tab');
      btn.setAttribute('aria-controls', panelId);
      btn.setAttribute('tabindex', idx === 0 ? '0' : '-1');
      btn.setAttribute('aria-selected', idx === 0 ? 'true' : 'false');
      btn.textContent = title;

      const panel = document.createElement('div');
      panel.className = 'tab-panel' + (idx === 0 ? ' is-active' : '');
      panel.id = panelId;
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tabId);
      if (idx !== 0) panel.setAttribute('hidden', '');
      panel.innerHTML = tabEl.querySelector(':scope > .tab-content')?.innerHTML || tabEl.innerHTML;

      // Click to activate
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        activate(idx);
        btn.focus();
      });

      nav.appendChild(btn);
      content.appendChild(panel);
      buttons.push(btn);
      panels.push(panel);
      tabEl.remove();
    });

    const activate = (index) => {
      buttons.forEach((b, i) => {
        const active = i === index;
        b.classList.toggle('is-active', active);
        b.setAttribute('aria-selected', active ? 'true' : 'false');
        b.setAttribute('tabindex', active ? '0' : '-1');
      });
      panels.forEach((p, i) => {
        const active = i === index;
        p.classList.toggle('is-active', active);
        if (active) {
          p.removeAttribute('hidden');
        } else {
          p.setAttribute('hidden', '');
        }
      });
    };

    // Keyboard navigation: Left/Right/Home/End, Enter/Space
    nav.addEventListener('keydown', (e) => {
      const currentIndex = buttons.findIndex((b) => b === document.activeElement);
      if (currentIndex === -1) return;
      let nextIndex = null;
      switch (e.key) {
        case 'ArrowRight':
          nextIndex = (currentIndex + 1) % buttons.length;
          break;
        case 'ArrowLeft':
          nextIndex = (currentIndex - 1 + buttons.length) % buttons.length;
          break;
        case 'Home':
          nextIndex = 0;
          break;
        case 'End':
          nextIndex = buttons.length - 1;
          break;
        case 'Enter':
        case ' ': // Space
          activate(currentIndex);
          e.preventDefault();
          return;
        default:
          return;
      }
      if (nextIndex !== null) {
        buttons[nextIndex].focus();
        activate(nextIndex);
        e.preventDefault();
      }
    });

    // Mount
    container.prepend(nav);
    container.appendChild(content);
  });
});
