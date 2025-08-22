<template>
  <div>
    <input v-model="ip" placeholder="Enter IP" />
    <button @click="search">Search</button>
    <p v-if="country">Country: {{ country }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const ip = ref('')
const country = ref('')

function search() {
  country.value = 'Unknown'
}
</script>
