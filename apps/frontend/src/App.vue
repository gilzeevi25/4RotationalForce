<script setup>
import IpSearch from './components/IpSearch.vue'
const apiBase = import.meta.env.VITE_API_BASE_URL || ''
const missingApi = !apiBase
</script>

<template>
  <div id="app">
    <div class="container">
      <div class="glass">
        <div class="h1">IP → Country</div>
        <div class="subtitle">
          Type an IPv4 address. We’ll look up its <b>country</b> and <b>city</b>.
        </div>

        <div v-if="missingApi" class="banner">
          <b>Heads up:</b> VITE_API_BASE_URL is not set. Create <code>apps/frontend/.env.local</code>
          with <code>VITE_API_BASE_URL=http://localhost:8080</code> (or your Render URL) and rebuild.
        </div>

        <IpSearch />
        <div class="footer">UI palette inspired by Torq (accent #85C4FF)</div>
      </div>
    </div>
    <PresentedBy />
  </div>
</template>
