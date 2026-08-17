(function () {
  const MCP_PREFIX = '/mcp';
  const DEFAULT_MODEL = 'qwen2.5-coder:3b';

  const DEFAULT_CONN_SCAN_BODY = {
    connections: [
      { src_ip: '10.0.0.5', dst_ip: '8.8.8.8', dst_port: 443, proto: 'tcp' },
      { src_ip: '10.0.0.12', dst_ip: '203.0.113.9', dst_port: 4444, proto: 'tcp' },
      {
        src_ip: '192.168.1.3',
        dst_ip: '45.33.32.156',
        dst_port: 80,
        payload_sample: 'GET /cgi-bin/../../etc/passwd HTTP/1.1'
      },
      {
        dst_port: 443,
        proto: 'tcp',
        user_agent: 'curl/8.0',
        risk_score: 0.2
      }
    ],
    progress_every: 1
  };

  let connScanAbortController = null;

  let baseUrlEl;
  let outputEl;
  let imageOutputEl;
  let outputPanelEl;
  let statusLineEl;
  let requestStatusBadgeEl;
  let modelSelectEl;
  let rawModelHintEl;

  const STATUS_TITLES = {
    idle: 'Idle',
    loading: 'Loading',
    completed: 'Completed',
    failed: 'Failed'
  };

  function setRequestState(state, message) {
    if (!statusLineEl || !requestStatusBadgeEl) return;
    const titleBase = STATUS_TITLES[state] || state;
    requestStatusBadgeEl.className = 'status-badge status-badge--' + state;
    requestStatusBadgeEl.title = message ? titleBase + ' — ' + message : titleBase;
    statusLineEl.textContent = message || '';
    if (state === 'completed') statusLineEl.className = 'status-line status-ok';
    else if (state === 'failed') statusLineEl.className = 'status-line status-err';
    else if (state === 'loading') statusLineEl.className = 'status-line status-loading';
    else statusLineEl.className = 'status-line';
    if (outputPanelEl) {
      outputPanelEl.classList.toggle('request-busy', state === 'loading');
      outputPanelEl.setAttribute('aria-busy', state === 'loading' ? 'true' : 'false');
    }
  }

  function baseUrl() {
    if (!baseUrlEl) return window.location.origin;
    const custom = (baseUrlEl.value || '').trim().replace(/\/+$/, '');
    return custom || window.location.origin;
  }

  function setOutput(text, isJson) {
    if (!outputEl || !imageOutputEl) return;
    imageOutputEl.hidden = true;
    imageOutputEl.innerHTML = '';
    outputEl.hidden = false;
    outputEl.innerHTML = '';
    const span = document.createElement('span');
    if (text == null || text === '') {
      span.textContent = '(empty)';
      span.className = 'muted';
    } else if (isJson) {
      try {
        const parsed = JSON.parse(text);
        span.textContent = JSON.stringify(parsed, null, 2);
      } catch {
        span.textContent = text;
      }
    } else {
      span.textContent = text;
    }
    outputEl.appendChild(span);
  }

  function setImageOutput(blob) {
    if (!outputEl || !imageOutputEl) return;
    outputEl.hidden = true;
    imageOutputEl.hidden = false;
    imageOutputEl.innerHTML = '';
    const img = document.createElement('img');
    img.src = URL.createObjectURL(blob);
    img.alt = 'Response image';
    imageOutputEl.appendChild(img);
  }

  async function request(method, path, body) {
    const url = baseUrl() + path;
    const opts = { method };
    if (body && (method === 'POST' || method === 'PUT')) {
      opts.headers = { 'Content-Type': 'application/json' };
      opts.body = typeof body === 'string' ? body : JSON.stringify(body);
    }
    setRequestState('loading', `${method} ${path}…`);
    let res;
    try {
      res = await fetch(url, opts);
    } catch (e) {
      console.error('control: fetch failed', path, e);
      setRequestState('failed', `Network error · ${path} — ${e.message || e}`);
      setOutput(String(e), false);
      return { ok: false, error: e };
    }
    const contentType = res.headers.get('content-type') || '';
    const summary = `${res.status} ${res.statusText} · ${path}`;
    if (res.ok) setRequestState('completed', summary);
    else setRequestState('failed', summary);
    if (contentType.includes('application/json')) {
      const text = await res.text();
      setOutput(text, true);
      return { ok: res.ok, json: text };
    }
    if (contentType.includes('image/')) {
      const blob = await res.blob();
      setImageOutput(blob);
      return { ok: res.ok };
    }
    const text = await res.text();
    setOutput(text, false);
    return { ok: res.ok, text };
  }

  function getSelectedModel() {
    const v = modelSelectEl && modelSelectEl.value ? modelSelectEl.value.trim() : '';
    return v || DEFAULT_MODEL;
  }

  function updateRawModelHint() {
    if (!rawModelHintEl) return;
    const m = getSelectedModel();
    rawModelHintEl.textContent =
      `Use "${m}" in JSON: {"name": "${m}"} for /api/show, {"model": "${m}", "prompt": "…"} for /api/generate, {"model": "${m}", "messages": [{"role":"user","content":"…"}], "stream": false} for ${MCP_PREFIX}/api/chat`;
  }

  async function fetchTagsAndPopulateDropdown(showFullOutput) {
    const url = baseUrl() + '/api/tags';
    setRequestState('loading', 'GET /api/tags …');

    let res;
    try {
      res = await fetch(url, { method: 'GET', cache: 'no-store' });
    } catch (e) {
      console.error('control: /api/tags fetch failed', e);
      setRequestState('failed', `Network error · /api/tags — ${e.message || e}`);
      if (modelSelectEl) {
        modelSelectEl.innerHTML = '';
        modelSelectEl.appendChild(new Option('(network error)', ''));
      }
      if (showFullOutput) setOutput(String(e), false);
      updateRawModelHint();
      return;
    }

    const text = await res.text();
    const contentType = res.headers.get('content-type') || '';
    if (!res.ok) {
      setRequestState('failed', `${res.status} ${res.statusText} · /api/tags`);
      if (modelSelectEl) {
        modelSelectEl.innerHTML = '';
        modelSelectEl.appendChild(new Option(`(HTTP ${res.status})`, ''));
      }
      if (showFullOutput) setOutput(text, contentType.includes('application/json'));
      updateRawModelHint();
      return;
    }

    let names = [];
    try {
      const data = JSON.parse(text);
      const models = data.models || [];
      names = models
        .map((m) => (m && (m.name || m.model)) || '')
        .filter(Boolean);
    } catch (e) {
      console.error('control: /api/tags JSON parse failed', e);
      setRequestState('failed', 'Invalid JSON from /api/tags');
      if (modelSelectEl) {
        modelSelectEl.innerHTML = '';
        modelSelectEl.appendChild(new Option('(bad JSON)', ''));
      }
      if (showFullOutput) setOutput(text, false);
      updateRawModelHint();
      return;
    }

    const prev = modelSelectEl ? modelSelectEl.value : '';
    if (modelSelectEl) {
      modelSelectEl.innerHTML = '';
      if (names.length === 0) {
        modelSelectEl.appendChild(new Option('(no models — pull in Ollama)', ''));
      } else {
        names.forEach((name) => modelSelectEl.appendChild(new Option(name, name)));
        if (prev && names.includes(prev)) modelSelectEl.value = prev;
        else modelSelectEl.selectedIndex = 0;
      }
    }
    setRequestState('completed', `${res.status} · ${names.length} model(s) · /api/tags`);
    if (showFullOutput) setOutput(text, true);
    updateRawModelHint();
  }

  function boot() {
    baseUrlEl = document.getElementById('baseUrl');
    outputEl = document.getElementById('output');
    imageOutputEl = document.getElementById('imageOutput');
    outputPanelEl = document.querySelector('.output-panel');
    statusLineEl = document.getElementById('statusLine');
    requestStatusBadgeEl = document.getElementById('requestStatusBadge');
    modelSelectEl = document.getElementById('modelSelect');
    rawModelHintEl = document.getElementById('rawModelHint');

    setRequestState('idle', 'Ready');

    if (!modelSelectEl) {
      console.error('control: #modelSelect missing');
    }

    const byId = (id) => document.getElementById(id);
    const on = (id, ev, fn) => {
      const el = byId(id);
      if (el) el.addEventListener(ev, fn);
      else console.warn('control: missing #' + id);
    };

    on('ollamaTags', 'click', async () => {
      await fetchTagsAndPopulateDropdown(true);
    });

    on('ollamaShow', 'click', async () => {
      await request('POST', '/api/show', { name: getSelectedModel() });
    });

    on('ollamaGenerate', 'click', async () => {
      const prompt = (byId('genPrompt') && byId('genPrompt').value.trim()) || 'Hello.';
      await request('POST', '/api/generate', {
        model: getSelectedModel(),
        prompt,
        stream: false
      });
    });

    on('mcpHealth', 'click', async () => {
      await request('GET', MCP_PREFIX + '/api/health');
    });

    on('mcpScreenshot', 'click', async () => {
      const path = MCP_PREFIX + '/api/screenshot';
      const url = baseUrl() + path;
      setRequestState('loading', `GET ${path}…`);
      let res;
      try {
        res = await fetch(url);
      } catch (e) {
        setRequestState('failed', `Network error · ${path} — ${e.message || e}`);
        setOutput(String(e), false);
        return;
      }
      const summary = `${res.status} ${res.statusText} · ${path}`;
      if (res.ok) setRequestState('completed', summary);
      else setRequestState('failed', summary);
      if (res.ok && (res.headers.get('content-type') || '').includes('image/')) {
        setImageOutput(await res.blob());
      } else {
        setOutput(await res.text(), false);
      }
    });

    on('mcpDescribe', 'click', async () => {
      await request('GET', MCP_PREFIX + '/api/describe_vision');
    });

    on('mcpYolo', 'click', async () => {
      await request('GET', MCP_PREFIX + '/api/yolo');
    });

    on('mcpYoloImage', 'click', async () => {
      const path = MCP_PREFIX + '/api/yolo_image';
      const url = baseUrl() + path;
      setRequestState('loading', `GET ${path}…`);
      let res;
      try {
        res = await fetch(url);
      } catch (e) {
        setRequestState('failed', `Network error · ${path} — ${e.message || e}`);
        setOutput(String(e), false);
        return;
      }
      const summary = `${res.status} ${res.statusText} · ${path}`;
      if (res.ok) setRequestState('completed', summary);
      else setRequestState('failed', summary);
      if (res.ok && (res.headers.get('content-type') || '').includes('image/')) {
        setImageOutput(await res.blob());
      } else {
        setOutput(await res.text(), false);
      }
    });

    on('mcpChat', 'click', async () => {
      const msgEl = byId('chatMessage');
      const content = (msgEl && msgEl.value.trim()) || 'Hello.';
      await request('POST', MCP_PREFIX + '/api/chat', {
        model: getSelectedModel(),
        messages: [{ role: 'user', content }],
        stream: false
      });
    });

    async function runConnectionScanStream() {
      const ta = byId('connScanPayload');
      if (!ta) return;
      let body;
      try {
        body = JSON.parse(ta.value || '{}');
      } catch (e) {
        setRequestState('failed', 'Invalid JSON in connection scan payload');
        setOutput(String(e), false);
        return;
      }
      if (!Array.isArray(body.connections)) {
        setRequestState('failed', 'Expected { "connections": [ … ] }');
        setOutput('Body must include a "connections" array.', false);
        return;
      }
      if (connScanAbortController) connScanAbortController.abort();
      connScanAbortController = new AbortController();
      const path = MCP_PREFIX + '/api/connection_scan/stream';
      const url = baseUrl() + path;
      setRequestState('loading', 'POST ' + path + ' (stream)…');
      const okEl = byId('connScanOk');
      const badEl = byId('connScanBad');
      const procEl = byId('connScanProcessed');
      const totEl = byId('connScanTotal');
      const engEl = byId('connScanEngine');
      if (okEl) okEl.textContent = '0';
      if (badEl) badEl.textContent = '0';
      if (procEl) procEl.textContent = '0';
      if (totEl) totEl.textContent = '0';
      if (engEl) engEl.textContent = '';
      const events = [];
      try {
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
          signal: connScanAbortController.signal
        });
        const ct = res.headers.get('content-type') || '';
        if (!res.ok) {
          const t = await res.text();
          setRequestState('failed', res.status + ' · ' + path);
          setOutput(t, ct.includes('application/json'));
          connScanAbortController = null;
          return;
        }
        const reader = res.body && res.body.getReader();
        if (!reader) {
          setRequestState('failed', 'No response body');
          connScanAbortController = null;
          return;
        }
        const dec = new TextDecoder();
        let buf = '';
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buf += dec.decode(value, { stream: true });
          const lines = buf.split('\n');
          buf = lines.pop() || '';
          for (let li = 0; li < lines.length; li++) {
            const s = lines[li].trim();
            if (!s) continue;
            let ev;
            try {
              ev = JSON.parse(s);
            } catch {
              continue;
            }
            events.push(ev);
            if (ev.type === 'start') {
              if (totEl) totEl.textContent = String(ev.total != null ? ev.total : '0');
              if (engEl) engEl.textContent = ev.engine ? 'Engine: ' + ev.engine : '';
            }
            if (ev.type === 'progress') {
              if (okEl) okEl.textContent = String(ev.ok);
              if (badEl) badEl.textContent = String(ev.malicious);
              if (procEl) procEl.textContent = String(ev.processed);
            }
            if (ev.type === 'error') {
              setRequestState('failed', ev.message || 'scan error');
              setOutput(JSON.stringify(events, null, 2), true);
              connScanAbortController = null;
              return;
            }
            if (ev.type === 'done') {
              if (okEl) okEl.textContent = String(ev.ok);
              if (badEl) badEl.textContent = String(ev.malicious);
              if (procEl) procEl.textContent = String(ev.total);
              if (totEl) totEl.textContent = String(ev.total);
              if (engEl && ev.engine) engEl.textContent = 'Engine: ' + ev.engine;
            }
          }
        }
        const tail = buf.trim();
        if (tail) {
          try {
            const ev = JSON.parse(tail);
            events.push(ev);
            if (ev.type === 'done') {
              if (okEl) okEl.textContent = String(ev.ok);
              if (badEl) badEl.textContent = String(ev.malicious);
              if (procEl) procEl.textContent = String(ev.total);
              if (totEl) totEl.textContent = String(ev.total);
            }
          } catch (_) {
            /* ignore */
          }
        }
        setRequestState('completed', 'Scan complete · ' + path);
        setOutput(JSON.stringify(events, null, 2), true);
      } catch (e) {
        if (e && e.name === 'AbortError') {
          setRequestState('idle', 'Scan cancelled');
        } else {
          setRequestState('failed', (e && e.message) || String(e));
          setOutput(String(e), false);
        }
      }
      connScanAbortController = null;
    }

    const connPayload = byId('connScanPayload');
    if (connPayload && !connPayload.value.trim()) {
      connPayload.value = JSON.stringify(DEFAULT_CONN_SCAN_BODY, null, 2);
    }

    on('connScanStream', 'click', () => {
      runConnectionScanStream();
    });

    on('rawSend', 'click', async () => {
      const method = byId('rawMethod').value;
      const path = (byId('rawPath').value || '').trim() || '/api/tags';
      const pathNorm = path.startsWith('/') ? path : '/' + path;
      let body = (byId('rawBody').value || '').trim();
      if ((method === 'POST' || method === 'PUT') && body) {
        try {
          JSON.parse(body);
        } catch {
          setRequestState('failed', 'Invalid JSON body');
          setOutput('Body is not valid JSON.', false);
          return;
        }
      } else {
        body = undefined;
      }
      await request(method, pathNorm, body);
    });

    on('copyOutput', 'click', () => {
      if (!outputEl) return;
      const text = outputEl.textContent;
      if (!text || outputEl.querySelector('.muted')) return;
      navigator.clipboard.writeText(text).then(
        () => {
          setRequestState('completed', 'Copied to clipboard');
        },
        () => {
          setRequestState('failed', 'Copy failed');
        }
      );
    });

    if (modelSelectEl) {
      modelSelectEl.addEventListener('change', updateRawModelHint);
    }

    if (baseUrlEl) {
      baseUrlEl.addEventListener('change', () => fetchTagsAndPopulateDropdown(false));
    }

    fetchTagsAndPopulateDropdown(false);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
