<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const sections = [
  {
    id: 'stage-1',
    title: '1. Backend',
    icon: 'server',
    summary: 'FastAPI service, env-driven config, clean routes, strict validation & clear JSON errors.',
    bullets: [
      'Env vars: DATASTORE_PROVIDER, DATA_FILE_PATH, allowed origins.',
      'Routes: GET /healthz, GET /v1/find-country, GET /v1/suggest',
      'Invalid IPv4 → 400 with {"error":"invalid IP"}; not found → 404.'
    ],
    codePeek: `# main.py (snippets)
/* CORS from settings, locator from factory, strict IPv4 check */
@app.get("/v1/find-country")
def find_country(ip: str = Query(...)):
    if not _is_ipv4(ip): return 400
    res = LOCATOR.lookup(ip)
    if not res:        return 404
    return {"country": country, "city": city}`
  },
  {
    id: 'stage-2',
    title: '2. Datastore & Extensibility',
    icon: 'database',
    summary: 'Pluggable IpLocator interface; CSV provider with in-memory dict + sorted list + bisect prefix search.',
    bullets: [
      'Base interface: IpLocator.lookup(ip), IpLocator.suggest(prefix, limit).',
      'CSV provider: validates IPv4, stores (country, city).',
      'Suggest: bisect over sorted IPs (O(log n) + k).'
    ],
    codePeek: `# datastore/base.py
class IpLocator(ABC):
    @abstractmethod
    def lookup(self, ip: str) -> Optional[tuple[str, str]]: ...
    @abstractmethod
    def suggest(self, prefix: str, limit: int = 10) -> list[str]: ...

# datastore/factory.py
def build_locator(provider: str, data_path: str) -> IpLocator:
    if provider == "csv": return CsvIpLocator(data_path)
    raise ValueError("Unsupported provider")`
  },
  {
    id: 'stage-3',
    title: '3. Frontend',
    icon: 'sparkles',
    summary: 'Vue 3 + Vite. IPv4 regex validation, debounced suggest, abortable fetch, keyboard nav.',
    bullets: [
      'Regex guards: full IPv4 & partial prefix.',
      'Debounce ~280ms; AbortController + timeout for suggest.',
      'Arrow keys cycle suggestions; Enter picks; Escape/Tab closes.'
    ],
    codePeek: `// IpSearch.vue (snippets)
const ipRegex = /^(25[0-5]|2[0-4]\\d|1?\\d?\\d)(\\.(25[0-5]|2[0-4]\\d|1?\\d?\\d)){3}$/;
const partialRegex = /^[0-9.]{1,15}$/;
debounceTimer = setTimeout(() => fetchSuggest(v), 280);
abortCtrl = new AbortController();`
  },
  {
    id: 'stage-4',
    title: '4. Integration & Tips',
    icon: 'link',
    summary: 'Front end talks to back end via VITE_API_BASE_URL; CORS whitelisting; easy deploy (Pages + Render).',
    bullets: [
      'Robust URL builder trims slashes; consistent Accept: application/json.',
      'CORS allowlist controlled from settings; lock down prod origins.',
      'Future: IPv6, trie-based suggest, rate limiting, structured telemetry.'
    ],
    codePeek: `// makeUrl helper (IpSearch.vue)
function makeUrl(path, params = {}) {
  const base = (import.meta.env.VITE_API_BASE_URL || '').replace(/\\/+$/, '');
  const p = path.startsWith('/') ? path : \`/\${path}\`;
  const url = new URL(base + p);
  Object.entries(params).forEach(([k,v]) => url.searchParams.set(k, String(v)));
  return url;
}`
  }
]

// collapsible “code peek”
const openIds = ref(new Set())

function toggle(id) {
  const n = new Set(openIds.value)
  n.has(id) ? n.delete(id) : n.add(id)
  openIds.value = n
}

// intersection observer to emit active section id (for sticky nav)
const activeId = ref('')
const emit = defineEmits(['active-change'])
let observer
onMounted(() => {
  const options = { root: null, rootMargin: '0px 0px -60% 0px', threshold: 0.1 }
  observer = new IntersectionObserver((entries) => {
    const visible = entries.filter(e => e.isIntersecting).sort((a,b) => b.intersectionRatio - a.intersectionRatio)
    if (visible[0]) {
      const id = visible[0].target.id
      activeId.value = id
      emit('active-change', id)
    }
  }, options)
  sections.forEach(s => {
    const el = document.getElementById(s.id)
    if (el) observer.observe(el)
  })
})

onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <div class="stages-wrapper" aria-label="How this project was built">
    <nav class="stage-inpage-nav" aria-label="Stage navigation">
      <a v-for="s in sections" :key="s.id" class="stage-link" :href="'#' + s.id" :class="{active: activeId === s.id}">
        <span class="dot" aria-hidden="true"></span>
        <span class="label">{{ s.title }}</span>
      </a>
    </nav>

    <section
      v-for="s in sections"
      :key="s.id"
      :id="s.id"
      class="stage-section"
      tabindex="-1"
      :aria-labelledby="s.id + '-title'"
    >
      <div class="stage-icon" :data-icon="s.icon" aria-hidden="true"></div>
      <h2 class="stage-title" :id="s.id + '-title'">{{ s.title }}</h2>
      <p class="stage-summary">{{ s.summary }}</p>
      <ul class="stage-bullets">
        <li v-for="(b,i) in s.bullets" :key="i">{{ b }}</li>
      </ul>

      <button
        class="stage-toggle"
        type="button"
        :aria-expanded="openIds.has(s.id)"
        @click="toggle(s.id)"
      >
        {{ openIds.has(s.id) ? 'Hide code peek' : 'Show code peek' }}
      </button>

      <div v-show="openIds.has(s.id)" class="code-peek" role="region" :aria-label="s.title + ' code snippet'">
        <pre><code>{{ s.codePeek }}</code></pre>
      </div>
    </section>
  </div>
</template>

<style scoped>
.stages-wrapper {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 2rem;
  padding: 2rem 1rem 4rem;
}

.stage-inpage-nav {
  position: sticky;
  top: 0.75rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 0.75rem;
  padding: 0.5rem 0.25rem;
  background: color-mix(in oklab, white 85%, transparent);
  backdrop-filter: blur(6px);
  border-radius: 999px;
  z-index: 2;
}

.stage-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.6rem;
  text-decoration: none;
  border-radius: 999px;
  font-size: 0.85rem;
  line-height: 1;
  color: #213646;
  border: 1px solid rgba(0,0,0,0.06);
}
.stage-link:focus { outline: 2px solid #1DBEE6; outline-offset: 2px; }
.stage-link:hover { background: rgba(29,190,230,0.07); }
.stage-link.active {
  background: rgba(29,190,230,0.15);
  font-weight: 600;
}
.stage-link.active .dot { opacity: 1; }

.stage-link .dot {
  width: 6px; height: 6px; border-radius: 999px; background: currentColor;
  opacity: 0.7;
}

.stage-section {
  padding: 2rem 1rem;
  border-radius: 16px;
  background:
    radial-gradient(60% 40% at 10% 0%, rgba(29,190,230,0.06), transparent 60%),
    radial-gradient(40% 60% at 90% 100%, rgba(33,54,70,0.06), transparent 60%),
    #ffffff;
  border: 1px solid rgba(0,0,0,0.05);
}

.stage-icon {
  width: 42px; height: 42px; border-radius: 10px;
  display: inline-flex; align-items: center; justify-content: center;
  margin-bottom: 0.5rem; background: #f0fbfe; color: #1DBEE6;
}
.stage-icon::before {
  display: inline-block; font-size: 22px; line-height: 1;
  /* minimal icon glyphs without external libs */
  content: attr(data-icon);
  /* visually map: server → 🖥, database → 🗄, sparkles → ✨, link → 🔗 */
}
.stage-icon[data-icon="server"]::before   { content: "🖥"; }
.stage-icon[data-icon="database"]::before { content: "🗄"; }
.stage-icon[data-icon="sparkles"]::before { content: "✨"; }
.stage-icon[data-icon="link"]::before     { content: "🔗"; }

.stage-title { margin: 0.25rem 0 0.25rem; color: #213646; font-size: 1.4rem; }
.stage-summary { margin: 0.25rem 0 0.75rem; color: #4a5c6a; }
.stage-bullets { margin: 0.5rem 0 1rem 1rem; color: #394957; }

.stage-toggle {
  display: inline-block;
  font-size: 0.9rem;
  padding: 0.4rem 0.7rem;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.1);
  background: #f8fcff;
  color: #213646;
}
.stage-toggle:hover { background: #eef8ff; }

.code-peek {
  margin-top: 0.75rem;
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.08);
  background: #0b2534;
  color: #d9f2ff;
  overflow: auto;
}
.code-peek pre { margin: 0; padding: 0.9rem 1rem; font-size: 0.85rem; }

@media (prefers-reduced-motion: no-preference) {
  .stage-section { transition: transform 200ms ease, box-shadow 200ms ease; }
  .stage-section:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,0,0,0.06); }
}
</style>
