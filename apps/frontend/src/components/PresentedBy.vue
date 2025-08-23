<template>
  <footer class="presented-by" role="contentinfo" aria-label="Presented by Gil Zeevi">
    <small class="presented-by__text">Presented by <strong>Gil Zeevi</strong></small>

    <!-- LinkedIn -->
    <a
      href="https://www.linkedin.com/in/gilzeevi"
      class="social-icon linkedin"
      aria-label="Gil Zeevi on LinkedIn"
      target="_blank"
      rel="noopener"
      @click="track('click_linkedin', { href: 'https://www.linkedin.com/in/gilzeevi' })"
    >
      <svg role="img" viewBox="0 0 24 24" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
        <title>LinkedIn</title>
        <path d="M20.447 20.452h-3.554v-5.569c0-1.327-.027-3.039-1.852-3.039-1.854 0-2.136 1.447-2.136 2.939v5.669h-3.554V9h3.414v1.561h.049c.476-.9 1.637-1.852 3.366-1.852 3.595 0 4.262 2.366 4.262 5.451v6.292zM5.337 7.433a2.062 2.062 0 1 1 0-4.124 2.062 2.062 0 0 1 0 4.124zM7.119 20.452H3.554V9h3.565v11.452zM22.225 0H1.771C.792 0 0 .771 0 1.729v20.542C0 23.229.792 24 1.771 24h20.451C23.206 24 24 23.229 24 22.271V1.729C24 .771 23.206 0 22.225 0z"/>
      </svg>
    </a>

    <!-- Email -->
    <a
      href="mailto:gzeevi25@gmail.com"
      class="social-icon gmail"
      aria-label="Email Gil Zeevi"
      @click="track('click_gmail', { href: 'mailto:gzeevi25@gmail.com' })"
    >
      <svg role="img" viewBox="0 0 24 24" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
        <title>Gmail</title>
        <rect x="1" y="4" width="22" height="16" rx="2" ry="2"
              style="fill:none;stroke:currentColor;stroke-width:2" />
        <polyline points="3,6 12,13 21,6"
                  style="fill:none;stroke:currentColor;stroke-width:2" />
      </svg>
    </a>

    <!-- GitHub -->
    <a
      href="https://github.com/gilzeevi25"
      class="social-icon github"
      aria-label="Gil Zeevi on GitHub"
      target="_blank"
      rel="noopener"
      @click="track('click_github', { href: 'https://github.com/gilzeevi25' })"
    >
      <svg role="img" viewBox="0 0 24 24" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
        <title>GitHub</title>
        <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.386-1.333-1.756-1.333-1.756-1.089-.744.083-.729.083-.729 1.205.084 1.84 1.238 1.84 1.238 1.07 1.835 2.808 1.305 3.495.998.108-.775.418-1.305.76-1.605-2.665-.303-5.466-1.332-5.466-5.931 0-1.31.469-2.381 1.237-3.221-.124-.303-.536-1.523.117-3.176 0 0 1.009-.322 3.301 1.23.96-.267 1.982-.399 3-.405 1.02.006 2.04.138 3 .405 2.291-1.553 3.3-1.23 3.3-1.23.654 1.653.242 2.873.118 3.176.77.84 1.236 1.911 1.236 3.221 0 4.61-2.807 5.625-5.479 5.921.431.371.814 1.102.814 2.221 0 1.604-.015 2.896-.015 3.289 0 .319.218.694.824.576C20.565 21.796 24 17.298 24 12c0-6.627-5.373-12-12-12z"/>
      </svg>
    </a>
  </footer>
</template>

<script setup>
// Safe telemetry helper (no-op if GA isn't present)
function track(eventName, params = {}) {
  try {
    if (typeof window !== 'undefined' && typeof window.gtag === 'function') {
      window.gtag('event', eventName, params);
    }
  } catch (_) {}
}
</script>

<style scoped>
:root {
  --primary: #213646;
  --accent:  #1DBEE6;
  --text:    #213646;
}

.presented-by {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.6rem;
  text-align: center;
  padding: 1rem 0 1.5rem;
  font-size: 0.9rem;
  color: #7a8b99;
  border-top: 1px solid rgba(0,0,0,0.05);
}

.presented-by__text strong { color: var(--text); }

.social-icon {
  display: inline-flex;
  width: 22px;
  height: 22px;
  line-height: 0;
  transition: transform 0.15s ease, opacity 0.15s ease;
  color: var(--accent);
}

.social-icon svg {
  width: 100%;
  height: 100%;
  fill: currentColor;
}

.social-icon:hover,
.social-icon:focus {
  transform: scale(1.12);
  outline: none;
}

@media (prefers-reduced-motion: reduce) {
  .social-icon { transition: none; }
}
</style>

