const profiles = {
  eli: {title: 'Eli', status: 'Cercana · conectada', symbol: '✦'},
  aurora: {title: 'Aurora', status: 'Creativa · conectada', symbol: 'A'},
  grupo: {title: 'Grupo', status: 'Eli y Aurora · conectadas', symbol: 'E+A'}
};

const welcomes = {
  eli: [{author: 'Eli', text: '¡Hola! Estoy aquí contigo. ¿Qué te gustaría crear, explorar o conversar hoy?'}],
  aurora: [{author: 'Aurora', text: '¡Hola! Estoy lista para imaginar, crear y ayudarte. ¿Qué te gustaría explorar hoy?'}],
  grupo: [
    {author: 'Eli', text: 'Estamos aquí contigo. ¿En qué te gustaría que pensemos juntas?'},
    {author: 'Aurora', text: 'Podemos combinar ideas, creatividad y distintas perspectivas ✨'}
  ]
};

let active = 'eli';
let busy = false;
let pendingAttachments = [];
let selectedChats = {eli: '', aurora: '', grupo: ''};

const $ = selector => document.querySelector(selector);
const messages = $('#messages');
const input = $('#message-input');
const send = $('#send');
const typing = $('#typing');
const attachButton = $('#attach-button');
const fileInput = $('#file-input');
const attachmentPreview = $('#attachment-preview');
const allowedImageTypes = new Set(['image/jpeg', 'image/png', 'image/webp', 'text/plain']);
const maxImageBytes = 8 * 1024 * 1024;
const maxTextBytes = 2 * 1024 * 1024;
const maxAttachments = 4;

const escapeHtml = value => String(value).replace(/[&<>'"]/g, character => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
}[character]));

function applyTheme(theme) {
  const dark = theme === 'dark';
  document.body.classList.toggle('dark', dark);
  $('#theme-icon').textContent = dark ? '☀' : '☾';
  $('#theme-label').textContent = dark ? 'Modo claro' : 'Modo oscuro';
  $('#theme-toggle').setAttribute('aria-pressed', String(dark));
  localStorage.setItem('elizyum-theme', theme);
}

function time() {
  return new Date().toLocaleTimeString('es', {hour: '2-digit', minute: '2-digit'});
}

function showToast(label = 'Mensaje copiado') {
  let toast = $('#copy-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'copy-toast';
    toast.className = 'copy-toast';
    document.body.appendChild(toast);
  }
  toast.textContent = `✓ ${label}`;
  toast.classList.add('visible');
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove('visible'), 1900);
}

async function copyText(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      const area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      const copied = document.execCommand('copy');
      area.remove();
      if (!copied) throw new Error('No se pudo copiar');
    }
    showToast();
  } catch (error) {
    showToast('No se pudo copiar');
  }
}

function attachmentSource(attachment) {
  return attachment.url || attachment.data_url || '';
}

function addMessage(author, text, attachments = []) {
  const key = author.toLowerCase();
  const isUser = key === 'tú' || key === 'usuario';
  const who = isUser ? 'user' : key.includes('aurora') ? 'aurora' : 'eli';
  const row = document.createElement('article');
  row.className = `message-row ${who}`;
  const avatar = isUser ? '' : `<div class="bubble-avatar ${who}-avatar">${who === 'aurora' ? 'A' : '✦'}</div>`;
  const validAttachments = Array.isArray(attachments) ? attachments.filter(attachmentSource) : [];
  const attachmentMarkup = validAttachments.length ? `
    <div class="message-attachments">
      ${validAttachments.map(attachment => attachment.type === 'text'
        ? `<a class="message-file" href="${escapeHtml(attachmentSource(attachment))}" target="_blank" title="Abrir archivo"><span>TXT</span><strong>${escapeHtml(attachment.name || 'Archivo.txt')}</strong></a>`
        : `<img class="message-attachment" src="${escapeHtml(attachmentSource(attachment))}" alt="${escapeHtml(attachment.name || 'Imagen adjunta')}" title="Abrir imagen">`).join('')}
    </div>` : '';
  const visibleText = String(text || '');

  row.innerHTML = `${avatar}<div class="bubble">
    <span class="author">${escapeHtml(author)}</span>
    ${attachmentMarkup}
    ${visibleText ? `<div class="message-content">${escapeHtml(visibleText).replace(/\n/g, '<br>')}</div>` : ''}
    <div class="message-meta">
      <button class="copy-message" type="button" title="Copiar mensaje" aria-label="Copiar mensaje">⧉ <span>Copiar</span></button>
      <span class="time">${time()}</span>
    </div>
  </div>`;

  row.querySelector('.copy-message').addEventListener('click', () => copyText(visibleText));
  row.querySelectorAll('.message-attachment').forEach(image => {
    image.addEventListener('click', () => window.open(image.src, '_blank'));
  });
  messages.appendChild(row);
  messages.scrollTop = messages.scrollHeight;
}

