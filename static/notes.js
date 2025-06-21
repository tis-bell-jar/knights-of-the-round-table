 document.addEventListener('DOMContentLoaded', () => {
  const container    = document.querySelector('#sticky-container');
  const unitId       = +container.dataset.unit;
  const filterBtn    = document.getElementById('filter-toggle');
  const storedFilter = localStorage.getItem('blueFilter') === 'on';

  // Global blue‐light filter
  function setFilter(on) {
    document.body.classList.toggle('blue-filter', on);
    filterBtn.textContent = on ? '☀️ Normal' : '🕶️ Filter';
    localStorage.setItem('blueFilter', on ? 'on' : 'off');
  }
  setFilter(storedFilter);
  filterBtn.addEventListener('click', () =>
    setFilter(!document.body.classList.contains('blue-filter'))
  );

  function api(id, method, data) {
    const url  = id ? `/api/notes/${id}` : '/api/notes';
    const full = method === 'GET'
      ? `${url}?unit=${unitId}` : url;
    return fetch(full, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: data ? JSON.stringify(data) : undefined
    }).then(r => {
      if (!r.ok && r.status !== 204) throw new Error(r.statusText);
      return r.status === 204 ? null : r.json();
    });
  }

  function renderNote(n) {
    const el = document.createElement('div');
    const modeClass = n.is_dark ? 'dark-note' : 'light-note';
    el.className = `note ${modeClass}`;
    el.style.setProperty('--c', n.bg_color);
    el.style.left   = n.x + 'px';
    el.style.top    = n.y + 'px';
    el.style.width  = n.width + 'px';
    el.style.height = n.height + 'px';
    if (n.collapsed) el.classList.add('collapsed');
    el.dataset.id = n.id;

    el.innerHTML = `
      <div class="logo-overlay"></div>
      <div class="note-accent"></div>
      <div class="note-header">
        <input class="unit-input" placeholder="Unit" value="${n.title||''}">
        <input type="color" class="color-picker" value="${n.bg_color}">
        <button class="add-sibling">＋</button>
        <button class="mode-toggle">${n.is_dark ? '☀️' : '🌙'}</button>
        <button class="close-btn">${n.collapsed ? '▢' : '▣'}</button>
        <button class="delete-btn">✕</button>
      </div>
      <div class="note-body"><textarea>${n.content}</textarea></div>
      <div class="note-footer">
        <span class="timestamp">${new Date(n.updated_at).toLocaleTimeString()}</span>
      </div>
    `;
    container.appendChild(el);

    const inp       = el.querySelector('.unit-input');
    const cpicker   = el.querySelector('.color-picker');
    const addBtn    = el.querySelector('.add-sibling');
    const modeBtn   = el.querySelector('.mode-toggle');
    const closeBtn  = el.querySelector('.close-btn');
    const delBtn    = el.querySelector('.delete-btn');
    const ta        = el.querySelector('textarea');
    const ts        = el.querySelector('.timestamp');
    const logo      = el.querySelector('.logo-overlay');

    // Save title
    inp.addEventListener('blur', () =>
      api(n.id, 'PUT', { title: inp.value })
    );

    // Update color bands
    cpicker.addEventListener('input', e => {
      n.bg_color = e.target.value;
      el.style.setProperty('--c', n.bg_color);
      api(n.id, 'PUT', { bg_color: n.bg_color });
    });

    // Twin-note
    addBtn.onclick = () =>
      api(null, 'POST', {
        unit_id: unitId,
        x: n.x + 30, y: n.y + 30,
        bg_color: n.bg_color,
        title: ''
      }).then(renderNote);

    // Per-note dark/light
    modeBtn.onclick = () => {
      n.is_dark = !n.is_dark;
      el.classList.toggle('dark-note', n.is_dark);
      el.classList.toggle('light-note', !n.is_dark);
      modeBtn.textContent = n.is_dark ? '☀️' : '🌙';
      api(n.id, 'PUT', { is_dark: n.is_dark });
    };

    // Collapse/expand & logo overlay
    closeBtn.onclick = () => {
      n.collapsed = !n.collapsed;
      el.classList.toggle('collapsed', n.collapsed);
      closeBtn.textContent = n.collapsed ? '▢' : '▣';
      logo.style.opacity = n.collapsed ? 0.5 : 0;
      api(n.id, 'PUT', { collapsed: n.collapsed });
    };

    // Delete
    delBtn.onclick = () =>
      api(n.id, 'DELETE').then(() => el.remove());

    // Markdown + autosave
    const mde = new SimpleMDE({
      element: ta,
      initialValue: n.content,
      toolbar: false,
      status: false,
      spellChecker: false
    });
    let timer;
    mde.codemirror.on('change', () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        api(n.id, 'PUT', { content: mde.value() })
          .then(u => ts.textContent = new Date(u.updated_at).toLocaleTimeString());
      }, 500);
    });

    // Drag & resize
    interact(el)
      .draggable({
        onmove(e) {
          n.x += e.dx; n.y += e.dy;
          el.style.left = n.x + 'px'; el.style.top = n.y + 'px';
        },
        onend: () => api(n.id, 'PUT', { x: n.x, y: n.y })
      })
      .resizable({
        edges: { left: true, right: true, bottom: true, top: true },
        onmove(e) {
          n.width = e.rect.width; n.height = e.rect.height;
          el.style.width = n.width + 'px';
          el.style.height = n.height + 'px';
        },
        onend: () => api(n.id, 'PUT', { width: n.width, height: n.height })
      });
  }

  // Load & render
  api(null, 'GET').then(notes => notes.forEach(renderNote));

  // Add note
  document.getElementById('add-note-btn').onclick = () =>
    api(null, 'POST', { unit_id: unitId }).then(renderNote);
});


