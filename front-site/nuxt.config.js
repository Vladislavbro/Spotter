export default defineNuxtConfig({
  css: [
    '@/assets/styles/_reset.css',
    '@/assets/styles/_colors.css',
    '@/assets/styles/_fonts.scss',
    '@/assets/styles/_global.scss',
  ],
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "@/assets/styles/index.scss" as *;',
        },
      },
    },
  },
  modules: [
    '@pinia/nuxt',
    'nuxt-swiper',
    'nuxt-lazy-load',
  ],

  lazyLoad: {
    images: false,
    videos: false,
    audios: false,
    iframes: false,
    native: false,
    directiveOnly: true,
    // defaultImage: '/images/default-image.jpg',
  },

  runtimeConfig: {
    public: {
      baseURL: process.env.BASE_URL,
    },
  },
  routeRules: {
    '/api/**': {
      proxy: {
        to: `${process.env.BASE_URL}/api/**`,
      },
    },
  },
  app: {
    head: {
      htmlAttrs: {
        lang: 'ru',
      },
      title: 'Spotter',
      meta: [
        {
          name: 'description',
          content: '',
        },
        { charset: 'utf-8' },
        {
          name: 'viewport',
          content:
            'width=device-width, height=device-height, initial-scale=1.0, maximum-scale=1.0',
        },
      ],
      link: [
        {
          rel: 'icon',
          type: 'image/x-icon',
          // href: `/favicon-${domain}.ico`,
        },
      ],
    },
    pageTransition: {
      name: 'fade',
      mode: 'out-in',
    },
  },
})