function setBusy(value) {
  busy = value;
  send.disabled = value;
  attachButton.disabled = value;
  typing.classList.toggle('hidden', !value);
  if (value) {
    typing.className = 'typing';
    $('#typing-avatar').className = `bubble-avatar ${active === 'aurora' ? 'aurora' : 'eli'}-avatar`;
    messages.scrollTop = messages.scrollHeight;
  }
}

function renderAttachmentPreview() {
  attachmentPreview.innerHTML = '';
  attachmentPreview.classList.toggle('hidden', pendingAttachments.length === 0);

  pendingAttachments.forEach((attachment, index) => {
    const card = document.createElement('div');
    card.className = 'attachment-card';
    const visual = attachment.type === 'text'
      ? '<div class="attachment-document">TXT</div>'
      : `<img src="${escapeHtml(attachment.data_url)}" alt="">`;
    card.innerHTML = `${visual}<span class="attachment-name">${escapeHtml(attachment.name)}</span><button class="remove-attachment" type="button" aria-label="Quitar ${escapeHtml(attachment.name)}">×</button>`;
    card.querySelector('.remove-attachment').addEventListener('click', () => {
      pendingAttachments.splice(index, 1);
      renderAttachmentPreview();
    });
    attachmentPreview.appendChild(card);
  });
}

function clearAttachments() {
  pendingAttachments = [];
  fileInput.value = '';
  renderAttachmentPreview();
}

function readFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(new Error(`No se pudo leer ${file.name}`));
    reader.readAsDataURL(file);
  });
}

async function selectImages(files) {
  const available = maxAttachments - pendingAttachments.length;
  if (available <= 0) {
    showToast('Máximo 4 imágenes');
    return;
  }

  for (const file of Array.from(files).slice(0, available)) {
    const fileType = file.type || (file.name.toLowerCase().endsWith('.txt') ? 'text/plain' : '');
    if (!allowedImageTypes.has(fileType)) {
      showToast('Solo JPG, PNG, WebP o TXT');
      continue;
    }
    const maxBytes = fileType === 'text/plain' ? maxTextBytes : maxImageBytes;
    if (file.size > maxBytes) {
      showToast(`${file.name} supera ${fileType === 'text/plain' ? '2' : '8'} MB`);
      continue;
    }
    try {
      pendingAttachments.push({
        name: file.name,
        type: fileType,
        size: file.size,
        data_url: await readFileAsDataUrl(file)
      });
    } catch (error) {
      showToast(error.message);
    }
  }

  if (files.length > available) showToast('Solo se añadieron 4 imágenes');
  renderAttachmentPreview();
}

function showWelcome() {
  welcomes[active].forEach(item => addMessage(item.author, item.text));
}

function renderHistoryMessages(history) {
  messages.innerHTML = '';
  if (!history.length) {
    showWelcome();
    return;
  }
  history.forEach(message => {
    if (message.role === 'user') addMessage('Tú', message.content, message.attachments);
    else if (message.role === 'assistant') addMessage((message.member || active).replace(/^./, character => character.toUpperCase()), message.content, message.attachments);
  });
}

async function loadConversationList() {
  const list = $('#history-list');
  list.innerHTML = '';
  try {
    const items = await window.pywebview.api.listar_conversaciones(active);
    items.forEach(item => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'history-item';
      button.classList.toggle('selected', selectedChats[active] === item.id);
      button.textContent = item.titulo;
      button.title = item.titulo;
      button.addEventListener('click', async () => {
        if (busy) return;
        clearAttachments();
        const history = await window.pywebview.api.cargar_conversacion(active, item.id);
        selectedChats[active] = item.id;
        await window.pywebview.api.guardar_estado_ui(active, item.id);
        renderHistoryMessages(history);
        document.querySelectorAll('.history-item').forEach(element => element.classList.remove('selected'));
        button.classList.add('selected');
      });
      list.appendChild(button);
    });
    if (!items.length) list.innerHTML = '<p class="history-empty">Aún no hay conversaciones</p>';
  } catch (error) {
    list.innerHTML = '<p class="history-empty">No se pudo cargar</p>';
  }
}

