const isDev = process.env.NODE_ENV !== 'production'

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
          href: '/favicon.ico',
        },
        {
          rel: 'icon',
          sizes: '16x16',
          type: 'image/png',
          href: '/favicons/favicon-16.png',
        },
        {
          rel: 'icon',
          sizes: '32x32',
          type: 'image/png',
          href: '/favicons/favicon-32.png',
        },
        {
          rel: 'icon',
          type: 'image/svg+xml',
          href: '/favicons/favicon.svg',
        },
        {
          rel: 'apple-touch-icon',
          sizes: '180x180',
          href: '/favicons/favicon-180.png',
        },
        {
          rel: 'manifest',
          href: '/manifest.webmanifest',
        },
      ],

      script: [
        ...(isDev
          ? []
          : [
              {
                key: 'ym',
                type: 'text/javascript',
                async: true,
                defer: true,
                innerHTML: `(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
                  m[i].l=1*new Date();
                  for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
                  k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
                  (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
                  ym(92355058, "init", {
                    clickmap:true,
                    trackLinks:true,
                    accurateTrackBounce:true,
                    webvisor:true,
                    ecommerce:"dataLayer"
                  });
                `,
              },
              {
                key: 'tmr',
                type: 'text/javascript',
                async: true,
                defer: true,
                innerHTML: `var _tmr = window._tmr || (window._tmr = []);
                  _tmr.push({id: "3412212", type: "pageView", start: (new Date()).getTime()});
                  (function (d, w, id) {
                    if (d.getElementById(id)) return;
                    var ts = d.createElement("script"); ts.type = "text/javascript"; ts.async = true; ts.id = id;
                    ts.src = "https://top-fwz1.mail.ru/js/code.js";
                    var f = function () {var s = d.getElementsByTagName("script")[0]; s.parentNode.insertBefore(ts, s);};
                    if (w.opera == "[object Opera]") { d.addEventListener("DOMContentLoaded", f, false); } else { f(); }
                  })(document, window, "tmr-code");
                `,
              },
              {
                key: 'carrot',
                type: 'text/javascript',
                async: true,
                defer: true,
                innerHTML: `!function(){function t(t,e){return function(){window.carrotquestasync.push(t,arguments)}}
                  if("undefined"==typeof carrotquest){var e=document.createElement("script");
                  e.type="text/javascript",
                  e.async=!0,
                  e.src="https://cdn.carrotquest.app/api.min.js",
                  document.getElementsByTagName("head")[0].appendChild(e),
                  window.carrotquest={},
                  window.carrotquestasync=[],
                  carrotquest.settings={};for(var n=["connect","track","identify","auth","onReady","addCallback","removeCallback","trackMessageInteraction"],a=0;a<n.length;a++)
                  carrotquest[n[a]]=t(n[a])}}(),
                  carrotquest.connect("56910-0324662aa8602916189c749fbe");
                `,
              },
            ]
        ),
      ],

      noscript: [
        {
          key: 'ym-noscript',
          innerHTML: `<div><img src="https://mc.yandex.ru/watch/92355058" style="position:absolute; left:-9999px;" alt="" /></div>`,
          tagPosition: 'bodyClose',
        },
        {
          key: 'tmr-noscript',
          innerHTML: `<div><img src="https://top-fwz1.mail.ru/counter?id=3412212;js=na" style="position:absolute;left:-9999px;" alt="Top.Mail.Ru" /></div>`,
          tagPosition: 'bodyClose',
        },
      ],
    },
    pageTransition: {
      name: 'fade',
      mode: 'out-in',
    },
  },
})
