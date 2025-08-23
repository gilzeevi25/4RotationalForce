<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'

const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').trim()

function makeUrl(path, params = {}) {
  // Robust URL builder that tolerates trailing/leading slashes
  const base = API_BASE.replace(/\/+$/,'')
  const p = path.startsWith('/') ? path : `/${path}`
  const url = new URL(base + p)
  Object.entries(params).forEach(([k,v]) => url.searchParams.set(k, String(v)))
  return url
}

const ip = ref('')
const loading = ref(false)
const errorMsg = ref('')
const result = ref(null)

const open = ref(false)
const suggestions = ref([])
const highlighted = ref(-1)
let abortCtrl = null
let debounceTimer = null
let suggestTimeout = null

const inputEl = ref(null)
const listboxId = 'ip-suggestions'
const activeDesc = computed(() => (highlighted.value >= 0 ? `opt-${highlighted.value}` : undefined))

const ipRegex = /^(25[0-5]|2[0-4]\d|1?\d?\d)(\.(25[0-5]|2[0-4]\d|1?\d?\d)){3}$/
const partialRegex = /^[0-9.]{1,15}$/
const valid = computed(() => ipRegex.test(ip.value))

function setError(msg) {
  errorMsg.value = msg
  result.value = null
}

async function fetchSuggest(prefix) {
  if (!partialRegex.test(prefix) || prefix.length < 2 || !API_BASE) {
    suggestions.value = []
    open.value = false
    return
  }
  if (abortCtrl) abortCtrl.abort()
  abortCtrl = new AbortController()

  // add a safety timeout to avoid dangling requests
  clearTimeout(suggestTimeout)
  suggestTimeout = setTimeout(() => abortCtrl?.abort(), 6000)

  try {
    const url = makeUrl('/v1/suggest', { prefix, limit: 10 })
    const r = await fetch(url, { signal: abortCtrl.signal, headers: { 'Accept': 'application/json' } })
    if (!r.ok) throw new Error('suggest failed')
    const data = await r.json()
    suggestions.value = Array.isArray(data?.suggestions) ? data.suggestions : []
    open.value = suggestions.value.length > 0
    highlighted.value = -1
    await nextTick()
  } catch {
    // non-blocking UX: ignore suggest failures
    open.value = false
  } finally {
    clearTimeout(suggestTimeout)
  }
}

function onInput(e) {
  const v = e.target.value.trim()
  ip.value = v
  setError('')
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => fetchSuggest(v), 280)
}

function onKeydown(e) {
  if (e.key === 'Enter' && !open.value) {
    // Enter submits when dropdown is closed
    e.preventDefault()
    submit()
    return
  }
  if (!open.value || suggestions.value.length === 0) return
  if (e.key === 'ArrowDown') {
    e.preventDefault()
    highlighted.value = (highlighted.value + 1) % suggestions.value.length
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    highlighted.value = (highlighted.value - 1 + suggestions.value.length) % suggestions.value.length
  } else if (e.key === 'Enter') {
    e.preventDefault()
    if (highlighted.value >= 0) {
      ip.value = suggestions.value[highlighted.value]
      open.value = false
    }
  } else if (e.key === 'Escape') {
    open.value = false
  } else if (e.key === 'Tab') {
    open.value = false
  }
}

function pick(s) {
  ip.value = s
  open.value = false
  inputEl.value?.focus()
}

async function submit() {
  open.value = false
  if (!API_BASE) {
    setError('API base is not configured (VITE_API_BASE_URL).')
    return
  }
  if (!valid.value) {
    setError('invalid IP')
    return
  }
  loading.value = true
  setError('')
  result.value = null
  try {
    const url = makeUrl('/v1/find-country', { ip: ip.value })
    const r = await fetch(url, { headers: { 'Accept': 'application/json' } })
    const data = await r.json()
    if (!r.ok) {
      setError(data?.error || 'internal error')
    } else {
      result.value = data
    }
  } catch {
    setError('internal error')
  } finally {
    loading.value = false
  }
}

function onClickOutside(e) {
  const root = document.getElementById('ip-search-root')
  if (root && !root.contains(e.target)) open.value = false
}

onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => {
  document.removeEventListener('click', onClickOutside)
  clearTimeout(debounceTimer)
  clearTimeout(suggestTimeout)
  if (abortCtrl) abortCtrl.abort()
})
</script>

<template>
  <form class="form" @submit.prevent="submit" novalidate>
    <div id="ip-search-root">
      <div class="input-wrap">
        <input
          ref="inputEl"
          class="input"
          type="text"
          inputmode="numeric"
          pattern="^([0-9]{1,3}\.){3}[0-9]{1,3}$"
          autocomplete="off"
          autocapitalize="off"
          spellcheck="false"
          placeholder="e.g., 2.22.233.255 or 8.8.8.8"
          :aria-invalid="!valid && ip.length>0"
          :aria-controls="listboxId"
          role="combobox"
          aria-autocomplete="list"
          :aria-expanded="open"
          :aria-activedescendant="activeDesc"
          :value="ip"
          @input="onInput"
          @keydown="onKeydown"
          @focus="() => suggestions.length && (open=true)"
        />

        <div
          v-if="open"
          class="suggestions"
          role="listbox"
          :id="listboxId"
          aria-label="IP suggestions"
        >
          <div
            v-for="(s, i) in suggestions"
            :key="s"
            class="sugg-item"
            role="option"
            :id="`opt-${i}`"
            :aria-selected="i===highlighted"
            @mousemove="highlighted=i"
            @mousedown.prevent="pick(s)"
          >
            <span>🔎</span><span>{{ s }}</span>
          </div>
        </div>
      </div>

      <button class="btn" :disabled="loading || !valid" type="submit">
        {{ loading ? 'Looking…' : 'Find' }}
      </button>

      <div v-if="result" class="result" role="status" aria-live="polite">
        <div><b>Country:</b> {{ result.country }}</div>
        <div><b>City:</b> {{ result.city }}</div>
      </div>

      <div v-if="errorMsg" class="error" role="alert">{{ errorMsg }}</div>
      <div class="helper">
        UI only accept IPv4 (e.g., 8.8.8.8). Autocomplete offers known IPs from the active datastore.
      </div>
    </div>
  </form>
</template>
