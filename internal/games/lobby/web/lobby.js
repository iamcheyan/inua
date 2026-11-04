// The game lobby's page: the tables as the lobby says they are, kept up
// to date over a WebSocket; joining or watching opens the table's game
// page with its code. At a free table a visitor may open a game the lobby
// hosts itself, when it does.

const $ = (id) => document.getElementById(id);
let T = {
  title: 'Game Lobby', table: 'TABLE %d', free: 'Free', freeNote: 'A host can open a game here.',
  subOpen: 'Join a game at a table, watch one, or open one at a free table. A host can also open a game here from Small Fortune or Chinese Checkers in inua.',
  freeOpen: 'Open a game here for others to join.', failed: 'The game could not open: %s',
  away: 'The host’s connection dropped: waiting for it to come back…', reconnecting: 'Reconnecting…', lobby: 'Waiting to start',
  room: 'Open seats: %d', playing: 'Playing', over: 'Over', join: 'Join', watch: 'Watch',
  leads: '%s sets up the game', open: 'Open seat', local: 'at the host’s screen', visitor: 'in a browser',
  computer: 'computer', ai: 'AI', reconnect: 'Connection lost: trying again…',
  games: { 'small-fortune': 'Small Fortune', 'chinese-checkers': 'Chinese Checkers' },
};

function fmt(s, ...args) {
  let i = 0;
  return String(s ?? '').replace(/%(?:\[(\d+)\])?([sd%])/g, (_, n, v) => {
    if (v === '%') return '%';
    if (n) i = Number(n) - 1;
    return String(args[i++]);
  });
}
const el = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
};

async function init() {
  try {
    T = { ...T, ...(await (await fetch('texts.json')).json()) };
  } catch { /* English, as written */ }
  for (const e of document.querySelectorAll('[data-t]')) {
    if (T[e.dataset.t]) e.textContent = T[e.dataset.t];
  }
  document.title = T.title;
  connect();
}

let retry = 0;
function connect() {
  const ws = new WebSocket(new URL('ws', location.href.replace(/^http/, 'ws')));
  ws.onopen = () => { retry = 0; $('notice').hidden = true; };
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.t === 'tables') show(m);
  };
  ws.onclose = () => {
    $('notice').textContent = T.reconnect;
    $('notice').hidden = false;
    setTimeout(connect, Math.min(1000 * 2 ** retry++, 15000));
  };
}

// games are what a visitor may open at a free table; failed, why the
// last try at a table did not open, by table.
let games = [];
const failed = new Map();

function show(m) {
  games = m.games ?? [];
  const sub = document.querySelector('[data-t="sub"]');
  sub.textContent = games.length ? T.subOpen : T.sub;
  $('tables').replaceChildren(...m.tables.map(card));
}

// open asks the lobby to host game at table n, and goes to its page.
async function open(n, game, buttons) {
  for (const b of buttons) b.disabled = true;
  failed.delete(n);
  try {
    const res = await fetch('new', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ game, table: n }),
    });
    const m = await res.json().catch(() => ({}));
    if (res.ok && m.url) {
      location.href = new URL(m.url, location.href).href;
      return;
    }
    failed.set(n, m.error || res.statusText);
  } catch (e) {
    failed.set(n, fmt(T.failed, e.message));
  }
  for (const b of buttons) b.disabled = false;
  const note = buttons[0]?.closest('.table')?.querySelector('.note');
  if (note) { note.textContent = failed.get(n); note.classList.add('failed'); }
}

// card is a table: free, or its game with the players and how to join it.
function card(t) {
  const li = el('li', 'table');
  const head = el('div', 'head');
  head.append(el('h3', 'kicker', fmt(T.table, t.n)));
  li.append(head);
  const st = t.status;
  const state = el('span', 'state');
  head.append(state);
  if (t.away) {
    // The host dropped: a short word in the head, why under the title.
    li.classList.add('away');
    state.textContent = T.reconnecting;
    state.classList.add('waiting');
  }
  if (st) failed.delete(t.n);
  if (!st) {
    if (t.away) li.append(el('p', 'note', T.away));
    else {
      li.classList.add('free');
      const why = failed.get(t.n);
      const note = el('p', why ? 'note failed' : 'note', why ?? (games.length ? T.freeOpen : T.freeNote));
      li.append(el('h2', '', T.free), note);
      if (games.length) {
        const acts = el('div', 'row new');
        const buttons = games.map((g) => el('button', 'button quiet', T.games[g] ?? g));
        buttons.forEach((b, i) => { b.type = 'button'; b.onclick = () => open(t.n, games[i], buttons); });
        acts.append(...buttons);
        li.append(acts);
      }
    }
    return li;
  }
  if (t.away) {
    li.append(el('h2', '', T.games[st.game] ?? st.game), el('p', 'note', T.away));
  } else {
    if (st.state === 'lobby') {
      state.textContent = st.room > 0 ? fmt(T.room, st.room) : T.lobby;
      state.classList.toggle('open', st.room > 0);
    } else state.textContent = T[st.state] ?? '';
    li.append(el('h2', '', T.games[st.game] ?? st.game));
  }
  const ul = el('ul');
  for (const s of st.seats ?? []) {
    const row = el('li', s.kind === 'open' ? 'empty' : ['local', 'visitor'].includes(s.kind) ? 'person' : '');
    if (s.kind === 'visitor' && !s.here) row.classList.add('gone');
    row.append(el('b', '', s.kind === 'open' ? T.open : s.name));
    if (s.kind !== 'open') row.append(el('span', '', T[s.kind] ?? ''));
    ul.append(row);
  }
  li.append(ul);
  if (st.lead) li.append(el('p', 'note lead', fmt(T.leads, st.lead)));
  const acts = el('div', 'row');
  const page = `t/${t.n}/#${st.code}`;
  if (st.state === 'lobby' && st.room > 0 && !t.away) {
    const join = el('a', 'button primary', T.join);
    join.href = page;
    acts.append(join);
  }
  const watch = el('a', 'button quiet', T.watch);
  watch.href = page;
  acts.append(watch);
  li.append(acts);
  return li;
}

init();
