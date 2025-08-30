<script setup>
import IpSearch from './components/IpSearch.vue'
import PresentedBy from './components/PresentedBy.vue'
import BuildStages from './components/BuildStages.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL || ''
const missingApi = !apiBase
</script>

<template>
  <main id="app-container">
    <!-- HERO: existing search block -->
    <section class="hero">
      <div class="hero-inner">
        <h1 class="hero-title">Spin2Country</h1>
        <p class="hero-subtitle">Type an IPv4, find its country & city</p>
        <IpSearch />
        <PresentedBy />
        <a class="scroll-hint" href="#stage-1" aria-label="Scroll to the build stages">↓ Learn how it was built</a>
      </div>
      <div class="hero-bg" aria-hidden="true"></div>
    </section>

    <!-- STAGES: the landing sections -->
    <BuildStages />
  </main>
</template>

<style scoped>
.hero {
  position: relative;
  padding: 3rem 1rem 1.25rem;
  text-align: center;
  overflow: hidden;
}
.hero-inner { max-width: 900px; margin: 0 auto; }
.hero-title { font-size: 2rem; margin: 0 0 0.25rem; color: #213646; }
.hero-subtitle { color: #4a5c6a; margin-bottom: 0.75rem; }

.scroll-hint {
  display: inline-block;
  margin-top: 0.75rem;
  text-decoration: none;
  color: #1DBEE6;
  font-weight: 600;
}
.scroll-hint:hover { text-decoration: underline; }

.hero-bg {
  position: absolute; inset: -10% -10% auto -10%;
  height: 60%;
  background:
    radial-gradient(40% 40% at 20% 20%, rgba(29,190,230,0.12), transparent 60%),
    radial-gradient(50% 40% at 80% 10%, rgba(33,54,70,0.12), transparent 60%),
    linear-gradient(180deg, rgba(255,255,255,0), rgba(255,255,255,1) 55%);
  pointer-events: none;
  z-index: -1;
}
</style>