async function loadHistory() {
  try {
    renderHistoryMessages(await window.pywebview.api.obtener_historial(active));
  } catch (error) {
    messages.innerHTML = '';
    showWelcome();
    addMessage('Elizyum', `No pude cargar el historial: ${error}`);
  }
}

function updateProfile() {
  const profile = profiles[active];
  $('#chat-title').textContent = profile.title;
  $('#chat-status').innerHTML = `<span class="status-dot"></span>${profile.status}`;
  const avatar = $('#header-avatar');
  avatar.textContent = profile.symbol;
  avatar.className = `header-avatar ${active === 'grupo' ? 'group' : active}-avatar`;
  document.querySelectorAll('.character').forEach(button => button.classList.toggle('active', button.dataset.chat === active));
  send.style.background = active === 'eli' ? 'var(--eli)' : active === 'aurora' ? 'var(--aurora)' : 'var(--blue)';
}

document.querySelectorAll('.character').forEach(button => button.addEventListener('click', async () => {
  if (busy) return;
  clearAttachments();
  active = button.dataset.chat;
  updateProfile();
  if (selectedChats[active]) await window.pywebview.api.cargar_conversacion(active, selectedChats[active]);
  await window.pywebview.api.guardar_estado_ui(active, selectedChats[active]);
  await loadHistory();
  await loadConversationList();
  input.focus();
}));

attachButton.addEventListener('click', () => {
  if (!busy) fileInput.click();
});

fileInput.addEventListener('change', async event => {
  await selectImages(event.target.files);
  fileInput.value = '';
});

$('#composer').addEventListener('submit', async event => {
  event.preventDefault();
  const text = input.value.trim();
  if ((!text && !pendingAttachments.length) || busy) return;

  const attachments = pendingAttachments.map(item => ({...item}));
  input.value = '';
  clearAttachments();
  addMessage('Tú', text || 'Imagen adjunta', attachments);
  setBusy(true);

  try {
    const responses = await window.pywebview.api.enviar_mensaje(active, text, attachments);
    responses.forEach(response => addMessage(response.autor, response.mensaje));
    selectedChats[active] = await window.pywebview.api.obtener_conversacion_actual(active);
    await window.pywebview.api.guardar_estado_ui(active, selectedChats[active]);
    await loadConversationList();
  } catch (error) {
    addMessage('Elizyum', `No pude completar la respuesta.\n\n${error}`);
  } finally {
    setBusy(false);
    input.focus();
  }
});

input.addEventListener('keydown', event => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    $('#composer').requestSubmit();
  }
});

$('#new-chat').addEventListener('click', () => {
  $('#modal-text').textContent = `¿Quieres comenzar una nueva conversación con ${profiles[active].title}?`;
  $('#modal').classList.remove('hidden');
});
$('#cancel').addEventListener('click', () => $('#modal').classList.add('hidden'));
$('#theme-toggle').addEventListener('click', () => applyTheme(document.body.classList.contains('dark') ? 'light' : 'dark'));
$('#confirm').addEventListener('click', async () => {
  await window.pywebview.api.nueva_conversacion(active);
  selectedChats[active] = '';
  await window.pywebview.api.guardar_estado_ui(active, '');
  $('#modal').classList.add('hidden');
  clearAttachments();
  messages.innerHTML = '';
  showWelcome();
  await loadConversationList();
  input.focus();
});

applyTheme(localStorage.getItem('elizyum-theme') || 'light');
window.addEventListener('pywebviewready', async () => {
  const state = await window.pywebview.api.obtener_estado_ui();
  selectedChats = {...selectedChats, ...state.seleccionadas};
  active = profiles[state.chat_activo] ? state.chat_activo : 'eli';
  if (selectedChats[active]) {
    try {
      await window.pywebview.api.cargar_conversacion(active, selectedChats[active]);
    } catch (error) {
      selectedChats[active] = '';
    }
  }
  updateProfile();
  await loadHistory();
  await loadConversationList();
  input.focus();
});
