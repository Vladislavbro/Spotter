export default defineNuxtPlugin({
  name: 'yandex-metrika',
  parallel: true,
  setup () {
    const router = useRouter()

    if (process.env.NODE_ENV !== 'production') {
      return
    }

    const id = 92355058

    const options = {
      webvisor: true,
      clickmap: true,
      useCDN: false,
      trackLinks: true,
      accurateTrackBounce: true,
      ecommerce: 'dataLayer',
      metrikaUrl: '',
    }

    const metrikaUrl = (options.useCDN ? 'https://cdn.jsdelivr.net/npm/yandex-metrica-watch' : 'https://mc.yandex.ru/metrika') + '/tag.js'
    options.metrikaUrl = metrikaUrl

    let ready = false
    const basePath = (router.options.base || '/').replace(/\/$/, '')

    router.isReady(() => {
      ready = true
    })

    function create () {
      if (!ready) {
        (function (m, e, t, r, i, k, a) {
          m[i] = m[i] || function () {
            (m[i].a = m[i].a || []).push(arguments)
          }
          m[i].l = 1 * new Date()
          k = e.createElement(t),
          a = e.body.getElementsByTagName(t)[0],
          k.async = 1,
          k.src = r,
          a.parentNode.insertBefore(k, a)
        })(window, document, 'script', metrikaUrl, 'ym')

        ym(id, 'init', options)
      }

      router.afterEach((to, from) => {
        ym(id, 'hit', basePath + to.fullPath, {
          referer: basePath + from.fullPath,
        })
      })
    }

    if (window.ym === undefined) {
      create()
    }
  },
})
