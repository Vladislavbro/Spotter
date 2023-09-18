<template>
  <div class="loader">
    <svg class="circular-loader" viewBox="25 25 50 50">
      <circle
        class="loader-path"
        cx="50"
        cy="50"
        r="20"
        fill="none"
        stroke-width="2"
      />
    </svg>
  </div>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.loader {
  position: relative;
  width: 30px;
  height: 30px;

  &:before {
    display: block;
    padding-top: 100%;
    content: '';
  }
}

.circular-loader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  margin: auto;
  transform-origin: center center;
  animation: rotate 2s linear infinite;
}

.loader-path {
  stroke: var(--black);
  stroke-dasharray: 150, 200;
  stroke-dashoffset: -10;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite, color 6s ease-in-out infinite;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -124;
  }
}

@keyframes color {
  0% {
    stroke: var(--white);
  }
  40% {
    stroke: var(--white);
  }
  66% {
    stroke: var(--white);
  }
  80%,
  90% {
    stroke: var(--white);
  }
}
</style>
