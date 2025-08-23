<script setup>
import IpSearch from './components/IpSearch.vue'
const apiBase = import.meta.env.VITE_API_BASE_URL || ''
const missingApi = !apiBase
</script>

<template>
  <div id="app">
    <div class="container">
      <div class="glass">
        <div class="h1">Spin2Country 🌍</div>
        <div class="subtitle">
          Type an IPv4 address. I’ll spin it up and return its <b>country</b> and <b>city</b>.
        </div>

        <div v-if="missingApi" class="banner">
          <b>Heads up:</b> VITE_API_BASE_URL is not set. Create <code>apps/frontend/.env.local</code>
          with <code>VITE_API_BASE_URL=http://localhost:8080</code> (or your Render URL) and rebuild.
        </div>

        <IpSearch />
        <div class="footer">⚡ Hint: Enter something like <code>0.1.2.3</code> to trigger some <b>torq</b>ue jokes.</div>
      </div>
    </div>
    <PresentedBy />
  </div>
</template>
